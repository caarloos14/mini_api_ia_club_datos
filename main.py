import os
import json
from datetime import datetime

from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from ia_service import generar_respuesta_ia
from database import crear_tabla, guardar_lead, obtener_leads
from email_service import enviar_correo_cliente

app = FastAPI()
crear_tabla()

class Mensaje(BaseModel):
    nombre: str
    email: str
    mensaje: str


@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

@app.get("/leads")
def ver_leads():
    leads = obtener_leads()

    return {
        "leads": leads
    }

@app.post("/lead")
def recibir_lead(datos: Mensaje):
    respuesta = generar_respuesta_ia(datos.mensaje)

    guardar_lead(
        datos.nombre,
        datos.email,
        datos.mensaje,
        respuesta
    )

    enviar_correo_cliente(
        datos.email,
        datos.nombre,
        respuesta
    )

    return {
        "mensaje": "Lead procesado y guardado correctamente",
        "nombre": datos.nombre,
        "email": datos.email,
        "mensaje_original": datos.mensaje,
        "respuesta_ia": respuesta
    }