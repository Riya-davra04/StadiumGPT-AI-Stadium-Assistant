import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


class TestMonitoring:
    @pytest.fixture
    def auth_token(self):
        email = f"monitor_{uuid.uuid4().hex[:8]}@example.com"
        client.post("/api/auth/register", json={
            "name": "Monitor User",
            "email": email,
            "password": "TestPass123",
            "role": "organizer",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": "TestPass123"
        })
        return response.json()["access_token"]
    
    def test_get_metrics(self, auth_token):
        response = client.get(
            "/api/monitoring/metrics",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "temperature" in response.json()
        assert "fan_satisfaction" in response.json()
    
    def test_get_sections(self, auth_token):
        response = client.get(
            "/api/monitoring/sections",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "A1" in response.json()
    
    def test_create_alert(self, auth_token):
        response = client.post(
            "/api/monitoring/alert/A1?message=Test%20alert",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "section" in response.json()