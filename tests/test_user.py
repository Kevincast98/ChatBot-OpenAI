# tests/test_user.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, get_session
from app.models import User

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_init_user(client):
    # Crear un nuevo usuario
    user_data = {"username": "testuser_3", "role": "admin"}
    response = client.post("/init_user/", json=user_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.json()}"
    assert response.json() == {"Success": True, "Detail": "Usuario 'testuser_3' creado exitosamente."}

    # Intentar crear el mismo usuario nuevamente
    response = client.post("/init_user/", json=user_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}. Response: {response.json()}"
    assert response.json() == {"Success": False, "Detail": "El usuario ya existe"}

def test_init_user_invalid_data(client):
    # Intentar crear un usuario sin nombre de usuario
    user_data = {"role": "user"}
    response = client.post("/init_user/", json=user_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}. Response: {response.json()}"