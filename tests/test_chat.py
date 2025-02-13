# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app.models import User, ChatHistory
from sqlmodel import Session
from sqlalchemy import text

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

@pytest.fixture(autouse=True)
def clear_data():
    with Session(engine) as session:
        session.execute(text("DELETE FROM user"))
        session.execute(text("DELETE FROM chathistory"))
        session.commit()

def test_ask(client):
    # Crear un nuevo usuario
    user_data = {"username": "testuser", "role": "user"}
    response = client.post("/init_user/", json=user_data)
    assert response.status_code == 201

    # Enviar un mensaje al chatbot
    message_data = {"username": "testuser", "message": "Hola"}
    response = client.post("/ask/", json=message_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json()["Success"] == True
    assert "Answer" in response.json()

def test_ask_user_not_found(client):
    # Enviar un mensaje al chatbot con un usuario no existente
    message_data = {"username": "unknownuser", "message": "Hola"}
    response = client.post("/ask/", json=message_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json() == {"Success": False, "Detail": "Usuario no encontrado"}

def test_ask_empty_message(client):
    # Crear un nuevo usuario
    user_data = {"username": "testuser", "role": "user"}
    response = client.post("/init_user/", json=user_data)
    assert response.status_code == 201

    # Enviar un mensaje vacío al chatbot
    message_data = {"username": "testuser", "message": ""}
    response = client.post("/ask/", json=message_data)
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 400
    assert response.json() == {"Success": False, "Detail": "El mensaje no puede estar vacío"}