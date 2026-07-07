"""
Health Check Tests
==================
Test suite for the health check endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealth:
    """Health check test suite"""
    
    def test_health_check_success(self):
        """Test health check endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert "services" in response.json()
        assert "database" in response.json()["services"]
        assert "gemini" in response.json()["services"]
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["name"] == "StadiumGPT"
        assert "endpoints" in response.json()
        assert "docs" in response.json()["endpoints"]
        assert "health" in response.json()["endpoints"]
    
    def test_health_check_services(self):
        """Test health check shows service statuses"""
        response = client.get("/health")
        assert response.status_code == 200
        services = response.json()["services"]
        assert isinstance(services["database"], bool)
        assert isinstance(services["gemini"], bool)
        assert isinstance(services["websocket"], int)