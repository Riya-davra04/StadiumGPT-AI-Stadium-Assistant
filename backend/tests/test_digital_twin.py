"""
Digital Twin Tests
==================
Test suite for the digital twin simulation and prediction features.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


class TestDigitalTwin:
    """Digital Twin API test suite"""
    
    @pytest.fixture
    def auth_token(self):
        """Get auth token for tests"""
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
    
    def test_get_simulation_status(self, auth_token):
        """Test getting simulation status"""
        response = client.get(
            "/api/digital-twin/status",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "running" in response.json()
        assert "sections_count" in response.json()
    
    def test_predict_crowd(self, auth_token):
        """Test crowd prediction"""
        response = client.get(
            "/api/digital-twin/predict/crowd?minutes=15",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "predictions" in response.json()
        assert "summary" in response.json()
        assert "critical_sections" in response.json()["summary"]
    
    def test_get_heatmap(self, auth_token):
        """Test getting heatmap data"""
        response = client.get(
            "/api/digital-twin/heatmap",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "data" in response.json()
        assert "legend" in response.json()
    
    def test_get_section_status(self, auth_token):
        """Test getting section status"""
        response = client.get(
            "/api/digital-twin/section/A1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "section" in response.json()
        assert "density" in response.json()
    
    def test_start_simulation(self, auth_token):
        """Test starting simulation"""
        response = client.post(
            "/api/digital-twin/simulation/start",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "simulation_started" in response.json()["status"]
    
    def test_stop_simulation(self, auth_token):
        """Test stopping simulation"""
        response = client.post(
            "/api/digital-twin/simulation/stop",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "simulation_stopped" in response.json()["status"]