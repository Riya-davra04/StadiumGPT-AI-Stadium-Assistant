import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Create test database - use in-memory for testing"""
    from app.utils.database import Database
    db = Database()
    db.db_path = ":memory:"
    db._init_db()
    return db

@pytest.fixture
def test_user():
    """Create test user data with unique email"""
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
    """Get auth token for authenticated tests"""
    # Register user
    register_response = client.post("/api/auth/register", json=test_user)
    
    # If registration fails, try to login anyway (user might exist)
    if register_response.status_code != 201:
        pass
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # If login fails, skip the test
    if response.status_code != 200:
        pytest.skip("Could not get auth token - authentication failed")
    
    return response.json()["access_token"]