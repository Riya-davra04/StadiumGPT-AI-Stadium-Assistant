"""
JWT Utilities Module
====================
Centralized JWT token handling for authentication.

Fails fast in non-development environments if ``JWT_SECRET_KEY`` is missing
or is the insecure default.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt

logger = logging.getLogger(__name__)

_INSECURE_DEFAULT = "your-secret-key-change-this"
JWT_SECRET = os.getenv("JWT_SECRET_KEY", _INSECURE_DEFAULT)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if JWT_SECRET == _INSECURE_DEFAULT and os.getenv("ENVIRONMENT", "development") == "production":
    raise RuntimeError(
        "JWT_SECRET_KEY must be set to a strong value in production "
        "(generate one with `openssl rand -hex 32`)."
    )


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT access token.

    Args:
        data: Claim payload (sub, email, role etc.)
        expires_delta: Optional TTL override.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT.

    Returns:
        The decoded payload, or ``None`` if the token is invalid/expired.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError as exc:
        logger.warning("Invalid token: %s", exc)
        return None