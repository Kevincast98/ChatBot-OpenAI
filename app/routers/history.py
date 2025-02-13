# app/routers/history.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from app.models import ChatHistory, User
from app.schemas import ChatHistoryResponse
from app.database import get_session
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/history", tags=["Historial"])

@router.get(
    "/{username}",
    summary="Consultar el historial de mensajes de un usuario",
    description="""
    Este endpoint permite consultar el historial de interacciones de un usuario con el chatbot.

    - **username**: Nombre de usuario del cual se desea obtener el historial de conversaciones.

    **Respuestas:**
    - ✅ `200`: Historial obtenido exitosamente.
    - ❌ `400`: Nombre de usuario vacío.
    - ❌ `404`: Usuario o historial no encontrado.
    - ❌ `500`: Error interno del servidor.
    """,
    responses={
        200: {
            "description": "Historial obtenido exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "Success": True,
                        "Detail": "Historial obtenido exitosamente",
                        "Data": [
                            {
                                "username": "usuario1",
                                "question": "¿Cuál es la capital de Francia?",
                                "answer": "París",
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "El nombre de usuario no puede estar vacío.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "El nombre de usuario no puede estar vacío"}
                }
            }
        },
        404: {
            "description": "Usuario o historial no encontrado.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "No se encontró historial para el usuario"}
                }
            }
        },
        500: {
            "description": "Ocurrió un error interno.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "Ocurrió un error interno", "Error": "Descripción del error"}
                }
            }
        }
    }
)
def get_history(username: str, session: Session = Depends(get_session)):
    """
    **Consulta el historial de mensajes de un usuario.**

    **Parámetros:**
    - `username`: Nombre de usuario del cual se obtendrá el historial.

    **Retorna:**
    - Un JSON con el historial de interacciones del usuario.
    """
    # Validar que el username no esté vacío
    if not username or username.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Success": False, "Detail": "El nombre de usuario no puede estar vacío"}
        )

    try:
        # Verificar si el usuario existe
        user_statement = select(User).where(User.username == username)
        usuario = session.exec(user_statement).first()
        if not usuario:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"Success": False, "Detail": "Usuario no encontrado"}
            )

        # Obtener historial de mensajes
        statement = select(ChatHistory).where(ChatHistory.username == username)
        historial = session.exec(statement).all()

        if not historial:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"Success": False, "Detail": "No se encontró historial para el usuario"}
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "Success": True,
                "Detail": "Historial obtenido exitosamente",
                "Data": [history.dict() for history in historial]
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"Success": False, "Detail": "Ocurrió un error interno", "Error": str(e)}
        )
