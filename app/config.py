# app/config.py
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")  # Ruta absoluta al .env
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")

print(f"OPENAI_API_KEY cargada: {OPENAI_API_KEY}")  # Verificar en consola

