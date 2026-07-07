from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict , Any
from datetime import datetime
from enum import Enum
import re


class UserRole(str, Enum):
    """User role types"""
    FAN = "fan"
    VOLUNTEER = "volunteer"
    STAFF = "staff"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class UserPreferences(BaseModel):
    """User preferences model"""
    language: str = "English"
    theme: str = "light"
    notifications: bool = True
    accessibility_mode: bool = False
    favorite_sections: List[str] = []
    preferred_food: List[str] = []


class User(BaseModel):
    """User model"""
    id: str = Field(..., description="Unique user ID")
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., description="User email address")
    role: UserRole = UserRole.FAN
    language: str = "English"
    preferences: UserPreferences = UserPreferences()
    accessibility_needs: Optional[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = False
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class UserCreate(BaseModel):
    """User creation model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.FAN
    language: str = "English"

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Invalid password')
        return v


class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    language: Optional[str] = None
    preferences: Optional[UserPreferences] = None
    accessibility_needs: Optional[List[str]] = None
    is_active: Optional[bool] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v


class UserResponse(BaseModel):
    """User response model"""
    id: str
    name: str
    email: EmailStr
    role: UserRole
    language: str
    preferences: UserPreferences
    accessibility_needs: Optional[List[str]]
    created_at: datetime
    last_active: datetime
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Authentication token model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class TokenData(BaseModel):
    """Token data model"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None