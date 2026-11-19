import os
import sqlite3

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-only-placeholder")
DATABASE = "tasks.db"

PAGE = """
<!doctype html><html lang="es"><head><meta charset="utf-8"><title>TaskBloom</title></head>
<body>
{% with messages = get_flashed_messages() %}{% for message in messages %}<p>{{ message }}</p>{% endfor %}{% endwith %}
{% if session.get('user_id') %}
<p>Hola, {{ session['email'] }} <a href="{{ url_for('logout') }}">Cerrar sesión</a></p>
<h1>Mis tareas</h1><form method="post" action="{{ url_for('create_task') }}">
<input name="title" placeholder="Nueva tarea"><button>Agregar</button></form>
<ul>{% for task in tasks %}<li>{{ task[1] }}</li>{% endfor %}</ul>
{% else %}
<h1>TaskBloom</h1><form method="post" action="{{ url_for('register') }}">
<input name="email" placeholder="Correo"><input name="password" type="password"><button>Registrarme</button></form>
<form method="post" action="{{ url_for('login') }}"><input name="email" placeholder="Correo">
<input name="password" type="password"><button>Iniciar sesión</button></form>
{% endif %}</body></html>
"""


def db():
    connection = sqlite3.connect(DATABASE)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)"
    )
    connection.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER, user_id INTEGER)"
    )
    return connection


@app.get("/")
def index():
    connection = db()
    tasks = connection.execute(
        "SELECT id, title, done FROM tasks WHERE user_id = ?", (session.get("user_id"),)
    ).fetchall()
    connection.close()
    return render_template_string(PAGE, tasks=tasks)


@app.post("/register")
def register():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not email or not password or len(email) > 254 or len(password) > 200:
        abort(400, "Correo y contraseña son obligatorios")
    connection = db()
    try:
        cursor = connection.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        connection.commit()
        session["user_id"], session["email"] = cursor.lastrowid, email
    except sqlite3.IntegrityError:
        flash("El correo ya está registrado")
    finally:
        connection.close()
    return redirect(url_for("index"))


@app.post("/login")
def login():
    email = request.form.get("email", "").strip()
    connection = db()
    user = connection.execute(
        "SELECT id, email, password FROM users WHERE email = ?", (email,)
    ).fetchone()
    connection.close()
    if user and check_password_hash(user[2], request.form.get("password", "")):
        session["user_id"], session["email"] = user[0], user[1]
    else:
        flash("Credenciales inválidas")
    return redirect(url_for("index"))


@app.post("/tasks")
def create_task():
    if "user_id" not in session:
        return redirect(url_for("index"))
    title = request.form.get("title", "").strip()
    if not title or len(title) > 200:
        abort(400, "El título es obligatorio")
    connection = db()
    connection.execute(
        "INSERT INTO tasks (title, done, user_id) VALUES (?, 0, ?)",
        (title, session["user_id"]),
    )
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    connection = db()
    connection.execute(
        "UPDATE tasks SET done = 1 - done WHERE id = ? AND user_id = ?",
        (task_id, session.get("user_id")),
    )
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    connection = db()
    connection.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, session.get("user_id")),
    )
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
