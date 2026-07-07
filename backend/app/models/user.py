from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import re


class UserRole(str, Enum):
    """User role types for the stadium management system"""
    FAN = "fan"
    VOLUNTEER = "volunteer"
    STAFF = "staff"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class UserPreferences(BaseModel):
    """User preferences model for personalization"""
    language: str = Field(default="English", description="Preferred language")
    theme: str = Field(default="light", description="UI theme preference")
    notifications: bool = Field(default=True, description="Enable notifications")
    accessibility_mode: bool = Field(default=False, description="Enable accessibility features")
    favorite_sections: List[str] = Field(default=[], description="Preferred stadium sections")
    preferred_food: List[str] = Field(default=[], description="Favorite food choices")


class User(BaseModel):
    """
    User model representing all system users.
    
    Attributes:
        id: Unique identifier
        name: Full name (2-100 chars)
        email: Valid email address
        role: User role (fan, volunteer, staff, organizer, admin)
        language: Preferred language
        preferences: User preferences
        accessibility_needs: List of accessibility requirements
        created_at: Account creation timestamp
        last_active: Last activity timestamp
        is_verified: Email verification status
        is_active: Account active status
        metadata: Additional user data
    """
    id: str = Field(..., description="Unique user ID")
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="User email address")
    role: UserRole = Field(default=UserRole.FAN, description="User role")
    language: str = Field(default="English", description="Preferred language")
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    accessibility_needs: Optional[List[str]] = Field(default=[], description="Accessibility requirements")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = Field(default=False, description="Email verified")
    is_active: bool = Field(default=True, description="Account active")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and sanitize user name"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserCreate(BaseModel):
    """User creation request model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = Field(default=UserRole.FAN)
    language: str = Field(default="English")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength.
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        """
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
    """User login request model"""
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or len(v) < 8:
            raise ValueError('Invalid password')
        return v


class UserUpdate(BaseModel):
    """User profile update model"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    language: Optional[str] = None
    preferences: Optional[UserPreferences] = None
    accessibility_needs: Optional[List[str]] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """User response model for API responses"""
    id: str
    name: str
    email: EmailStr
    role: UserRole
    language: str
    preferences: UserPreferences = UserPreferences()
    accessibility_needs: Optional[List[str]] = []
    created_at: datetime
    last_active: datetime
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Authentication token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class TokenData(BaseModel):
    """Token payload model"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None