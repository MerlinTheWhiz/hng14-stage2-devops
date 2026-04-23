import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_redis():
    with patch("main.r") as mock:
        yield mock

def test_create_job(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1
    
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert mock_redis.lpush.called
    assert mock_redis.hset.called

def test_get_job_exists(mock_redis):
    mock_redis.hget.return_value = b'completed'
    
    response = client.get("/jobs/1234-abcd")
    assert response.status_code == 200
    assert response.json() == {"job_id": "1234-abcd", "status": "completed"}
    mock_redis.hget.assert_called_with("job:1234-abcd", "status")

def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None
    
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "not found"}

def test_health_check(mock_redis):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
