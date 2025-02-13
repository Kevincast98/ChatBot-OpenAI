# app/routers/history.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from app.models import ChatHistory, User
from app.schemas import ChatHistoryResponse
from app.database import get_session

router = APIRouter(prefix="/history", tags=["Historial"])

@router.get("/{username}", response_model=dict, summary="Consultar el historial de mensajes de un usuario")
def get_history(username: str, session: Session = Depends(get_session)):
    # Validar que el username no esté vacío
    if not username or username.strip() == "":
        return {
            "Success": False,
            "Detail": "El nombre de usuario no puede estar vacío"
        }

    try:
        # Verificar si el usuario existe
        user_statement = select(User).where(User.username == username)
        usuario = session.exec(user_statement).first()
        if not usuario:
            return {
                "Success": False,
                "Detail": "Usuario no encontrado"
            }

        # Obtener historial de mensajes
        statement = select(ChatHistory).where(ChatHistory.username == username)
        historial = session.exec(statement).all()

        if not historial:
            return {
                "Success": False,
                "Detail": "No se encontró historial para el usuario"
            }

        return {
            "Success": True,
            "Detail": "Historial obtenido exitosamente",
            "Data": historial
        }

    except Exception as e:
        return {
            "Success": False,
            "Detail": "Ocurrió un error interno",
            "Error": str(e)
        }

