import re
from typing import Optional, List
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email:
        return False
    
    # Basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """Validate password strength"""
    if not password or len(password) < 8:
        return False
    
    # Check for at least one uppercase, one lowercase, one digit
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    return has_upper and has_lower and has_digit and has_special


def validate_location(location: str) -> bool:
    """Validate location format"""
    if not location or len(location) < 2:
        return False
    
    # Location should be at least 2 characters and contain valid characters
    return bool(re.match(r'^[a-zA-Z0-9\s\-_,.]+$', location))


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return False
    
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-()]', '', phone)
    
    # Check if it's a valid phone number (US/International)
    return bool(re.match(r'^\+?[0-9]{10,15}$', cleaned))


def validate_section(section: str) -> bool:
    """Validate section format"""
    if not section:
        return False
    
    # Section format: A1, B2, C3, etc.
    return bool(re.match(r'^[A-Z]\d+$', section))


def validate_gate(gate: str) -> bool:
    """Validate gate format"""
    if not gate:
        return False
    
    # Gate format: A, B, C, D, E
    return bool(re.match(r'^[A-E]$', gate))


def validate_language(language: str) -> bool:
    """Validate language format"""
    if not language:
        return False
    
    languages = ['English', 'Hindi', 'Spanish', 'French', 'Arabic', 'Japanese', 'German', 'Chinese']
    return language in languages


def validate_timestamp(timestamp: str) -> bool:
    """Validate timestamp format"""
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def validate_coordinates(lat: float, lng: float) -> bool:
    """Validate GPS coordinates"""
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lng <= 180):
        return False
    return True


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>]', '', text)
    sanitized = sanitized.strip()
    
    return sanitized[:500]  # Limit length


def validate_queue_length(length: int) -> bool:
    """Validate queue length"""
    return 0 <= length <= 1000


def validate_density(density: float) -> bool:
    """Validate density value"""
    return 0 <= density <= 1


def validate_severity(severity: str) -> bool:
    """Validate severity level"""
    return severity in ['low', 'medium', 'high', 'critical']


def validate_emergency_type(emergency_type: str) -> bool:
    """Validate emergency type"""
    types = ['medical', 'fire', 'security', 'crowd', 'natural', 'terror', 'infrastructure']
    return emergency_type in types


def validate_role(role: str) -> bool:
    """Validate user role"""
    roles = ['fan', 'volunteer', 'staff', 'organizer', 'admin']
    return role in roles


def validate_preferences(preferences: dict) -> bool:
    """Validate user preferences"""
    valid_keys = ['language', 'theme', 'notifications', 'accessibility_mode']
    for key in preferences:
        if key not in valid_keys:
            return False
    return True