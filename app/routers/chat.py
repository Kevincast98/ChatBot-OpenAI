# app/routers/chat.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.schemas import Message, ChatResponse
from app.models import User, ChatHistory
from app.database import get_session
from app.services.openai_service import obtener_respuesta_openai
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/ask", tags=["Chatbot"])

@router.post("/", summary="Enviar mensaje al chatbot y obtener respuesta")
def ask(message: Message, session: Session = Depends(get_session)):
    # Validar que el mensaje no esté vacío
    if not message.message.strip():
        return JSONResponse(
            status_code=400,
            content={"Success": False, "Detail": "El mensaje no puede estar vacío"}
        )
    
    # Verificar si el usuario existe
    statement = select(User).where(User.username == message.username)
    usuario = session.exec(statement).first()
    if not usuario:
        return JSONResponse(
            status_code=404,
            content={"Success": False, "Detail": "Usuario no encontrado"}
        )
    
    # Llamada al servicio de OpenAI
    try:
        respuesta = obtener_respuesta_openai(message.message, usuario.role)
    except Exception as e:
        return JSONResponse(
            status_code=500,
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
        status_code=200,
        content={
            "Success": True,
            "Answer": respuesta,
            "Detail": "Respuesta generada con éxito"
        }
    )
