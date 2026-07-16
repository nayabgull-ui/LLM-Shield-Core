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

def test_pii_redaction_email():
    """
    Test that the LLM Shield detects and redacts emails properly.
    """
    test_payload = {
        "prompt": "My personal email is nayabgull@gmail.com and I need help."
    }
    # Replace "/scan" with your actual endpoint path if it is different (e.g., "/api/v1/scan")
    response = client.post("/scan", json=test_payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert that the output prompt has redacted the email
    assert "nayabgull@gmail.com" not in data["sanitized_prompt"]
    assert "[REDACTED]" in data["sanitized_prompt"]