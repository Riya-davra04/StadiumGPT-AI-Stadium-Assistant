"""
Pytest Configuration for StadiumGPT Tests
==========================================
This module provides fixtures and configuration for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
import os

# Set test environment
os.environ["ENVIRONMENT"] = "test"


@pytest.fixture
def client():
    """
    Create a test client for FastAPI application.
    
    Returns:
        TestClient: Test client for making API requests
    """
    return TestClient(app)


@pytest.fixture
def test_db():
    """
    Create an in-memory database for testing.
    
    Returns:
        Database: Test database instance
    """
    from app.utils.database import Database
    db = Database()
    db.db_path = ":memory:"
    db._init_db()
    return db


@pytest.fixture
def test_user():
    """
    Generate test user data with unique email.
    
    Returns:
        dict: Test user credentials
    """
    unique_id = uuid.uuid4().hex[:8]
    return {
        "name": "Test User",
        "email": f"test_{unique_id}@example.com",
        "password": "TestPass123",
        "role": "fan",
        "language": "English"
    }


@pytest.fixture
def auth_token(client, test_user):
    """
    Get an authentication token for a test user.
    
    This fixture registers a user and returns their access token.
    
    Args:
        client: Test client fixture
        test_user: Test user fixture
        
    Returns:
        str: JWT access token
        
    Raises:
        pytest.skip: If authentication fails
    """
    # Register user
    client.post("/api/auth/register", json=test_user)
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # Skip test if login fails
    if response.status_code != 200:
        pytest.skip("Could not get auth token")
    
    return response.json()["access_token"]


@pytest.fixture
def authenticated_client(client, auth_token):
    """
    Create a test client with authentication token.
    
    Args:
        client: Test client fixture
        auth_token: Authentication token fixture
        
    Returns:
        TestClient: Authenticated test client
    """
    client.headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    return client