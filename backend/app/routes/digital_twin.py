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
    
    This endpoint uses the Digital Twin simulation engine to predict
    crowd congestion and provide actionable recommendations.
    
    Args:
        section: Specific section to predict (None for all)
        minutes: Prediction timeframe in minutes (default: 30)
        current_user: Authenticated user
    
    Returns:
        Dict with predictions, summary, and actionable alerts
    
    Example Response:
        {
            "predictions": {
                "A1": {
                    "current": 0.65,
                    "predicted_30min": 0.75,
                    "level": "high",
                    "recommendation": "Monitor A1 closely..."
                }
            },
            "summary": {
                "critical_sections": [],
                "high_sections": ["A1"],
                "overall": "high"
            },
            "actionable_alerts": [...]
        }
    """
    try:
        return await digital_twin.predict_congestion(section, minutes)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to predict congestion: {str(e)}"
        )


@router.get("/dashboard")
async def get_realtime_dashboard(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get real-time dashboard data for organizers.
    
    Returns live crowd status, attendance estimates, and alerts
    for all sections in the stadium.
    
    Args:
        current_user: Authenticated user
    
    Returns:
        Dict with sections status and summary statistics
    """
    try:
        return await digital_twin.get_realtime_dashboard()
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get dashboard data: {str(e)}"
        )