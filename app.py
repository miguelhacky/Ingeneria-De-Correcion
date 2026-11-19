import sqlite3
import os

from flask import Flask, g, redirect, render_template_string, request, session, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-only-placeholder")
DATABASE = "tasks.sqlite3"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    db.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        session["user_id"] = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        return redirect(url_for("tasks"))
    return render_template_string(
        """
        <h1>Reto 0: Mis tareas</h1>
        <form method="post">
          <input name="username" placeholder="Usuario">
          <input name="password" type="password" placeholder="Contraseña">
          <button>Registrarme</button>
        </form>
        """
    )


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    init_db()
    if "user_id" not in session:
        return redirect(url_for("index"))
    db = get_db()
    if request.method == "POST":
        title = request.form["title"]
        db.execute("INSERT INTO tasks (user_id, title) VALUES (?, ?)", (session["user_id"], title))
        db.commit()
    rows = db.execute("SELECT * FROM tasks").fetchall()
    return render_template_string(
        "<h1>Mis tareas</h1><form method='post'><input name='title'><button>Crear</button></form>"
        "<ul>{% for task in tasks %}<li>{{ task['title'] }}</li>{% endfor %}</ul>",
        tasks=rows,
    )


if __name__ == "__main__":
    app.run(debug=True)

