#!/usr/bin/env python3

import databases
from mymodels import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

#from typing import Optional
from typing_extensions import Annotated
import httpx


# Database Configuration
DATABASE_URL = "sqlite:///./cache.db?check_same_thread=False"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# FastAPI App
app = FastAPI()



@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Convert JSON object to database format
def __extract_table_fields(vin:str, vin_details: dict):
    return {
        'vin'          : vin,
        'make'         : vin_details["Make"],
        'model'        : vin_details["Model"],
        'model_year'   : vin_details["ModelYear"],
        'body_class'   : vin_details["BodyClass"]
    }

# Unpack Python Objects for export, this could be handled using batch processing and other tools
def __extract_rows_from_objects(cached_vins):
    return [obj.__dict__ for obj in cached_vins]

# Helper function to fetch VIN details from vPIC API
async def __fetch_vin_details(vin: str):

    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()["Results"][0]

# Routes
@app.get("/lookup")
async def lookup_vin(vin: Annotated[
    str,
    Query(
        title="VIN",
        description="A 17 digit alphanumeric string.",
        regex='[A-Za-z0-9]{17}')]
):
    session = SessionLocal()
    cached_vin = session.get(VIN, vin)
    
    if cached_vin:
        return VINResponse(**cached_vin.__dict__, cached_result=True)
    else:
        # Call vPIC API and fetch VIN details
        try:
            vin_details    = await __fetch_vin_details(vin)
            table_details  = __extract_table_fields(vin, vin_details)
            print(table_details)
            
            # Create a new VIN record in the cache
            new_vin = VIN(**table_details)
            session.add(new_vin)
            session.commit()

            return VINResponse(**{**table_details, 'cached_result': False})
        except httpx.HTTPError:
            return {"error": "Failed to fetch VIN details from vPIC API."}




@app.get("/remove")
async def remove_vin(vin: Annotated[
    str,
    Query(
        title="VIN",
        description="A 17 digit alphanumeric string.",
        regex='[A-Za-z0-9]{17}')]
):
    
    session = SessionLocal()
    cached_vin = session.get(VIN, vin)
    
    if cached_vin:
        session.delete(cached_vin)
        session.commit()
        return RemoveResponse(vin=vin, cache_delete_success=True)
    else:
        #raise HTTPException(status_code=404, detail="VIN not found in cache")
        return RemoveResponse(vin=vin, cache_delete_success=False)



@app.get("/export")
async def export_cache():
    session = SessionLocal()
    query = session.query(VIN)
    cached_vins = __extract_rows_from_objects(query.all())
    
    # Export rows to a Parquet file
    # You'll need to install the 'pyarrow' package for this
    
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    df = pd.DataFrame(cached_vins, columns=["vin", "make", "model", "model_year", "body_class"])
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "cache.parquet")

    file_path = "cache.parquet"
    
    # Return the exported file as a response
    return FileResponse(file_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

