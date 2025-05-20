To write unit tests for the `/users/` endpoint, you can use the `TestClient` from FastAPI's `fastapi.testclient` module and `pytest`:

```python
# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserIn, UserOut
from fastapi import HTTPException
from bson import ObjectId

client = TestClient(app)

def test_create_user_success():
    response = client.post("/users/",
                           json={"username": "testuser", "email": "test@test.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@test.com"
    assert "id" in data

def test_create_user_existing_email():
    client.post("/users/",
                json={"username": "testuser", "email": "test@test.com"})
    response = client.post("/users/",
                           json={"username": "testuser2", "email": "test@test.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_create_user_invalid_data():
    response = client.post("/users/", json={"username": "testuser"})
    assert response.status_code == 422

def test_create_user_edge_case():
    response = client.post("/users/",
                           json={"username": "testuser", "email": "testuser@test.com"})
    assert response.status_code == 200
    response = client.post("/users/",
                           json={"username": "testuser", "email": "testuser@test.com"})
    assert response.status_code == 400
```

In these tests:

- `test_create_user_success()` tests a successful user creation.
- `test_create_user_existing_email()` tests the case where a user tries to register with an email that already exists in the database. The test first creates a user with a specific email, then tries to create another user with the same email, and checks if an error is returned.
- `test_create_user_invalid_data()` tests the case where the request data is not valid. In this case, the email is missing.
- `test_create_user_edge_case()` tests an edge case where two users with the same username but different emails are created. The first creation should succeed, and the second should fail because the email is the same.

Please note that these tests are not comprehensive and you should add more tests to cover all possible edge cases and scenarios. Also, these tests assume that each test runs independently and the data from one test doesn't affect another. If that's not the case, you might need to add setup and teardown steps to ensure the database is in the expected state before each test.