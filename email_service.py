import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def enviar_correo_cliente(destinatario: str, nombre: str, respuesta: str):
    """
    Envía un correo automático al cliente con la respuesta generada por la IA.

    Esta función utiliza los datos guardados en el archivo .env:
    - EMAIL_USER: correo desde el que se envía el mensaje.
    - EMAIL_PASSWORD: contraseña de aplicación del correo.

    Recibe el email del cliente, su nombre y la respuesta generada por la IA.
    Después construye un correo sencillo y lo envía usando SMTP.
    """

    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_password:
        raise ValueError("Faltan EMAIL_USER o EMAIL_PASSWORD en el archivo .env")

    asunto = "Respuesta automática a tu consulta"

    cuerpo = f"""
Hola {nombre},

Gracias por contactar con nosotros.

{respuesta}

Un saludo,
Equipo del gimnasio
"""

    mensaje = EmailMessage()
    mensaje["From"] = email_user
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

#Quiero conectarme al servidor SMTP de Gmail usando una conexión segura. SMTP es el protocolo que se usa para enviar correos. 465 es el puerto seguro
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_password)
        smtp.send_message(mensaje)