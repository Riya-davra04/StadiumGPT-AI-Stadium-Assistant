"""Base service class with structured logging helpers."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseService:
    """Common base for service classes (logging, timestamps, validation)."""

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name
        self.logger = logging.getLogger(f"{__name__}.{service_name}")

    def log_info(self, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        self.logger.info("[%s] %s", self.service_name, message, extra={"data": data})

    def log_error(self, message: str, error: Optional[BaseException] = None) -> None:
        self.logger.error("[%s] %s", self.service_name, message, exc_info=error)

    def log_warning(self, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        self.logger.warning("[%s] %s", self.service_name, message, extra={"data": data})

    @staticmethod
    def get_timestamp() -> str:
        """Return a timezone-aware UTC ISO-8601 timestamp."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def validate_input(data: Dict[str, Any], required_fields: List[str]) -> bool:
        return all(field in data and data[field] is not None for field in required_fields)