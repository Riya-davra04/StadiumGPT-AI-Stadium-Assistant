"""Security utilities for input sanitization and validation"""

import re
import html
from typing import Optional
import bcrypt
from datetime import datetime, timedelta
import jwt
import os

class SecurityUtils:
    """Security utilities for sanitizing user input"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        if not text:
            return ""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>]', '', text)
        # Escape HTML entities
        sanitized = html.escape(sanitized)
        # Limit length to prevent abuse
        return sanitized[:500]
    
    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        """Sanitize and validate email"""
        if not email:
            return None
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return email
        return None
    
    @staticmethod
    def sanitize_location(location: str) -> str:
        """Sanitize location input"""
        if not location:
            return ""
        return re.sub(r'[^a-zA-Z0-9\s\-_.]', '', location)[:100]
    
    @staticmethod
    def sanitize_description(description: str) -> str:
        """Sanitize description/emergency text"""
        if not description:
            return ""
        sanitized = re.sub(r'[<>]', '', description)
        sanitized = html.escape(sanitized)
        return sanitized[:1000]
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        if not password or not hashed:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    @staticmethod
    def create_jwt_token(data: dict, secret: str, expires_in: int = 3600) -> str:
        """Create JWT token with expiration"""
        payload = data.copy()
        payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
        return jwt.encode(payload, secret, algorithm='HS256')
    
    @staticmethod
    def verify_jwt_token(token: str, secret: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            return jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None