"""Base service class for all services"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseService:
    """Base class for all services"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"{__name__}.{service_name}")
    
    def log_info(self, message: str, data: Optional[Dict] = None):
        """Log info message"""
        self.logger.info(f"[{self.service_name}] {message}", extra={"data": data})
    
    def log_error(self, message: str, error: Optional[Exception] = None):
        """Log error message"""
        self.logger.error(f"[{self.service_name}] {message}", exc_info=error)
    
    def log_warning(self, message: str, data: Optional[Dict] = None):
        """Log warning message"""
        self.logger.warning(f"[{self.service_name}] {message}", extra={"data": data})
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.utcnow().isoformat()
    
    def validate_input(self, data: Dict, required_fields: list) -> bool:
        """Validate required fields in input data"""
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        return True