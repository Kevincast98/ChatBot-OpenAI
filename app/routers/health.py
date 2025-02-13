# app/routers/health.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, text
from app.database import get_session
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Salud"])

@router.get(
    "/",
    summary="Verificar el estado del servicio y conexión a la base de datos",
    description="""
    Este endpoint permite comprobar si el servicio está activo y si la conexión a la base de datos es exitosa.

    **Respuestas:**
    - ✅ `200`: Servicio en funcionamiento y base de datos conectada.
    - ❌ `500`: Error en la conexión a la base de datos.
    """,
    responses={
        200: {
            "description": "El servicio está activo y la base de datos conectada.",
            "content": {
                "application/json": {
                    "example": {
                        "Success": True,
                        "Detail": "El servicio está activo",
                        "Database": "Conectada"
                    }
                }
            }
        },
        500: {
            "description": "Error en la conexión a la base de datos.",
            "content": {
                "application/json": {
                    "example": {
                        "Success": False,
                        "Detail": "Error en la conexión a la base de datos",
                        "Error": "Descripción del error"
                    }
                }
            }
        }
    }
)
def health_check(session: Session = Depends(get_session)):
    """
    **Verifica el estado del servicio y la conexión con la base de datos.**

    **Retorna:**
    - `200`: Si el servicio y la base de datos están funcionando correctamente.
    - `500`: Si hay un problema en la conexión con la base de datos.
    """
    try:
        # Ejecutar una consulta simple para verificar la conexión a la base de datos
        session.exec(text("SELECT 1"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "Success": True,
                "Detail": "El servicio está activo",
                "Database": "Conectada"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "Success": False,
                "Detail": "Error en la conexión a la base de datos",
                "Error": str(e)
            }
        )
