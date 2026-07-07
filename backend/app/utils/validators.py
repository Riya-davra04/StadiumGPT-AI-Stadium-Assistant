"""
Validators Module
==================
Centralized validation functions for the application.
"""

import re
from typing import Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """Validate password strength."""
    if not password or len(password) < 8:
        return False
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    return has_upper and has_lower and has_digit


def validate_location(location: str) -> bool:
    """Validate location format."""
    if not location or len(location) < 2:
        return False
    return bool(re.match(r'^[a-zA-Z0-9\s\-_,.]+$', location))


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    if not phone:
        return False
    cleaned = re.sub(r'[\s\-()]', '', phone)
    return bool(re.match(r'^\+?[0-9]{10,15}$', cleaned))