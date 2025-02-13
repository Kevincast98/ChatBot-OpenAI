# app/database.py

# from sqlmodel import SQLModel
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import DATABASE_URL

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    print("Inicializando la base de datos...")  # Para verificar que la función se ejecuta
    SQLModel.metadata.create_all(engine)
    print("Base de datos inicializada correctamente.")  # Confirmación

def get_session():
    with Session(engine) as session:
        yield session
