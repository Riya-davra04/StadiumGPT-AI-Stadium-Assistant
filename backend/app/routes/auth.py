from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any
from datetime import datetime, timedelta
import logging
import uuid

from app.models.user import User, UserCreate, UserLogin, Token, UserResponse
from app.services.auth import AuthService
from app.utils.database import Database
from app.utils.validators import validate_email, validate_password
from app.utils.security import SecurityUtils

logger = logging.getLogger(__name__)
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Initialize services
auth_service = AuthService()
db = Database()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user_data: UserCreate) -> Dict[str, Any]:
    """
    Register a new user
    """
    try:
        # Validate email
        if not validate_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Sanitize input
        user_data.name = SecurityUtils.sanitize_input(user_data.name)
        user_data.email = SecurityUtils.sanitize_email(user_data.email)
        
        # Check if user exists
        existing_user = await db.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with dictionary
        user_dict = {
            "id": str(uuid.uuid4()),
            "name": user_data.name,
            "email": user_data.email,
            "password_hash": auth_service._hash_password(user_data.password),
            "role": user_data.role.value,
            "language": user_data.language,
            "preferences": {},  # ✅ Dictionary
            "accessibility_needs": [],  # ✅ List
            "created_at": datetime.utcnow().isoformat(),
            "last_active": datetime.utcnow().isoformat(),
            "is_verified": 0,
            "is_active": 1
        }
        
        # Save to database
        await db.create_user(user_dict)
        
        logger.info(f"User registered: {user_data.email}")
        
        # Return user without password
        user_dict.pop("password_hash", None)
        return user_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
async def login_user(request: Request, login_data: UserLogin) -> Dict[str, Any]:
    """
    Login user and return access token
    """
    try:
        # Authenticate user
        user = await auth_service.authenticate_user(
            login_data.email,
            login_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Generate token
        token = await auth_service.create_access_token(
            data={"sub": user["id"], "email": user["email"], "role": user["role"]},
            expires_delta=timedelta(hours=1)
        )
        
        logger.info(f"User logged in: {user['email']}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 3600
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Logout user"""
    try:
        await auth_service.invalidate_token(token)
        logger.info("User logged out")
        return {
            "message": "Logged out successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get current user information"""
    try:
        payload = await auth_service.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user = await db.get_user_by_id(payload.get("sub"))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


@router.post("/refresh")
async def refresh_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Refresh access token"""
    try:
        new_token = await auth_service.refresh_token(token)
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": 3600
        }
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.put("/update-profile")
async def update_profile(
    user_data: Dict[str, Any],
    token: str = Depends(oauth2_scheme)
) -> Dict[str, Any]:
    """Update user profile"""
    try:
        payload = await auth_service.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = await db.update_user(payload.get("sub"), user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User profile updated: {user['email']}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    token: str = Depends(oauth2_scheme)
) -> Dict[str, Any]:
    """Change user password"""
    try:
        payload = await auth_service.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        result = await auth_service.change_password(
            payload.get("sub"),
            current_password,
            new_password
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password change failed"
            )
        
        logger.info(f"Password changed for user: {payload.get('email')}")
        
        return {
            "message": "Password changed successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Change password error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )