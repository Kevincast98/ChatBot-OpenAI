# app/routers/user.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.schemas import UserCreate
from app.models import User
from app.database import get_session

router = APIRouter(prefix="/init_user", tags=["Usuarios"])

@router.post("/", summary="Inicializar un usuario con rol predeterminado")
def init_user(user: UserCreate, session: Session = Depends(get_session)):
    # Verificar si el usuario ya existe
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"Success": False, "Detail": "El usuario ya existe"}
        )

    # Crear el nuevo usuario
    nuevo_usuario = User(username=user.username, role=user.role)
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    # Retornar respuesta con éxito
    return JSONResponse(
        status_code=201,
        content={"Success": True, "Detail": f"Usuario '{user.username}' creado exitosamente."}
    )

