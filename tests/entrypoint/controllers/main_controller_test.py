import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))
from fastapi.testclient import TestClient
from main.entrypoint.main import app

client = TestClient(app)

def test_should_return_info():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "system" in data
    assert "machine" in data
    assert "processor" in data
    assert "python_version" in data
    assert "environment" in data
