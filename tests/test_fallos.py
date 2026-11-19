import sqlite3

import pytest

import app as modulo


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(modulo, "DATABASE", str(tmp_path / "test.sqlite3"))
    modulo.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with modulo.app.test_client() as cliente:
        yield cliente


def registrar(cliente, usuario, clave):
    return cliente.post(
        "/",
        data={"username": usuario, "password": clave},
        follow_redirects=True,
    )


def test_no_guarda_contrasena_en_texto_plano(cliente, tmp_path, monkeypatch):
    registrar(cliente, "ana", "Clave123*")
    db = sqlite3.connect(str(tmp_path / "test.sqlite3"))
    guardada = db.execute("SELECT password FROM users WHERE username = 'ana'").fetchone()[0]
    db.close()
    assert guardada != "Clave123*"


def test_rechaza_usuario_vacio(cliente):
    respuesta = cliente.post("/", data={"username": "", "password": "Clave123*"})
    assert respuesta.status_code == 400


def test_usuario_no_ve_tareas_de_otro_usuario(cliente):
    registrar(cliente, "ana", "Clave123*")
    cliente.post("/tasks", data={"title": "Tarea privada de Ana"})
    cliente.get("/", follow_redirects=False)
    with cliente.session_transaction() as sesion:
        sesion["user_id"] = 2
    respuesta = cliente.get("/tasks")
    assert b"Tarea privada de Ana" not in respuesta.data

