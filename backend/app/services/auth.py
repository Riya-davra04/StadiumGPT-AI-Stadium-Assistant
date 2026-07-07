"""
Authentication Service
=======================
Handles user registration, credential verification, token lifecycle and a
simple in-memory brute-force lockout (per email).
"""

from __future__ import annotations

import logging
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

import bcrypt

from app.models.user import UserCreate
from app.utils.database import Database
from app.utils.jwt_utils import create_access_token, verify_token

logger = logging.getLogger(__name__)

# Brute force lockout: N failures within WINDOW seconds -> lock for LOCKOUT seconds.
_MAX_FAILURES = 5
_WINDOW_SECONDS = 300
_LOCKOUT_SECONDS = 900


class AuthService:
    """Authentication service for user management."""

    def __init__(self) -> None:
        self.db = Database()
        # email -> (failure_timestamps: list[float], locked_until: float)
        self._failures: Dict[str, Tuple[list, float]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Persist a new user (password stored as bcrypt hash)."""
        now_iso = datetime.now(timezone.utc).isoformat()
        user_dict = {
            "id": str(uuid.uuid4()),
            "name": user_data.name,
            "email": user_data.email,
            "password_hash": self._hash_password(user_data.password),
            "role": user_data.role.value,
            "language": user_data.language,
            "preferences": {},
            "accessibility_needs": [],
            "created_at": now_iso,
            "last_active": now_iso,
            "is_verified": 0,
            "is_active": 1,
        }
        await self.db.create_user(user_dict)
        user_dict.pop("password_hash", None)
        return user_dict

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify credentials with brute-force protection and constant-time compare."""
        if self._is_locked(email):
            logger.warning("Login attempt on locked account: %s", email)
            return None

        user = await self.db.get_user_by_email(email)
        if not user or not self._verify_password(password, user.get("password_hash", "")):
            self._record_failure(email)
            return None

        self._clear_failures(email)
        user.pop("password_hash", None)
        return user

    async def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        return create_access_token(data, expires_delta)

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        return verify_token(token)

    async def invalidate_token(self, token: str) -> bool:
        """Stateless JWTs cannot be revoked without a blocklist – return True as no-op."""
        return True

    async def refresh_token(self, token: str) -> Optional[str]:
        payload = await self.verify_token(token)
        if not payload:
            return None
        return create_access_token(
            data={
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role"),
            },
            expires_delta=timedelta(hours=1),
        )

    async def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:
        user = await self.db.get_user_by_id(user_id)
        if not user or not self._verify_password(current_password, user.get("password_hash", "")):
            return False
        await self.db.update_user(user_id, {"password_hash": self._hash_password(new_password)})
        return True

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _verify_password(password: str, hashed: str) -> bool:
        if not password or not hashed:
            # Constant-time dummy check to reduce user-enumeration timing signal.
            bcrypt.checkpw(b"dummy", bcrypt.hashpw(b"dummy", bcrypt.gensalt()))
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except (ValueError, TypeError) as exc:
            logger.warning("Password verify failed: %s", exc)
            return False

    def _is_locked(self, email: str) -> bool:
        entry = self._failures.get(email)
        return bool(entry and entry[1] > time.time())

    def _record_failure(self, email: str) -> None:
        now = time.time()
        failures, _ = self._failures.get(email, ([], 0.0))
        failures = [t for t in failures if now - t < _WINDOW_SECONDS]
        failures.append(now)
        locked_until = now + _LOCKOUT_SECONDS if len(failures) >= _MAX_FAILURES else 0.0
        self._failures[email] = (failures, locked_until)
        # Small jitter to smooth timing across code paths.
        time.sleep(secrets.randbelow(20) / 1000.0)

    def _clear_failures(self, email: str) -> None:
        self._failures.pop(email, None)