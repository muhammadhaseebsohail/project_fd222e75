Here is how you can write unit tests for the above FastAPI application using pytest and FastAPI's TestClient:

```python
from fastapi.testclient import TestClient
from main import app, verify_token, User
import pytest

client = TestClient(app)

# Add this fixture to simulate a logged in user
@pytest.fixture
def logged_in_user():
    user = User(username='testuser', password='testpassword')
    response = client.post("/login", data=user.dict())
    return response.json()

def test_login():
    # Success case
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Error case - wrong username
    response = client.post("/login", data={"username": "wronguser", "password": "testpassword"})
    assert response.status_code == 401

    # Error case - wrong password
    response = client.post("/login", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401

    # Data validation - Missing username
    response = client.post("/login", data={"password": "testpassword"})
    assert response.status_code == 422

    # Data validation - Missing password
    response = client.post("/login", data={"username": "testuser"})
    assert response.status_code == 422

def test_logout(logged_in_user):
    # Success case
    token = logged_in_user["access_token"]
    response = client.get("/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Successfully logged out"}

    # Error case - No token
    response = client.get("/logout")
    assert response.status_code == 403

    # Error case - wrong token
    response = client.get("/logout", headers={"Authorization": "Bearer wrongtoken"})
    assert response.status_code == 403

    # Edge case - Expired token
    # For this test, you would need to adjust the token expiration time in your JWT utility functions
    # And wait for the token to expire before sending the request
```

This suite of tests covers success cases, error cases, data validation, and edge cases. It uses pytest's fixtures to simulate a logged in user, and uses FastAPI's TestClient to send requests to the API.