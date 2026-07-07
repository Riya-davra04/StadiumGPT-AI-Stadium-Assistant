"""
Authentication Service
=======================
Handles user authentication, registration, and token management.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import bcrypt
import uuid
import json
import logging

from app.models.user import UserCreate
from app.utils.database import Database
from app.utils.jwt_utils import create_access_token, verify_token

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user management."""
    
    def __init__(self) -> None:
        """Initialize authentication service."""
        self.db = Database()
    
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
        
        Returns:
            User data without password hash
        """
        try:
            hashed_password = self._hash_password(user_data.password)
            
            user_dict = {
                "id": str(uuid.uuid4()),
                "name": user_data.name,
                "email": user_data.email,
                "password_hash": hashed_password,
                "role": user_data.role.value,
                "language": user_data.language,
                "preferences": {},
                "accessibility_needs": [],
                "created_at": datetime.utcnow().isoformat(),
                "last_active": datetime.utcnow().isoformat(),
                "is_verified": 0,
                "is_active": 1
            }
            
            await self.db.create_user(user_dict)
            user_dict.pop("password_hash", None)
            return user_dict
        except Exception as e:
            logger.error(f"Register user error: {e}")
            raise
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User's email
            password: User's password
        
        Returns:
            User data if authenticated, None otherwise
        """
        try:
            user = await self.db.get_user_by_email(email)
            if not user:
                return None
            
            if not self._verify_password(password, user.get("password_hash")):
                return None
            
            user.pop("password_hash", None)
            return user
        except Exception as e:
            logger.error(f"Authenticate user error: {e}")
            return None
    
    async def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create access token using centralized utility."""
        return create_access_token(data, expires_delta)
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify token using centralized utility."""
        return verify_token(token)
    
    async def invalidate_token(self, token: str) -> bool:
        """Invalidate a token (logout)."""
        return True
    
    async def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an existing token."""
        payload = await self.verify_token(token)
        if not payload:
            return None
        
        return create_access_token(
            data={"sub": payload.get("sub"), "email": payload.get("email"), "role": payload.get("role")},
            expires_delta=timedelta(hours=1)
        )
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = await self.db.get_user_by_id(user_id)
        if not user:
            return False
        
        if not self._verify_password(current_password, user.get("password_hash")):
            return False
        
        new_hash = self._hash_password(new_password)
        await self.db.update_user(user_id, {"password_hash": new_hash})
        return True
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        if not password or not hashed:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False