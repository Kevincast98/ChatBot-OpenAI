# FastAPI Chatbot

## Descripción
Este es un proyecto de chatbot desarrollado con FastAPI, utilizando SQLAlchemy para la gestión de bases de datos y SQLite como base de datos predeterminada. El chatbot maneja autenticación de usuarios y almacenamiento de datos de conversación.

## Características
- Base de datos gestionada con SQLAlchemy y SQLite.
- Autenticación y manejo de usuarios.
- Implementación de pruebas unitarias
- Despliegue con Uvicorn.


## Instalación
1. **Clona el repositorio:**
   ```bash
    git clone https://github.com/Kevincast98/ChatBot-OpenAI.git
    cd fastapi-chatbot

2. **Crear entorno virtual**

        python -m venv venv
        source venv/bin/activate  # En Linux/Mac
        venv\Scripts\activate  # En Windows

3. **Instalar dependencias**

        pip install -r requirements.txt

4. **Crear el .env**
Debido a temas de credenciales y compatibilidad, debes crear un archivo con el siguiente nombre ".env" ubicado en la carpeta raiz donde se agregaran las credenciales:

- **Estrutura:** 
    ```bash
    /fastapi-chatbot
    │── app/
    │   ├── config.py
    │   ├── services/
    │   ├── routers/
    │── .env <-------aqui debes crear el archivo ".env"
    │── main.py


- **Archivo ".env":**  Dentro del archivo ".env" deben agregarse estas credenciales y guardar el archivo:
    ```bash
    OPENAI_API_KEY=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

    DATABASE_URL=sqlite+aiosqlite:///./database.db

## Ejecucion del proyecto
Para ejecutar la API en desarrollo:

    uvicorn app.main:app --reload
 La API estará disponible en http://127.0.0.1:8000.
## Pruebas
Ejecuta las pruebas con:

    pytest

ubicarse en la carpeta de test y ejecutar comando en la terminal


## Swagger
Documentacion

    http://127.0.0.1:8000/docs

## Tecnologías utilizadas
- FastAPI
- SQLite
- Uvicorn
- Pytest
- Postman


🔹 Desarrollado por Kevin Castrillon 
