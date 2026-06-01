import os
from dotenv import load_dotenv
from google import genai

import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generar_respuesta_ia(mensaje: str):
    prompt = f"""
    Eres un asistente amable de un gimnasio.

    Responde de forma breve y clara al siguiente mensaje de un cliente.

    No uses Markdown.
    No uses negritas.
    No uses listas.
    Escribe solo texto plano.

    Mensaje del cliente:

    {mensaje}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


