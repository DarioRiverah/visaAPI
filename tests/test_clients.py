# tests/test_clients.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_platinum_ok():
    payload = {
        "name": "Alice",
        "country": "USA",
        "monthlyIncome": 1200,
        "viseClub": True,
        "cardType": "Platinum"
    }
    resp = client.post("/client", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["status"] == "Registered"
    assert data["cardType"] == "Platinum"
    # No asumas que siempre es 1 si otros tests ya crearon clientes:
    assert isinstance(data["clientId"], int)

def test_register_gold_rejected_low_income():
    payload = {
        "name": "Bob",
        "country": "USA",
        "monthlyIncome": 300,
        "viseClub": False,
        "cardType": "Gold"
    }
    resp = client.post("/client", json=payload)
    # Ahora devolvemos error PLANO sin 'detail'
    assert resp.status_code == 400
    data = resp.json()
    assert data["status"] == "Rejected"
