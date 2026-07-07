# Dummy RAGService (since faiss is not installed)
class RAGService:
    def __init__(self):
        pass
    async def retrieve(self, query, top_k=3):
        return []
    async def get_context(self, query):
        return {"context": {}, "query": query}

from app.services.gemini_service import GeminiService
from app.services.navigation import NavigationService
from app.services.crowd_management import CrowdManagementService
from app.services.queue_management import QueueManagementService
from app.services.emergency import EmergencyService
from app.services.analytics import AnalyticsService
from app.services.auth import AuthService

__all__ = [
    "GeminiService",
    "RAGService",  # Now it exists
    "NavigationService",
    "CrowdManagementService",
    "QueueManagementService",
    "EmergencyService",
    "AnalyticsService",
    "AuthService"
]