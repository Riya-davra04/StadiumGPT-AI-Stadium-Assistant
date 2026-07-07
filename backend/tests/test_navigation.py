import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestNavigation:
    """Navigation API tests"""
    
    @pytest.fixture
    def auth_token(self):
        client.post("/api/auth/register", json={
            "name": "Nav User",
            "email": "nav@example.com",
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": "nav@example.com",
            "password": "TestPass123"
        })
        return response.json()["access_token"]
    
    def test_get_route(self, auth_token):
        """Test getting a route"""
        response = client.get(
            "/api/navigation/route?start=GateA&end=SectionB",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "route" in response.json()
    
    def test_get_nearby_locations(self, auth_token):
        """Test getting nearby locations"""
        response = client.get(
            "/api/navigation/nearby?location=GateA&radius=50",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "facilities" in response.json()