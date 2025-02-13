# app/routers/chat.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas import Message, ChatResponse
from app.models import User, ChatHistory
from app.database import get_session
from app.services.openai_service import obtener_respuesta_openai

router = APIRouter(prefix="/ask", tags=["Chatbot"])

@router.post(
    "/",
    summary="Enviar mensaje al chatbot y obtener respuesta",
    description="""
    Este endpoint permite enviar un mensaje al chatbot y obtener una respuesta basada en OpenAI.

    - **username**: Nombre del usuario que envía el mensaje.
    - **message**: Contenido del mensaje a enviar.

    **Respuestas:**
    - ✅ `200`: Respuesta generada exitosamente.
    - ❌ `400`: El mensaje está vacío.
    - ❌ `404`: Usuario no encontrado.
    - ❌ `500`: Error interno con OpenAI.
    """,
    responses={
        200: {
            "description": "Respuesta generada con éxito.",
            "content": {
                "application/json": {
                    "example": {
                        "Success": True,
                        "Answer": "Hola, ¿en qué puedo ayudarte?",
                        "Detail": "Respuesta generada con éxito"
                    }
                }
            }
        },
        400: {
            "description": "El mensaje está vacío.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "El mensaje no puede estar vacío"}
                }
            }
        },
        404: {
            "description": "Usuario no encontrado.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "Usuario no encontrado"}
                }
            }
        },
        500: {
            "description": "Error interno con la API de OpenAI.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "Error en la API de OpenAI: {error}"}
                }
            }
        }
    }
)
def ask(message: Message, session: Session = Depends(get_session)):
    """
    **Envía un mensaje al chatbot y recibe una respuesta.**

    **Parámetros:**
    - `message`: Contiene el mensaje enviado por el usuario.

    **Retorna:**
    - Un JSON con la respuesta del chatbot.
    """
    # Validar que el mensaje no esté vacío
    if not message.message.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Success": False, "Detail": "El mensaje no puede estar vacío"}
        )
    
    # Verificar si el usuario existe
    statement = select(User).where(User.username == message.username)
    usuario = session.exec(statement).first()
    if not usuario:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"Success": False, "Detail": "Usuario no encontrado"}
        )
    
    # Llamada al servicio de OpenAI
    try:
        respuesta = obtener_respuesta_openai(message.message, usuario.role)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"Success": False, "Detail": f"Error en la API de OpenAI: {str(e)}"}
        )
    
    # Guardar la interacción en la base de datos
    historial = ChatHistory(
        username=message.username,
        question=message.message,
        answer=respuesta
    )
    session.add(historial)
    session.commit()
    session.refresh(historial)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Success": True,
            "Answer": respuesta,
            "Detail": "Respuesta generada con éxito"
        }
    )
