import sqlite3
from datetime import datetime


def crear_tabla():
    conexion = sqlite3.connect("leads.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT,
            mensaje TEXT,
            respuesta_ia TEXT,
            fecha TEXT
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_lead(nombre, email, mensaje, respuesta_ia):
    conexion = sqlite3.connect("leads.db")
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO leads (nombre, email, mensaje, respuesta_ia, fecha)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, email, mensaje, respuesta_ia, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conexion.commit()
    conexion.close()

def obtener_leads():
    conexion = sqlite3.connect("leads.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, email, mensaje, respuesta_ia, fecha
        FROM leads
    """)

    filas = cursor.fetchall()
    conexion.close()

    leads = []

    for fila in filas:
        leads.append({
            "id": fila[0],
            "nombre": fila[1],
            "email": fila[2],
            "mensaje": fila[3],
            "respuesta_ia": fila[4],
            "fecha": fila[5]
        })

    return leads