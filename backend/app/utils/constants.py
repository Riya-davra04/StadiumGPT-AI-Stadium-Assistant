"""Constants used throughout the application"""

from enum import Enum
from typing import Dict, List

# API Configuration
class APIConfig:
    TITLE = "StadiumGPT - AI Smart Stadium Assistant"
    VERSION = "1.0.0"
    DESCRIPTION = "Revolutionary AI-powered stadium operations platform for FIFA World Cup"

# HTTP Status Codes
class HTTPStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNPROCESSABLE = 422
    INTERNAL_SERVER_ERROR = 500

# Response Messages
class Messages:
    USER_REGISTERED = "User registered successfully"
    USER_LOGGED_IN = "User logged in successfully"
    USER_LOGGED_OUT = "User logged out successfully"
    INVALID_CREDENTIALS = "Invalid credentials"
    USER_NOT_FOUND = "User not found"
    EMAIL_ALREADY_EXISTS = "Email already registered"
    EMERGENCY_REPORTED = "Emergency reported successfully"
    EMERGENCY_RESOLVED = "Emergency resolved successfully"

# Stadium Configuration
class StadiumConfig:
    NAME = "FIFA World Cup Stadium"
    CAPACITY = 80000
    TIMEZONE = "UTC"
    DEFAULT_LANGUAGE = "English"
    SUPPORTED_LANGUAGES: List[str] = ["English", "Hindi", "Spanish", "French", "Arabic", "Japanese"]

# Emergency Configuration
class EmergencyConfig:
    MEDICAL_CONTACT = "111"
    SECURITY_CONTACT = "112"
    FIRE_CONTACT = "113"
    GENERAL_EMERGENCY = "911"
    RESPONSE_TIME = 3  # minutes

# Queue Configuration
class QueueConfig:
    UPDATE_INTERVAL = 5  # seconds
    MAX_THRESHOLD = 50  # maximum queue length

# Crowd Configuration
class CrowdConfig:
    UPDATE_INTERVAL = 10  # seconds
    LOW_THRESHOLD = 0.3
    MEDIUM_THRESHOLD = 0.6
    HIGH_THRESHOLD = 0.8

# JWT Configuration
class JWTConfig:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 7

# Redis Configuration
class RedisConfig:
    TTL = 3600  # seconds
    MAX_SIZE = 10000
    SESSION_TTL = 86400  # 24 hours

# Rate Limiting
class RateLimitConfig:
    REQUESTS_PER_MINUTE = 60
    WINDOW_SECONDS = 60