from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
import uuid
import os
import logging
from passlib.context import CryptContext

from app.models.user import UserCreate, User
from app.utils.database import Database

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.db = Database()
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60
    
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Hash password
            hashed_password = self._hash_password(user_data.password)
            
            # Create user
            user_dict = {
                "id": str(uuid.uuid4()),
                "name": user_data.name,
                "email": user_data.email,
                "password_hash": hashed_password,
                "role": user_data.role.value,
                "language": user_data.language,
                "preferences": {},
                "created_at": datetime.utcnow().isoformat(),
                "last_active": datetime.utcnow().isoformat(),
                "is_verified": False,
                "is_active": True
            }
            
            # Save to database
            await self.db.create_user(user_dict)
            
            # Return user without password
            user_dict.pop("password_hash", None)
            return user_dict
            
        except Exception as e:
            logger.error(f"Register user error: {e}")
            raise
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        try:
            # Get user from database
            user = await self.db.get_user_by_email(email)
            if not user:
                return None
            
            # Verify password
            if not self._verify_password(password, user.get("password_hash")):
                return None
            
            # Return user without password
            user.pop("password_hash", None)
            return user
            
        except Exception as e:
            logger.error(f"Authenticate user error: {e}")
            return None
    
    async def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Create token error: {e}")
            raise
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    async def invalidate_token(self, token: str) -> bool:
        """Invalidate a token (for logout)"""
        # In a real implementation, you'd add the token to a blacklist
        # For now, just return True
        return True
    
    async def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an existing token"""
        try:
            payload = await self.verify_token(token)
            if not payload:
                return None
            
            # Create new token with extended expiry
            new_token = await self.create_access_token(
                data={"sub": payload.get("sub"), "email": payload.get("email"), "role": payload.get("role")},
                expires_delta=timedelta(hours=1)
            )
            return new_token
            
        except Exception as e:
            logger.error(f"Refresh token error: {e}")
            return None
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Get user
            user = await self.db.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verify current password
            if not self._verify_password(current_password, user.get("password_hash")):
                return False
            
            # Hash new password
            new_hash = self._hash_password(new_password)
            
            # Update user
            await self.db.update_user(user_id, {"password_hash": new_hash})
            return True
            
        except Exception as e:
            logger.error(f"Change password error: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        if not password or not hashed_password:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except:
            return False