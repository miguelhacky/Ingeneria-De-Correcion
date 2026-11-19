import sqlite3

import pytest

import app as modulo


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(modulo, "DATABASE", str(tmp_path / "test.db"))
    modulo.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with modulo.app.test_client() as cliente:
        yield cliente


def registrar(cliente, correo, clave):
    return cliente.post(
        "/register",
        data={"email": correo, "password": clave},
        follow_redirects=True,
    )


def test_no_guarda_contrasena_en_texto_plano(cliente, tmp_path):
    registrar(cliente, "ana@example.com", "Clave123*")
    db = sqlite3.connect(str(tmp_path / "test.db"))
    guardada = db.execute(
        "SELECT password FROM users WHERE email = 'ana@example.com'"
    ).fetchone()[0]
    db.close()
    assert guardada != "Clave123*"


def test_rechaza_correo_vacio(cliente):
    respuesta = cliente.post(
        "/register", data={"email": "", "password": "Clave123*"}
    )
    assert respuesta.status_code == 400


def test_usuario_no_puede_modificar_tarea_de_otro(cliente, tmp_path):
    registrar(cliente, "ana@example.com", "Clave123*")
    cliente.post("/tasks", data={"title": "Tarea privada de Ana"})
    cliente.get("/logout")
    registrar(cliente, "beto@example.com", "Clave456*")
    cliente.get("/tasks/1/toggle")
    db = sqlite3.connect(str(tmp_path / "test.db"))
    tarea = db.execute("SELECT done FROM tasks WHERE id = 1").fetchone()
    db.close()
    assert tarea[0] == 0
