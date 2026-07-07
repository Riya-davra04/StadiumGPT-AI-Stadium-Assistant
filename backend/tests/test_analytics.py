import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


class TestAnalytics:
    @pytest.fixture
    def auth_token(self):
        email = f"analytics_{uuid.uuid4().hex[:8]}@example.com"
        client.post("/api/auth/register", json={
            "name": "Analytics User",
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
    
    def test_analytics_crowd(self, auth_token):
        response = client.post(
            "/api/analytics/crowd",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"density": {"A1": 0.8, "B1": 0.3, "C1": 0.5}}
        )
        assert response.status_code == 200
        assert "average_density" in response.json()
        assert "crowd_level" in response.json()