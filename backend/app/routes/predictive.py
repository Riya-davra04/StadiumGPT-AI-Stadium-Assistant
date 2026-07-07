from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from app.services.predictive_analytics import PredictiveAnalyticsService
from app.routes.auth import get_current_user

router = APIRouter()
service = PredictiveAnalyticsService()


@router.get("/15min")
async def predict_15min(
    section: Optional[str] = Query(None),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """15-minute crowd prediction."""
    return await service.predict_15min(section)


@router.get("/60min")
async def predict_60min(
    section: Optional[str] = Query(None),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """60-minute crowd prediction."""
    return await service.predict_60min(section)


@router.get("/anomalies")
async def detect_anomalies(
    section: Optional[str] = Query(None),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Detect abnormal crowd patterns."""
    return await service.detect_anomalies(section)