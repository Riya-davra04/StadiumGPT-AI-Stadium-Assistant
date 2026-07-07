"""
Security utilities for input sanitization.

JWT and password-hash helpers previously duplicated in this module have been
consolidated: use :mod:`app.utils.jwt_utils` for JWT and
:mod:`app.services.auth` for password hashing.
"""

from __future__ import annotations

import html
import re
from typing import Optional


class SecurityUtils:
    """Static helpers for sanitizing untrusted user input."""

    _EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize free-form user input (strips angle brackets, HTML-escapes, caps length)."""
        if not text:
            return ""
        sanitized = re.sub(r"[<>]", "", text)
        sanitized = html.escape(sanitized)
        return sanitized[:500]

    @staticmethod
    def sanitize_email(email: str) -> Optional[str]:
        """Return normalized lowercase email if it is well-formed, else ``None``."""
        if not email:
            return None
        normalized = email.strip().lower()
        return normalized if SecurityUtils._EMAIL_RE.match(normalized) else None

    @staticmethod
    def sanitize_location(location: str) -> str:
        """Sanitize a stadium location identifier."""
        if not location:
            return ""
        return re.sub(r"[^a-zA-Z0-9\s\-_.]", "", location)[:100]

    @staticmethod
    def sanitize_description(description: str) -> str:
        """Sanitize longer free-form text (emergency descriptions, etc.)."""
        if not description:
            return ""
        sanitized = re.sub(r"[<>]", "", description)
        sanitized = html.escape(sanitized)
        return sanitized[:1000]