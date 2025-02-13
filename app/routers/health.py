# app/routers/health.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, text
from app.database import get_session

router = APIRouter(prefix="/health", tags=["Salud"])

@router.get("/", summary="Verificar el estado del servicio y conexión a la base de datos")
def health_check(session: Session = Depends(get_session)):
    """
    Endpoint para verificar el estado del servicio y la conexión con la base de datos.
    """
    try:
        # Ejecutar una consulta simple para verificar la conexión a la base de datos
        session.exec(text("SELECT 1"))
        return {
            "Success": True,
            "Detail": "El servicio está activo",
            "Database": "Conectada"
        }
    except Exception as e:
        return {
            "Success": False,
            "Detail": "Error en la conexión a la base de datos",
            "Error": str(e)
        }
