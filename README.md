# Mini API con IA - Versión Solución

Esta rama contiene la versión completa de la demo de la Mini API con IA para el Club de Datos.

A diferencia de la rama `main`, donde el proyecto está preparado para construirse casi desde cero durante la clase, esta rama ya incluye todos los archivos principales:

```text
main.py
ia_service.py
database.py
email_service.py
requirements.txt
.gitignore
```

El objetivo de esta rama es servir como referencia completa para comprobar el funcionamiento final del proyecto.

---

## 1. Qué hace esta demo

La demo simula un flujo real de automatización para un negocio, por ejemplo un gimnasio.

El flujo completo es:

```text
Cliente envía nombre, email y mensaje
        ↓
FastAPI recibe la petición
        ↓
Pydantic valida los datos
        ↓
Gemini genera una respuesta automática
        ↓
SQLite guarda el lead en la base de datos
        ↓
Python envía un email automático al cliente
        ↓
La API devuelve una respuesta final en JSON
```

---

## 2. Estructura del proyecto

```text
mini_api_ia_club_datos/
│
├── main.py
├── ia_service.py
├── database.py
├── email_service.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. Instalar dependencias

Antes de ejecutar el proyecto, instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

Si `uvicorn` no se reconoce directamente, ejecutar la API usando:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 4. Variables de entorno necesarias

La versión solución necesita un archivo `.env`.

Crear un archivo llamado:

```text
.env
```

con este contenido:

```env
GEMINI_API_KEY=tu_clave_de_gemini
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion
```

Importante: el archivo `.env` no debe subirse a GitHub.

---

## 5. De dónde sale `GEMINI_API_KEY`

`GEMINI_API_KEY` es la clave que permite usar la API de Gemini.

Se obtiene desde Google AI Studio.

Pasos generales:

1. Entrar en Google AI Studio.
2. Iniciar sesión con una cuenta de Google.
3. Ir a la sección de API keys.
4. Crear una nueva clave.
5. Copiarla en el archivo `.env`.

Ejemplo:

```env
GEMINI_API_KEY=AIza...
```

Esta clave se usa en `ia_service.py`.

---

## 6. De dónde sale `EMAIL_USER`

`EMAIL_USER` es el correo desde el que se enviarán los mensajes automáticos.

Ejemplo:

```env
EMAIL_USER=mi_correo@gmail.com
```

Este correo se usa en `email_service.py`.

---

## 7. De dónde sale `EMAIL_PASSWORD`

Si se usa Gmail, `EMAIL_PASSWORD` no es la contraseña normal de Gmail.

Hay que generar una contraseña de aplicación.

Pasos generales:

1. Entrar en la cuenta de Google.
2. Ir a Seguridad.
3. Activar la verificación en dos pasos.
4. Buscar "Contraseñas de aplicaciones".
5. Crear una contraseña de aplicación.
6. Copiar la contraseña de 16 caracteres.
7. Pegarla en `.env`.

Ejemplo:

```env
EMAIL_PASSWORD=abcdefghijklmnop
```

Si Google muestra la contraseña separada por espacios, se puede pegar sin espacios.

---

## 8. Archivo `main.py`

`main.py` es el archivo principal de la API.

Aquí se crea la aplicación FastAPI:

```python
app = FastAPI()
```

También se llama a:

```python
crear_tabla()
```

para asegurarnos de que la tabla `leads` exista cuando se levanta el servidor.

### Rutas principales

#### `GET /`

Comprueba que la API está funcionando.

Devuelve:

```json
{
  "mensaje": "API funcionando correctamente"
}
```

#### `GET /leads`

Devuelve todos los leads guardados en la base de datos.

#### `POST /lead`

Recibe los datos de un cliente, genera una respuesta con IA, guarda el lead y envía un correo automático.

El cuerpo esperado es:

```json
{
  "nombre": "Carlos",
  "email": "carlos@email.com",
  "mensaje": "Hola, quiero información sobre el gimnasio"
}
```

---

## 9. Archivo `ia_service.py`

Este archivo contiene la lógica de conexión con Gemini.

Parte principal:

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Esto crea el cliente de Gemini usando la clave almacenada en `.env`.

La función principal es:

```python
generar_respuesta_ia(mensaje: str)
```

Esta función:

1. Recibe el mensaje del cliente.
2. Construye un prompt.
3. Envía el prompt a Gemini.
4. Devuelve el texto generado por la IA.

La respuesta se obtiene con:

```python
response.text.strip()
```

`response.text` extrae el texto generado por Gemini.

`strip()` limpia espacios y saltos de línea al principio y al final.

---

## 10. Archivo `database.py`

Este archivo contiene la lógica de base de datos usando SQLite.

SQLite guarda la base de datos en un archivo llamado:

```text
leads.db
```

Si el archivo no existe, SQLite lo crea automáticamente.

Si ya existe, se conecta a la base de datos existente.

### Funciones principales

#### `crear_tabla()`

Crea la tabla `leads` si todavía no existe.

La tabla tiene estas columnas:

```text
id
nombre
email
mensaje
respuesta_ia
fecha
```

#### `guardar_lead(nombre, email, mensaje, respuesta_ia)`

Guarda un nuevo lead en la tabla `leads`.

Usa placeholders:

```sql
VALUES (?, ?, ?, ?, ?)
```

Los placeholders separan el código SQL de los datos del usuario y ayudan a prevenir inyecciones SQL.

#### `obtener_leads()`

Lee todos los registros de la tabla `leads` y los devuelve como una lista de diccionarios.

Esto permite que FastAPI los devuelva como JSON.

---

## 11. Archivo `email_service.py`

Este archivo contiene la función encargada de enviar correos automáticos.

La función principal es:

```python
enviar_correo_cliente(destinatario, nombre, respuesta)
```

Esta función:

1. Lee `EMAIL_USER` desde `.env`.
2. Lee `EMAIL_PASSWORD` desde `.env`.
3. Construye el correo.
4. Se conecta al servidor SMTP de Gmail.
5. Inicia sesión.
6. Envía el mensaje.

La conexión SMTP se hace con:

```python
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(email_user, email_password)
    smtp.send_message(mensaje)
