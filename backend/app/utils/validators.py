"""
Validators Module
==================
Centralized validation functions for the application.
"""

from __future__ import annotations

import re
from typing import Final

_EMAIL_RE: Final = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
_LOCATION_RE: Final = re.compile(r"^[a-zA-Z0-9\s\-_,.]+$")
_PHONE_RE: Final = re.compile(r"^\+?[0-9]{10,15}$")


def validate_email(email: str) -> bool:
    """Return ``True`` if the email is well-formed."""
    if not email:
        return False
    return bool(_EMAIL_RE.match(email))


def validate_password(password: str) -> bool:
    """Return ``True`` if the password satisfies the minimum strength policy.

    Policy: ≥ 8 chars, at least one uppercase, one lowercase, one digit.
    """
    if not password or len(password) < 8:
        return False
    return (
        bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[a-z]", password))
        and bool(re.search(r"\d", password))
    )


def validate_location(location: str) -> bool:
    """Return ``True`` if the location string uses only allowed characters."""
    if not location or len(location) < 2:
        return False
    return bool(_LOCATION_RE.match(location))


def validate_phone(phone: str) -> bool:
    """Return ``True`` if the phone number matches an E.164-like format."""
    if not phone:
        return False
    cleaned = re.sub(r"[\s\-()]", "", phone)
    return bool(_PHONE_RE.match(cleaned))