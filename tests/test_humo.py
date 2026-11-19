from app import app


def test_pagina_principal_responde():
    app.config["TESTING"] = True
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200

