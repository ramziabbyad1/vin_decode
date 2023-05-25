#!/usr/bin/env python3

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel



Base = declarative_base()

# VIN Model
class VIN(Base):
    __tablename__ = "vin_cache"

    vin = Column(String(17), primary_key=True)
    make = Column(String)
    model = Column(String)
    model_year = Column(String)
    body_class = Column(String)


# Request Models
class VINRequest(BaseModel):
    vin: str


# Response Models
class VINResponse(BaseModel):
    vin: str
    make: str
    model: str
    model_year: str
    body_class: str
    cached_result: bool


class RemoveResponse(BaseModel):
    vin: str
    cache_delete_success: bool
