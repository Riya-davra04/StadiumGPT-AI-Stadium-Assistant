import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

class TestAuth:
    """Authentication API tests"""
    
    def test_register_user(self):
        """Test user registration"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        response = client.post("/api/auth/register", json={
            "name": "Test User",
            "email": unique_email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["email"] == unique_email
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register first time
        client.post("/api/auth/register", json={
            "name": "Test User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        
        # Try to register again with same email
        response = client.post("/api/auth/register", json={
            "name": "Another User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        assert response.status_code == 400
        assert "already registered" in response.text.lower()
    
    def test_login_success(self, auth_token):
        """Test successful login - uses auth_token fixture"""
        # The fixture handles registration and login
        assert auth_token is not None
        assert len(auth_token) > 0
    
    def test_login_wrong_password(self, test_user):
        """Test login with wrong password"""
        # Register first
        client.post("/api/auth/register", json=test_user)
        
        # Login with wrong password
        response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "WrongPass123"
        })
        assert response.status_code == 401
    
    def test_get_current_user(self, auth_token):
        """Test getting current user"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "email" in response.json()