```

Esto significa:

```text
Conectarse de forma segura a Gmail
Iniciar sesión con correo y contraseña de aplicación
Enviar el mensaje
Cerrar la conexión automáticamente
```

---

## 12. Ejecutar la API

Ejecutar:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

En local también se puede usar:

```bash
uvicorn main:app --reload
```

En Codespaces es recomendable usar:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 13. Probar desde `/docs`

FastAPI genera documentación interactiva automáticamente.

Abrir:

```text
/docs
```

Desde ahí se pueden probar:

```text
GET /
GET /leads
POST /lead
```

Para probar `POST /lead`, usar un cuerpo como:

```json
{
  "nombre": "Carlos",
  "email": "carlos@email.com",
  "mensaje": "Hola, quiero información sobre las clases del gimnasio"
}
```

---

## 14. Ver la base de datos desde terminal

Instalar el comando de SQLite si hace falta:

```bash
sudo apt update
sudo apt install sqlite3 -y
```

Abrir la base de datos:

```bash
sqlite3 leads.db
```

Dentro de SQLite:

```sql
.headers on
.mode table
.tables
.schema leads
SELECT * FROM leads;
```

Para salir:

```sql
.quit
```

---

## 15. Diferencia entre SQLite y una base de datos tipo PostgreSQL

En esta demo usamos SQLite porque es simple y no requiere instalar un servidor de base de datos.

SQLite:

```text
Guarda la base de datos en un archivo .db
No necesita servidor
Es ideal para demos, pruebas y proyectos pequeños
```

PostgreSQL o MySQL:

```text
Funcionan como servidores de base de datos
Requieren usuario, contraseña, host y puerto
Son más habituales en producción
```

En un proyecto real, `database.py` podría modificarse para conectarse a PostgreSQL o MySQL sin cambiar demasiado el resto de la API.

---

## 16. Por qué usamos `.env`, `dotenv` y `os`

El archivo `.env` guarda configuraciones sensibles fuera del código.

Ejemplo:

```env
GEMINI_API_KEY=...
EMAIL_USER=...
EMAIL_PASSWORD=...
```

En Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

clave = os.getenv("GEMINI_API_KEY")
```

`load_dotenv()` carga las variables del archivo `.env`.

`os.getenv(...)` lee esas variables desde Python.

Esto permite usar claves privadas sin escribirlas directamente en el código.

---

## 17. Por qué no se sube `.env`

El archivo `.env` contiene credenciales privadas.

Por eso debe estar en `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
leads.db
.venv/
```

Así evitamos subir claves privadas, contraseñas o bases de datos de prueba a GitHub.

---

## 18. Comandos útiles

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar API:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Abrir SQLite:

```bash
sqlite3 leads.db
```

Ver tablas:

```sql
.tables
```

Ver estructura de la tabla:

```sql
.schema leads
```

Ver datos:

```sql
.headers on
.mode table
SELECT * FROM leads;
```

Salir de SQLite:

```sql
.quit
```

---

## 19. Para qué sirve esta rama

Esta rama sirve como solución completa del proyecto.

Se puede usar para:

```text
Comprobar el código final
Comparar con la rama main
Revisar errores durante la clase
Tener una referencia si algo falla
Mostrar el flujo completo ya terminado
```

La rama `main` está pensada para construir el proyecto paso a paso.

La rama `solucion` está pensada para tener la versión final funcionando.
