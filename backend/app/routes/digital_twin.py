from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from app.services.digital_twin import DigitalTwinService
from app.routes.auth import get_current_user

router: APIRouter = APIRouter()
digital_twin: DigitalTwinService = DigitalTwinService()
logger = logging.getLogger(__name__)


@router.get("/predict/congestion")
async def predict_congestion(
    section: Optional[str] = Query(None, description="Specific section to predict"),
    minutes: int = Query(30, description="Prediction timeframe in minutes"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Predict congestion for a section or all sections."""
    try:
        return await digital_twin.predict_congestion(section, minutes)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict congestion")


@router.get("/dashboard")
async def get_realtime_dashboard(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get real-time dashboard data for organizers."""
    try:
        return await digital_twin.get_realtime_dashboard()
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")