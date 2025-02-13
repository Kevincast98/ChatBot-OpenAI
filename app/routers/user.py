# app/routers/user.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas import UserCreate
from app.models import User
from app.database import get_session

router = APIRouter(prefix="/init_user", tags=["Usuarios"])

@router.post(
    "/",
    summary="Inicializar un usuario con rol predeterminado",
    description="""
    Crea un nuevo usuario con un rol específico si no existe en la base de datos.
    
    - **username**: Nombre del usuario (único).
    - **role**: Rol asignado al usuario.
    
    **Respuestas:**
    - ✅ `201`: Usuario creado exitosamente.
    - ❌ `400`: El usuario ya existe.
    """,
    responses={
        201: {
            "description": "Usuario creado exitosamente.",
            "content": {
                "application/json": {
                    "example": {"Success": True, "Detail": "Usuario 'admin' creado exitosamente."}
                }
            }
        },
        400: {
            "description": "El usuario ya existe.",
            "content": {
                "application/json": {
                    "example": {"Success": False, "Detail": "El usuario ya existe"}
                }
            }
        }
    }
)
def init_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Inicializa un usuario con un rol predeterminado.

    **Parámetros:**
    - `user`: Datos del usuario a crear.

    **Retorna:**
    - Un JSON con el estado de la operación.
    """
    # Verificar si el usuario ya existe
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Success": False, "Detail": "El usuario ya existe"}
        )

    # Crear el nuevo usuario
    nuevo_usuario = User(username=user.username, role=user.role)
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    # Retornar respuesta con éxito
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"Success": True, "Detail": f"Usuario '{user.username}' creado exitosamente."}
    )
