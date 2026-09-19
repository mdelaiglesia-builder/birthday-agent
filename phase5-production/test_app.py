from fastapi.testclient import TestClient
from app import app
import pytest

@pytest.mark.skip(reason="Requires a real Voyage AI API call; the free tier's 3 RPM limit makes this unreliable in CI even with the voyage_pacing fixture's spacing (see conftest.py). Skipped rather than paced -- unskip locally to verify against the real API.")
def test_ask_routes_to_event_subagent(voyage_pacing):
    client = TestClient(app)
    response = client.post("/ask", json={"message": "where do I park?"})
    assert response.status_code == 200
    assert any(word in response.json()["agent"] for word in ["Parroquia San Ignacio de Loyola", "Molina Ciudad"])

def test_ask_routes_to_guest_subagent():
    client = TestClient(app)
    response = client.post("/ask", json={"message": "how many guests are coming?"})
    assert response.status_code == 200
    assert any(word in response.json()["agent"] for word in ["RSVP", "confirmed"])
