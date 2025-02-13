# app/services/openai_service.py
import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def obtener_respuesta_openai(pregunta: str, role: str) -> str:
    """
    Llama a la API de OpenAI configurando un rol específico y devuelve la respuesta.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa un modelo más barato que text-davinci-003
            messages=[
                {"role": "system", "content": f"Actúa como un {role}. Responde de manera detallada."},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

    except openai.error.RateLimitError:
        return "Has excedido tu cuota gratuita en OpenAI. Revisa tu cuenta en https://platform.openai.com/account/billing"

    except openai.error.OpenAIError as e:
        return f"Error en la API de OpenAI: {str(e)}"
