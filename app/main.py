# app/main.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import init_db
from app.routers import user, chat, history, health

app = FastAPI(
    title="Chatbot Configurable con Roles",
    description="API RESTful usando FastAPI y la API de OpenAI",
    version="0.28.0"
)

# Iniciar la base de datos al arrancar la aplicación
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir los routers
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(history.router)
app.include_router(health.router)

# Manejo global de errores de validación (422 Unprocessable Entity)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "Success": False,
            "Detail": "Campos requeridos no enviados o formato incorrecto.",
            "Errors": exc.errors()  # Muestra los errores específicos
        }
    )
