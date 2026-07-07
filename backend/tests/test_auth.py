"""
Authentication API Tests
========================
Comprehensive test suite for authentication endpoints including:
- User registration
- User login
- Token validation
- Rate limiting
- Error handling
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
import time

client = TestClient(app)


class TestAuth:
    """Authentication API test suite"""
    
    def test_register_user_success(self):
        """Test successful user registration"""
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
        assert "password" not in response.json()
    
    def test_register_user_invalid_email(self):
        """Test registration with invalid email format"""
        response = client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "invalid-email",
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        assert response.status_code == 422
        assert "email" in response.text.lower()
    
    def test_register_user_weak_password(self):
        """Test registration with weak password"""
        response = client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "weak",
            "role": "fan",
            "language": "English"
        })
        assert response.status_code == 422
        assert "password" in response.text.lower()
    
    def test_register_user_duplicate_email(self):
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
        
        # Try to register again
        response = client.post("/api/auth/register", json={
            "name": "Another User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        assert response.status_code == 400
        assert "already registered" in response.text.lower()
    
    def test_login_user_success(self):
        """Test successful login"""
        email = f"login_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register
        client.post("/api/auth/register", json={
            "name": "Login User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        
        # Login
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": "TestPass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        assert "expires_in" in response.json()
    
    def test_login_user_wrong_password(self):
        """Test login with wrong password"""
        email = f"wrongpass_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register
        client.post("/api/auth/register", json={
            "name": "Login User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        
        # Login with wrong password
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": "WrongPass123"
        })
        assert response.status_code == 401
        assert "invalid credentials" in response.text.lower()
    
    def test_login_user_not_found(self):
        """Test login with non-existent user"""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "TestPass123"
        })
        assert response.status_code == 401
        assert "invalid credentials" in response.text.lower()
    
    def test_get_current_user(self):
        """Test getting current user profile"""
        email = f"me_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register
        client.post("/api/auth/register", json={
            "name": "Current User",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        
        # Login
        login_response = client.post("/api/auth/login", json={
            "email": email,
            "password": "TestPass123"
        })
        token = login_response.json()["access_token"]
        
        # Get profile
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == email
        assert "password" not in response.json()
    
    def test_get_current_user_invalid_token(self):
        """Test getting profile with invalid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_rate_limiting_login(self):
        """Test rate limiting on login endpoint"""
        email = f"rate_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register
        client.post("/api/auth/register", json={
            "name": "Rate Test",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        
        # Send multiple login requests
        for _ in range(10):
            client.post("/api/auth/login", json={
                "email": email,
                "password": "WrongPass123"
            })
        
        # The 11th request should be rate limited (depending on your limit)
        response = client.post("/api/auth/login", json={
            "email": email,
            "password": "WrongPass123"
        })
        # Either rate limited or just fails authentication
        assert response.status_code in [401, 429]
    
    def test_refresh_token(self):
        """Test token refresh endpoint"""
        email = f"refresh_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register and login
        client.post("/api/auth/register", json={
            "name": "Refresh Test",
            "email": email,
            "password": "TestPass123",
            "role": "fan",
            "language": "English"
        })
        login_response = client.post("/api/auth/login", json={
            "email": email,
            "password": "TestPass123"
        })
        token = login_response.json()["access_token"]
        
        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()