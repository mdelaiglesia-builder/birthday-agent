from fastapi.testclient import TestClient
from app import app

def test_ask_routes_to_event_subagent():
    client = TestClient(app)
    response = client.post("/ask", json={"message": "where do I park?"})
    assert response.status_code == 200
    assert any(word in response.json()["agent"] for word in ["Parroquia San Ignacio de Loyola", "Molina Ciudad"])

def test_ask_routes_to_guest_subagent():
    client = TestClient(app)
    response = client.post("/ask", json={"message": "how many guests are coming?"})
    assert response.status_code == 200
    assert any(word in response.json()["agent"] for word in ["RSVP", "confirmed"])
