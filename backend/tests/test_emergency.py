import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestEmergency:
    """Emergency API tests"""
    
    @pytest.fixture
    def auth_token(self):
        client.post("/api/auth/register", json={
            "name": "Emergency User",
            "email": "emergency@example.com",
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": "emergency@example.com",
            "password": "TestPass123"
        })
        return response.json()["access_token"]
    
    def test_report_emergency(self, auth_token):
        """Test reporting an emergency"""
        response = client.post(
            "/api/emergency/report",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "type": "medical",
                "location": "Section A",
                "description": "Someone fainted",
                "severity": "medium"
            }
        )
        assert response.status_code == 200
        assert "alert" in response.json()
    
    def test_get_active_emergencies(self, auth_token):
        """Test getting active emergencies"""
        response = client.get(
            "/api/emergency/active",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "alerts" in response.json()