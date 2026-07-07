# Backend package initialization
__version__ = "1.0.0"
__author__ = "StadiumGPT Team"

from app.main import app
from app.services import GeminiService

# Don't import RAGService

__all__ = [
    "app",
    "GeminiService"
]