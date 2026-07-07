import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCrowd:
    """Crowd API tests"""
    
    @pytest.fixture
    def auth_token(self):
        client.post("/api/auth/register", json={
            "name": "Crowd User",
            "email": "crowd@example.com",
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": "crowd@example.com",
            "password": "TestPass123"
        })
        return response.json()["access_token"]
    
    def test_get_heatmap(self, auth_token):
        """Test getting crowd heatmap"""
        response = client.get(
            "/api/crowds/heatmap",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "heatmap" in response.json()
    
    def test_get_crowd_status(self, auth_token):
        """Test getting crowd status"""
        response = client.get(
            "/api/crowds/status",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "status" in response.json()