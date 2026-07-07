"""
Authentication Routes
======================
API endpoints for user authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any
from datetime import timedelta, datetime
import logging

from app.models.user import UserCreate, UserLogin, Token, UserResponse
from app.services.auth import AuthService
from app.utils.database import Database
from app.utils.validators import validate_email, validate_password
from app.utils.security import SecurityUtils

logger = logging.getLogger(__name__)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
auth_service = AuthService()
db = Database()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user_data: UserCreate) -> Dict[str, Any]:
    """
    Register a new user.
    
    Args:
        request: HTTP request
        user_data: User registration data
    
    Returns:
        Created user data
    """
    try:
        # Validate email
        if not validate_email(user_data.email):
            raise HTTPException(400, "Invalid email format")
        
        # Sanitize input
        user_data.name = SecurityUtils.sanitize_input(user_data.name)
        user_data.email = SecurityUtils.sanitize_email(user_data.email)
        
        # Check if user exists
        existing_user = await db.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(400, "Email already registered")
        
        user = await auth_service.register_user(user_data)
        logger.info(f"User registered: {user['email']}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(500, "Registration failed")


@router.post("/login", response_model=Token)
async def login_user(request: Request, login_data: UserLogin) -> Dict[str, Any]:
    """
    Login user and return access token.
    
    Args:
        request: HTTP request
        login_data: User login credentials
    
    Returns:
        JWT access token
    """
    try:
        user = await auth_service.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(401, "Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
        
        token = await auth_service.create_access_token(
            data={"sub": user["id"], "email": user["email"], "role": user["role"]},
            expires_delta=timedelta(hours=1)
        )
        
        logger.info(f"User logged in: {user['email']}")
        return {"access_token": token, "token_type": "bearer", "expires_in": 3600}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(500, "Login failed")


@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Logout user."""
    await auth_service.invalidate_token(token)
    return {"message": "Logged out", "timestamp": datetime.utcnow().isoformat()}


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get current user profile."""
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    
    user = await db.get_user_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/refresh")
async def refresh_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Refresh access token."""
    new_token = await auth_service.refresh_token(token)
    if not new_token:
        raise HTTPException(401, "Token refresh failed")
    return {"access_token": new_token, "token_type": "bearer", "expires_in": 3600}