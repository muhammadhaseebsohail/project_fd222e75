To setup MongoDB database, you typically wouldn't expose an endpoint, instead, you would create and configure your database during application startup. Here is how you can do it with FastAPI and motor (the async MongoDB driver):

```python
# main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
    app.mongodb = app.mongodb_client['database_name']

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
```

In this code, we're creating a MongoDB connection when the application starts, and closing it when the application shuts down. The database connection is stored in `app.mongodb` and can be used in your endpoints.

Now, let's create a model and an endpoint to add a new user to our MongoDB database:

```python
# models.py
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    email: str

class UserOut(UserIn):
    id: str

# main.py
from fastapi import FastAPI, HTTPException
from models import UserIn, UserOut
from bson import ObjectId

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    """Create a new user"""
    if await app.mongodb["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_obj = { "username": user.username, "email": user.email }
    ret = await app.mongodb["users"].insert_one(user_obj)
    user_obj["id"] = str(ret.inserted_id)
    return user_obj
```

In this code, we have created two Pydantic models: `UserIn` (for request) and `UserOut` (for response). We have also created a POST endpoint `/users/` to add a new user to our MongoDB database. Before the new user is added, we check if the email already exists in the database, and if it does, we return a 400 error. If the email doesn't exist, we add the new user to the database and return the newly created user object.