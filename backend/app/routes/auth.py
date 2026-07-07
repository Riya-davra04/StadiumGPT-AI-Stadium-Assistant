"""
Authentication Routes
======================
API endpoints for user authentication.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.models.user import Token, UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService
from app.utils.database import Database
from app.utils.security import SecurityUtils
from app.utils.validators import validate_email

logger = logging.getLogger(__name__)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
auth_service = AuthService()
db = Database()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(request: Request, user_data: UserCreate) -> Dict[str, Any]:
    """Register a new user account.

    Pydantic already enforces email format and password strength (see
    :class:`app.models.user.UserCreate`); this route adds sanitization and
    uniqueness checks.
    """
    if not validate_email(user_data.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid email format")

    user_data.name = SecurityUtils.sanitize_input(user_data.name)
    sanitized_email = SecurityUtils.sanitize_email(user_data.email)
    if not sanitized_email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid email format")
    user_data.email = sanitized_email

    if await db.get_user_by_email(user_data.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    try:
        user = await auth_service.register_user(user_data)
    except Exception as exc:
        logger.exception("Registration failed for %s: %s", user_data.email, exc)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Registration failed") from exc

    logger.info("User registered: %s", user["email"])
    return user


@router.post("/login", response_model=Token, summary="Login and receive an access token")
async def login_user(request: Request, login_data: UserLogin) -> Dict[str, Any]:
    """Authenticate a user and return a short-lived JWT."""
    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = await auth_service.create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"]},
        expires_delta=timedelta(hours=1),
    )
    logger.info("User logged in: %s", user["email"])
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


@router.post("/logout", summary="Logout the current user")
async def logout_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Logout endpoint (JWTs are stateless; clients should discard the token)."""
    await auth_service.invalidate_token(token)
    return {"message": "Logged out", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Return the profile of the authenticated user."""
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user = await db.get_user_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    user.pop("password_hash", None)
    return user


@router.post("/refresh", summary="Refresh the access token")
async def refresh_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Issue a fresh access token given a still-valid existing token."""
    new_token = await auth_service.refresh_token(token)
    if not new_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token refresh failed")
    return {"access_token": new_token, "token_type": "bearer", "expires_in": 3600}