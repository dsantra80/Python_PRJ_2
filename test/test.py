import pytest
import requests
import json

BASE_URL = "http://localhost:5000"

def test_status():
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}

def test_generate():
    payload = {
        "prompt": "Tell me a story about a dragon",
        "max_tokens": 50,
        "temperature": 0.7
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/generate", data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    assert "response" in response.json()
