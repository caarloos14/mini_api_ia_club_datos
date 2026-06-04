# Mini API con IA - Club de Datos

Este proyecto es una demo sencilla para construir una API con Python, FastAPI, Gemini, SQLite y envío automático de correos.

La idea de la práctica es simular un flujo real de automatización para un negocio:

1. Un cliente deja sus datos y escribe un mensaje.
2. La API recibe ese mensaje.
3. Gemini genera una respuesta automática.
4. El lead se guarda en una base de datos SQLite.
5. Opcionalmente, se envía un correo automático al cliente.

---

## 1. Crear el Codespace

Enlace directo recomendado:

```text
https://codespaces.new/caarloos14/mini_api_ia_club_datos?ref=main
```

Comprobar que la rama seleccionada sea:

```text
main
```

Después pulsar:

```text
Create codespace
```

Se abrirá un VS Code en el navegador.

---

## 2. Instalar dependencias

En la terminal del Codespace ejecutar:

```bash
pip install -r requirements.txt
```

Si `uvicorn` no se reconoce después de instalar, se puede ejecutar con:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 3. Variables de entorno

El proyecto necesita un archivo `.env` para guardar claves privadas.

Crear un archivo llamado:

```text
.env
```

y añadir estas variables:

```env
GEMINI_API_KEY=tu_clave_de_gemini
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion
```

---

## 4. ¿De dónde saco `GEMINI_API_KEY`?

La clave de Gemini se obtiene desde Google AI Studio.

Pasos generales:

1. Entrar en Google AI Studio.
2. Iniciar sesión con una cuenta de Google.
3. Ir a la sección de API keys.
4. Crear una nueva API key.
5. Copiarla y pegarla en el archivo `.env`.

Ejemplo:

```env
GEMINI_API_KEY=AIza...
```

No se debe subir esta clave a GitHub.

---

## 5. ¿De dónde saco `EMAIL_USER`?

`EMAIL_USER` es el correo desde el que se enviarán los emails automáticos.

Ejemplo:

```env
EMAIL_USER=mi_correo@gmail.com
```

---

## 6. ¿De dónde saco `EMAIL_PASSWORD`?

Si se usa Gmail, no se debe poner la contraseña normal de Gmail.

Hay que crear una contraseña de aplicación.

Pasos generales:

1. Entrar en la cuenta de Google.
2. Ir a Seguridad.
3. Activar la verificación en dos pasos.
4. Buscar "Contraseñas de aplicaciones".
5. Crear una contraseña de aplicación para este proyecto.
6. Copiar la contraseña de 16 caracteres.
7. Pegarla en el archivo `.env`.

Ejemplo:

```env
EMAIL_PASSWORD=abcdefghijklmnop
```

Si Google muestra la contraseña separada por espacios, se puede pegar sin espacios.

---

## 7. ¿Por qué usamos `.env`?

El archivo `.env` sirve para guardar información sensible fuera del código.

Por ejemplo:

- Claves de API.
- Correos.
- Contraseñas.
- Configuraciones privadas.

En Python usamos:

```python
from dotenv import load_dotenv
import os

load_dotenv()

clave = os.getenv("GEMINI_API_KEY")
```

`load_dotenv()` carga las variables del archivo `.env`.

`os.getenv(...)` permite leer esas variables desde Python.

Esto evita escribir claves privadas directamente dentro del código.

---

## 8. Importante: no subir `.env` a GitHub

El archivo `.env` contiene datos privados.

Por eso debe estar incluido en `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
leads.db
.venv/
```

Así Git no subirá esas claves al repositorio.

---

## 9. Ejecutar la API

Cuando ya esté creado `main.py`, ejecutar:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O también:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Codespaces mostrará un aviso indicando que el puerto 8000 está disponible.

Pulsar:

```text
Open in Browser
```

---

## 10. Probar la API

La ruta principal es:

```text
/
```

Debe devolver algo parecido a:

```json
{
  "mensaje": "API funcionando correctamente"
}
```

La documentación interactiva de FastAPI está en:

```text
/docs
```

Desde `/docs` se pueden probar los endpoints sin crear una interfaz web.

---

## 11. Flujo del proyecto

El flujo completo de la demo es:

```text
Cliente envía datos
        ↓
FastAPI recibe la petición
        ↓
Pydantic valida los datos
        ↓
Gemini genera una respuesta automática
        ↓
SQLite guarda el lead
        ↓
Opcionalmente se envía un email automático
        ↓
La API devuelve una respuesta en JSON
```

---

## 12. Archivos principales

### `main.py`

Contiene la API principal.

Aquí se definen las rutas:

- `GET /`
- `POST /lead`
- `GET /leads`

### `ia_service.py`

Contiene la lógica para llamar a Gemini.

Lee la variable:

```env
GEMINI_API_KEY
```

y usa esa clave para generar respuestas automáticas.

### `database.py`

Contiene las funciones para trabajar con SQLite:

- Crear la tabla.
- Guardar leads.
- Obtener leads.

SQLite guarda la base de datos en un archivo llamado:

```text
leads.db
```

Si `leads.db` no existe, SQLite lo crea automáticamente.

Si ya existe, se conecta a la base de datos existente.

### `email_service.py`

Contiene la función para enviar correos automáticos.

Lee estas variables del `.env`:

```env
EMAIL_USER
EMAIL_PASSWORD
```

y usa SMTP para enviar el correo.

---

## 13. Ver la base de datos desde terminal

Para ver la base de datos en Codespaces, instalar SQLite si hace falta:

```bash
sudo apt update
sudo apt install sqlite3 -y
```

Después abrir la base de datos:

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

## 14. Qué es un lead

Un lead es una persona que muestra interés en un producto o servicio.

Por ejemplo, alguien que deja su nombre, email y mensaje pidiendo información.

En esta demo, cada lead se guarda con:

- Nombre.
- Email.
- Mensaje original.
- Respuesta generada por IA.
- Fecha.

---

## 15. Por qué usamos placeholders en SQL

En SQLite usamos consultas como esta:

```python
cursor.execute(\"\"\"
    INSERT INTO leads (nombre, email, mensaje, respuesta_ia, fecha)
    VALUES (?, ?, ?, ?, ?)
\"\"\", (nombre, email, mensaje, respuesta_ia, fecha))
```

Los signos `?` son placeholders.

Sirven para separar el código SQL de los datos del usuario.

Esto ayuda a evitar inyecciones SQL, porque aunque un usuario escriba algo que parezca código SQL, SQLite lo trata como texto normal y no como una instrucción ejecutable.

---

## 16. Comandos útiles

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

Ver datos:

```sql
SELECT * FROM leads;
```

Salir de SQLite:

```sql
.quit
```

---

## 17. Nota final

Esta demo usa SQLite para simplificar la práctica y evitar instalaciones complejas.

En un proyecto real se podría sustituir SQLite por PostgreSQL, MySQL o una base de datos en la nube, manteniendo una estructura muy parecida en el resto de la API.
