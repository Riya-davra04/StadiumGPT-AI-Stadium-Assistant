"""Unit tests for :mod:`app.utils.validators`."""

import pytest

from app.utils.validators import (
    validate_email,
    validate_location,
    validate_password,
    validate_phone,
)


class TestValidateEmail:
    """Email format validation."""

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "user.name+tag@sub.example.co",
            "u1234@x.io",
        ],
    )
    def test_valid_email(self, email: str) -> None:
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "",
            "no-at-sign",
            "@missing.local",
            "missing@tld",
            "space in@name.com",
        ],
    )
    def test_invalid_email(self, email: str) -> None:
        assert validate_email(email) is False


class TestValidatePassword:
    """Password strength policy."""

    def test_meets_all_rules(self) -> None:
        assert validate_password("Strong1Pass") is True

    @pytest.mark.parametrize(
        "password",
        ["", "short1A", "alllowercase1", "ALLUPPERCASE1", "NoDigitsHere"],
    )
    def test_fails_policy(self, password: str) -> None:
        assert validate_password(password) is False


class TestValidateLocation:
    def test_accepts_common_names(self) -> None:
        assert validate_location("Gate A-1, Section 3") is True

    @pytest.mark.parametrize("value", ["", "X", "gate<script>"])
    def test_rejects_invalid(self, value: str) -> None:
        assert validate_location(value) is False


class TestValidatePhone:
    @pytest.mark.parametrize("phone", ["+911234567890", "9876543210", "+1 (415) 555-1212"])
    def test_valid(self, phone: str) -> None:
        assert validate_phone(phone) is True

    @pytest.mark.parametrize("phone", ["", "abc", "12345"])
    def test_invalid(self, phone: str) -> None:
        assert validate_phone(phone) is False