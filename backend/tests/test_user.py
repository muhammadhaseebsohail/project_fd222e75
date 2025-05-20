You can use FastAPI's TestClient in conjunction with pytest to test your API endpoints. Below is an example of a test suite for the above endpoint:

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app
import pytest

@pytest.fixture
def test_app() -> FastAPI:
    return app

@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)

def test_create_user_success(client: TestClient):
    response = client.post(
        "/user",
        json={
            "name": "Test",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "password": "test1234"
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["phone_number"] == "1234567890"
    assert "password" not in response.json()

def test_create_user_bad_request(client: TestClient):
    response = client.post(
        "/user",
        json={
            "name": "Test",
            "email": "test",
            "phone_number": "1234567890",
            "password": "test1234"
        },
    )
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_user_invalid_phone_number(client: TestClient):
    response = client.post(
        "/user",
        json={
            "name": "Test",
            "email": "test@example.com",
            "phone_number": "123",
            "password": "test1234"
        },
    )
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_user_no_password(client: TestClient):
    response = client.post(
        "/user",
        json={
            "name": "Test",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "password": ""
        },
    )
    assert response.status_code == 422
    assert "detail" in response.json()
```

In the above code, a pytest fixture is used to create a TestClient instance. This client is then used to send HTTP requests to the API and check the responses. Various edge cases are tested, such as invalid email, invalid phone number and empty password.