def test_crear_bloque_valido(client):
    resp = client.post("/agenda", json={
        "usuario_id": 1,
        "titulo": "Estudiar para el parcial",
        "fecha": "2026-09-15",
        "hora_inicio": "14:00",
        "hora_fin": "16:00",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["titulo"] == "Estudiar para el parcial"

def test_crear_bloque_falta_campo(client):
    resp = client.post("/agenda", json={
        "usuario_id": 1,
        "titulo": "Sin fecha",
    })
    assert resp.status_code == 400

def test_hora_fin_antes_que_inicio(client):
    resp = client.post("/agenda", json={
        "usuario_id": 1,
        "titulo": "Bloque inválido",
        "fecha": "2026-09-15",
        "hora_inicio": "16:00",
        "hora_fin": "14:00",
    })
    assert resp.status_code == 400
    assert "posterior" in resp.get_json()["error"]

def test_listar_bloques_de_usuario(client):
    client.post("/agenda", json={
        "usuario_id": 1, "titulo": "A", "fecha": "2026-09-15",
        "hora_inicio": "09:00", "hora_fin": "10:00",
    })
    client.post("/agenda", json={
        "usuario_id": 2, "titulo": "B", "fecha": "2026-09-15",
        "hora_inicio": "09:00", "hora_fin": "10:00",
    })
    resp = client.get("/agenda?usuario_id=1")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["titulo"] == "A"