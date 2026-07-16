import pytest
from fastapi.testclient import TestClient
from app.main import app

# This initializes the FastAPI test client
client = TestClient(app)

def test_api_health():
    """
    Test that the base API endpoint is up, running, and accessible.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_pii_redaction_email():
    """
    Test that the LLM Shield scans and processes email payloads properly.
    """
    test_payload = {
        "prompt": "My personal email is nayabgull@gmail.com and I need help."
    }
    
    # Hit the correct endpoint path
    response = client.post("/api/v1/shield/scan", json=test_payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert against your actual ScanResponse schema fields
    assert "safe" in data
    assert "risk_score" in data
    assert "matched_patterns" in data