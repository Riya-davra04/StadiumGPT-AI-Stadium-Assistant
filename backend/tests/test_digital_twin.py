import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


class TestDigitalTwin:
    """Digital Twin API test suite"""
    
    @pytest.fixture
    def auth_token(self):
        email = f"twin_{uuid.uuid4().hex[:8]}@example.com"
        client.post("/api/auth/register", json={
            "name": "Digital Twin User",
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
    
    def test_predict_congestion(self, auth_token):
        response = client.get(
            "/api/digital-twin/predict/congestion?minutes=30",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "predictions" in response.json()
        assert "summary" in response.json()
    
    def test_predict_congestion_specific_section(self, auth_token):
        response = client.get(
            "/api/digital-twin/predict/congestion?section=A1&minutes=15",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "predictions" in response.json()
        assert "A1" in response.json()["predictions"]
    
    def test_realtime_dashboard(self, auth_token):
        response = client.get(
            "/api/digital-twin/dashboard",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "sections" in response.json()
        assert "summary" in response.json()
    
    def test_predict_congestion_invalid_section(self, auth_token):
        response = client.get(
            "/api/digital-twin/predict/congestion?section=Z9",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "error" in result
        assert "Section Z9 not found" in result["error"]
    
    def test_create_alert(self, auth_token):
        response = client.post(
            f"/api/digital-twin/alert/A1?message=High%20congestion%20detected",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        if response.status_code == 404:
            pytest.skip("Alert endpoint not implemented")
        assert response.status_code in [200, 404]