import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_read_main():
    """Test the main root path for a simple response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_evaluate_essay():
    """Test the essay evaluation endpoint."""
    request_data = {
        "prompt_id": 1,
        "essay_output": "This is a sample essay.",
        "student_id": "test123"
    }
    response = client.post("/evaluate", json=request_data)
    assert response.status_code == 200
    assert 'criticism' in response.json()
    assert response.json()['student_id'] == "test123"

def test_invalid_data():
    """Test the endpoint with invalid data to ensure it handles errors properly."""
    response = client.post("/evaluate", json={"invalid": "data"})
    assert response.status_code == 422
