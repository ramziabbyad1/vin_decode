# VIN DECODER

This program uses python 3.8.11, but is probably compatibile with version >= 3.6. 

Make sure you have dependencies:
```
	$ pip install fastapi uvicorn httpx
	$ pip install pytest pytest-asyncio
	$ pip install pyarrow 
	$ pip install databases sqlalchemy
```

To start the server run: 
```
	$ python main.py
```

To run unit tests run:
```
	$ pytest -v test.py.
```

To view the results of cache /export, run:
```
	$ python display_cache.py 
```

## API Description:

This is a program that uses SQLAlchemy, and FastAPI to implement a VIN decoding information system.

There are three functions that can be accessed using this program.

**/lookup?vin={vin}**

>Check the cache for a vin record containing the appropriate fields from the problem description. If present, return a response object with cachei\_result = True. Otherwise return with cached\_result=False; cache the result.  The VIN must be a 17 digit alphanumeric string or else the function will return 422 HTTP ERROR: Unprocessable Entity. 

**/remove?vin={vin}**
	
>Check the cache for a vin record. If present, delete the object from cache and return with cache\_delete\_success=True. Otherwise return with cache\_delete\_success=False; The VIN must be a 17 digit alphanumeric string or else the function will return  422 HTTP ERROR: Unprocessable Entity.

**/export**
	
>Export the cached data to a parquet file and return a Response object. You can view the cached records using display cache, as mentioned above.

## TODO:

1. Build/production system      :  A system for cleaning and backing up files (including log files).  Note, the cache needs to be initialized
on StartUp
2. Dependency Injection					:  Configuration should be separate from implementation.
3. Batch Export                 :  To avoid straining the DB, this should be done in batches
4. Modularity          					:  The databse implementation should be separate from the API code and be accessed in global or static way.
5. Asynchronous IO     					:  The database should have a thread pool and support asynchronous lookups and updates.
6. Logging             					:  Logging should simplify bug-hunting and a logging framework with log-levels should be used. 
7. Empty VIN Fields    					:  Some VINs will have missing fields such as the 1988 Lamborghini Countach, which has no model and no body 
																	 class. This should be dealt with in a standardized way by consumers of the API.


## Testing

You can test the implmentation as follows, lookup is run twice to ensure the cache FLAG is set:
``` 
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XPWD40X1ED215307
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XKWDB0X57J211825
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XP5DB9X7YN526158
curl -w "\n" http://127.0.0.1:8000/lookup?vin=4V4NC9EJXEN171694
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XP5DB9X7XD487964
curl -w "\n" http://127.0.0.1:8000/lookup?vin=ZA9CA05AXJLA12340

curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XPWD40X1ED215307
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XKWDB0X57J211825
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XP5DB9X7YN526158
curl -w "\n" http://127.0.0.1:8000/lookup?vin=4V4NC9EJXEN171694
curl -w "\n" http://127.0.0.1:8000/lookup?vin=1XP5DB9X7XD487964
curl -w "\n" http://127.0.0.1:8000/lookup?vin=ZA9CA05AXJLA12340	

curl -sw "\n" http://127.0.0.1:8000/export
python display_cache.py

curl -w "\n" http://127.0.0.1:8000/remove?vin=1XPWD40X1ED215307
curl -w "\n" http://127.0.0.1:8000/remove?vin=1XKWDB0X57J211825
curl -w "\n" http://127.0.0.1:8000/remove?vin=1XP5DB9X7YN526158
curl -w "\n" http://127.0.0.1:8000/remove?vin=4V4NC9EJXEN171694
curl -w "\n" http://127.0.0.1:8000/remove?vin=1XP5DB9X7XD487964
curl -w "\n" http://127.0.0.1:8000/remove?vin=ZA9CA05AXJLA12340


curl -sw "\n" http://127.0.0.1:8000/export
python display_cache.py

```

