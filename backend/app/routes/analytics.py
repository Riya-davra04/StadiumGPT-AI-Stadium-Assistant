from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import logging

from app.services.analytics import AnalyticsService
from app.routes.auth import get_current_user

router = APIRouter()
analytics_service = AnalyticsService()
logger = logging.getLogger(__name__)


@router.post("/crowd")
async def analyze_crowd(
    data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Analyze crowd data and get insights."""
    try:
        return await analytics_service.analyze_crowd(data)
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))