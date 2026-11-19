# Proyecto

Reto 0 es una aplicación web Flask para registrar usuarios y gestionar tareas ficticias.
Cada usuario debe poder consultar únicamente sus propias tareas.

## Stack

Flask, SQLite, python-dotenv y pytest.

## Comandos

- Instalar: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
- Ejecutar: `.venv\Scripts\python.exe app.py`
- Pruebas: `.venv\Scripts\python.exe -m pytest -v`
- Estilo: `ruff check .`

## Estructura

- `app.py`: aplicación Flask, rutas y acceso a SQLite.
- `tests/`: pruebas automatizadas del reto.
- `requirements.txt`: dependencias de ejecución.
- `.env.example`: nombres de variables de entorno requeridas.
- `README.md`: instrucciones de uso.
- `evidencias.md`: registro de evidencias del taller.

## Qué no hacer

- No modificar las pruebas para que pasen.
- No escribir claves en el código.
- No instalar dependencias sin explicar para qué.
- No hacer commit ni push.

## Lecciones aprendidas

- Las contraseñas se guardan siempre con hash, nunca en texto plano.
- Las entradas obligatorias se validan en el servidor antes de guardar datos.
- Las consultas de tareas filtran siempre por el usuario autenticado.
