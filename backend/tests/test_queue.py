import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestQueue:
    """Queue API tests"""
    
    @pytest.fixture
    def auth_token(self):
        client.post("/api/auth/register", json={
            "name": "Queue User",
            "email": "queue@example.com",
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": "queue@example.com",
            "password": "TestPass123"
        })
        return response.json()["access_token"]
    
    def test_get_all_queues(self, auth_token):
        """Test getting all queues"""
        response = client.get(
            "/api/queues/all",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "queues" in response.json()
    
    def test_get_queue_status(self, auth_token):
        """Test getting specific queue status"""
        response = client.get(
            "/api/queues/status/food_a",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "status" in response.json()