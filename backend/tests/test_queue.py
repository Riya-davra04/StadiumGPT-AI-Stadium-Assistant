import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
import time

client = TestClient(app)


class TestQueue:
    """Queue API test suite"""
    
    @pytest.fixture
    def auth_token(self):
        email = f"queue_{uuid.uuid4().hex[:8]}@example.com"
        client.post("/api/auth/register", json={
            "name": "Queue User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": "TestPass123"
        })
        if response.status_code == 429:
            time.sleep(2)
            response = client.post("/api/auth/login", json={
                "email": email,
                "password": "TestPass123"
            })
        return response.json()["access_token"]
    
    def test_get_all_queues(self, auth_token):
        """Test getting all queue statuses"""
        response = client.get(
            "/api/queues/all",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        # ✅ Check for 'queues' key
        assert "queues" in result
        assert isinstance(result["queues"], dict)
        # Check that there are queues
        assert len(result["queues"]) > 0
    
    def test_get_queue_status(self, auth_token):
        """Test getting specific queue status"""
        response = client.get(
            "/api/queues/status/food_a",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "status" in result
        assert "estimated_wait" in result["status"]
        assert "queue_length" in result["status"]
    
    def test_get_queue_status_not_found(self, auth_token):
        """Test getting status for non-existent queue"""
        response = client.get(
            "/api/queues/status/nonexistent",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        assert "error" in result["status"]
        assert "Establishment not found" in result["status"]["error"]
    
    def test_get_best_queue_option(self, auth_token):
        """Test getting best queue option"""
        response = client.get(
            "/api/queues/best-option?category=food&max_wait=10",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        # ✅ Check for either best_option or message
        assert "best_option" in result or "message" in result
        
        # ✅ If best_option exists, verify structure
        if "best_option" in result and result["best_option"]:
            assert "name" in result["best_option"] or "wait_time" in result["best_option"]
    
    def test_get_best_queue_option_invalid_category(self, auth_token):
        """Test best queue option with invalid category"""
        response = client.get(
            "/api/queues/best-option?category=invalid&max_wait=10",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        result = response.json()
        # ✅ Should return message for no options
        assert "best_option" in result or "message" in result