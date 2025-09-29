# tests/test_purchases.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_client(card_type="Platinum", income=1200, club=True, country="USA"):
    payload = {
        "name": "Tester",
        "country": country,
        "monthlyIncome": income,
        "viseClub": club,
        "cardType": card_type
    }
    r = client.post("/client", json=payload)
    assert r.status_code == 200, r.text
    return r.json()["clientId"]

def test_purchase_platinum_saturday_over_200_gets_30_percent():
    client_id = create_client(card_type="Platinum", income=1500, club=True, country="USA")
    # Sábado 2025-09-20
    purchase = {
        "clientId": client_id,
        "amount": 250.0,
        "currency": "USD",
        "purchaseDate": "2025-09-20T14:30:00Z",
        "purchaseCountry": "USA"
    }
    r = client.post("/purchase", json=purchase)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "Approved"
    assert data["purchase"]["discountApplied"] == 75.0  # 30% de 250
    assert data["purchase"]["finalAmount"] == 175.0
    # Tus labels traen el texto en español con "Sábado >200"
    assert "Sábado >200" in data["purchase"]["benefit"]

def test_purchase_black_from_banned_country_rejected():
    # Cliente Black válido (residencia NO baneada)
    client_id = create_client(card_type="Black", income=3000, club=True, country="USA")
    # Compra desde país prohibido
    purchase = {
        "clientId": client_id,
        "amount": 300.0,
        "currency": "USD",
        "purchaseDate": "2025-09-22T15:00:00Z",  # Lunes
        "purchaseCountry": "India"
    }
    r = client.post("/purchase", json=purchase)
    # Ahora devolvemos rechazo PLANO sin 'detail'
    assert r.status_code == 400
    data = r.json()
    assert data["status"] == "Rejected"

def test_purchase_platinum_abroad_saturday_picks_best_discount_not_additive():
    client_id = create_client(card_type="Platinum", income=1500, club=True, country="USA")
    # Sábado y en el exterior: 30% (sábado >200) compite con 5% exterior -> gana 30%
    purchase = {
        "clientId": client_id,
        "amount": 300.0,
        "currency": "USD",
        "purchaseDate": "2025-09-20T10:00:00Z",
        "purchaseCountry": "France"
    }
    r = client.post("/purchase", json=purchase)
    assert r.status_code == 200
    data = r.json()
    assert data["purchase"]["discountApplied"] == 90.0  # 30% de 300
    assert data["purchase"]["finalAmount"] == 210.0
    # Asegura que no acumuló el 5% adicional
    assert data["purchase"]["benefit"].startswith("Sábado >200")
