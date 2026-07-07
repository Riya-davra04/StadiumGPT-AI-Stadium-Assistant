"""Unit tests for :mod:`app.utils.security` and :mod:`app.utils.jwt_utils`."""

from datetime import timedelta

import pytest

from app.utils.jwt_utils import create_access_token, verify_token
from app.utils.security import SecurityUtils


class TestSanitizers:
    """Input sanitization helpers."""

    def test_strips_angle_brackets_and_escapes(self) -> None:
        result = SecurityUtils.sanitize_input("<script>alert('x')</script>")
        assert "<" not in result
        assert ">" not in result
        assert "&#x27;" in result or "'" not in result

    def test_returns_empty_for_none_like(self) -> None:
        assert SecurityUtils.sanitize_input("") == ""
        assert SecurityUtils.sanitize_description("") == ""

    def test_caps_length(self) -> None:
        assert len(SecurityUtils.sanitize_input("a" * 5000)) == 500
        assert len(SecurityUtils.sanitize_description("a" * 5000)) == 1000

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("User@Example.COM", "user@example.com"),
            ("  user@example.com  ", "user@example.com"),
            ("bad-email", None),
            ("", None),
        ],
    )
    def test_email(self, email: str, expected) -> None:
        assert SecurityUtils.sanitize_email(email) == expected

    def test_location(self) -> None:
        assert SecurityUtils.sanitize_location("Gate-A_1") == "Gate-A_1"
        assert "<" not in SecurityUtils.sanitize_location("Gate<A>")


class TestJWT:
    """JWT round-trip and expiry behaviour."""

    def test_round_trip(self) -> None:
        token = create_access_token({"sub": "user-1", "role": "fan"})
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "user-1"
        assert payload["role"] == "fan"
        assert "exp" in payload

    def test_expired_token_returns_none(self) -> None:
        token = create_access_token({"sub": "u"}, expires_delta=timedelta(seconds=-1))
        assert verify_token(token) is None

    def test_invalid_token_returns_none(self) -> None:
        assert verify_token("not-a-jwt") is None