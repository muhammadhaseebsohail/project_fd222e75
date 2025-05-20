In this task, we're going to create a user collection in MongoDB via FastAPI. First, we'll design the user schema which includes a phone number. After that, we'll create POST endpoint to add a new user into the collection.

1. Pydantic models for request/response:
```python
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    class Config:
        orm_mode = True
```

2. Necessary service layer code:
```python
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from .models import UserCreate, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncIOMotorClient, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    user = await db["myDatabase"]["users"].insert_one({**user.dict(), "password": hashed_password})
    if user:
        return User(id=str(user.inserted_id), **user.dict())
    else:
        raise HTTPException(status_code=400, detail="Error occurred while creating user.")
```

3. API endpoint:
```python
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .models import UserCreate, User
from .services import create_user

app = FastAPI()

@app.post("/user", response_model=User)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Create a new user in the system.

    - **name**: The name of the user
    - **email**: The email of the user
    - **phone_number**: The phone number of the user
    - **password**: The password of the user
    """
    return await create_user(db, user)
```
Note: get_database function must be implemented to create database connection and it is not shown in the above snippet.

This code includes the creation of a user with required fields like name, email, phone_number, and password. Password is hashed before storing into the database. The API is documented with OpenAPI standards and the code is written following best practices of FastAPI.