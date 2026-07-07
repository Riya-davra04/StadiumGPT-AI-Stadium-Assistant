"""
Digital Twin Routes
===================
API endpoints for stadium crowd simulation and prediction.
"""

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
    """
    Predict congestion for a section or all sections.
    
    Returns actionable insights for organizers.
    """
    try:
        return await digital_twin.predict_congestion(section, minutes)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict congestion")


@router.get("/dashboard")
async def get_realtime_dashboard(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get real-time dashboard data for organizers.
    
    Returns live crowd status, estimates, and alerts.
    """
    try:
        return await digital_twin.get_realtime_dashboard()
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")


@router.post("/alert/{section}")
async def create_alert(
    section: str,
    message: str = Query(..., description="Alert message"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Create an alert for a specific section.
    
    This can be triggered automatically or manually by organizers.
    """
    if current_user.get("role") not in ["organizer", "admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return {
        "section": section,
        "message": message,
        "created_by": current_user.get("name"),
        "timestamp": datetime.utcnow().isoformat()
    }