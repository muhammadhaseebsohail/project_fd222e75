The necessary Pydantic models and service code are already provided in the question. The missing part is the 'get_database' function which is required to establish a connection to the MongoDB. Here is the code for it:

```python
from pymongo import MongoClient
from fastapi import Depends
from starlette.requests import Request

def get_database(request: Request):
    return request.state.db
```

This function will be used in the API endpoint as a dependency to get the database connection.

And here is the complete code for the API endpoint including all necessary imports:

```python
from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .models import UserCreate, User
from .services import create_user
from pymongo import MongoClient

app = FastAPI()

def get_database(request: Request):
    return request.state.db

@app.post("/user", response_model=User)
async def create_user_endpoint(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Create a new user in the system.

    - **name**: The name of the user
    - **email**: The email of the user
    - **phone_number**: The phone number of the user
    - **password**: The password of the user
    """
    return await create_user(db, user)
```

The API endpoint is a POST request to "/user" which takes a 'UserCreate' object from the request body and a database connection from the 'get_database' dependency. It returns a 'User' object after creating a new user in the database. If an error occurs during the creation of the user, it raises an HTTPException with status code 400.