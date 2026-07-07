from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.services.gemini_service import GeminiService
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()
gemini_service = GeminiService()


@router.get("/options")
async def get_transport_options(
    current_location: str = Query(..., description="Current location"),
    destination: Optional[str] = Query(None, description="Destination"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get available transport options
    
    Args:
        current_location: Current location
        destination: Destination
        current_user: Current authenticated user
    
    Returns:
        Transport options
    """
    try:
        # Mock transport options
        options = {
            "metro": {
                "name": "Metro",
                "distance": 200,
                "estimated_time": 5,
                "crowd_level": "medium",
                "availability": "available",
                "waiting_time": 3
            },
            "bus": {
                "name": "Bus",
                "distance": 150,
                "estimated_time": 10,
                "crowd_level": "low",
                "availability": "available",
                "waiting_time": 15
            },
            "taxi": {
                "name": "Taxi/Ride-share",
                "distance": 100,
                "estimated_time": 8,
                "crowd_level": "low",
                "availability": "limited",
                "waiting_time": 20,
                "cost": 15.50
            },
            "parking": {
                "name": "Parking",
                "distance": 300,
                "estimated_time": 12,
                "crowd_level": "high",
                "availability": "limited"
            }
        }
        
        # Add AI recommendation
        context = {
            "current_location": current_location,
            "destination": destination,
            "options": options
        }
        ai_recommendation = await gemini_service.process_query(
            f"Recommend the best transport option from {current_location}",
            context
        )
        
        return {
            "options": options,
            "recommendation": ai_recommendation.get("response", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Transport options error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get transport options: {str(e)}"
        )


@router.get("/parking")
async def get_parking_status(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get parking availability"""
    try:
        parking = {
            "P1": {"available": 45, "total": 200, "status": "available"},
            "P2": {"available": 12, "total": 150, "status": "limited"},
            "P3": {"available": 0, "total": 100, "status": "full"}
        }
        
        return {
            "parking": parking,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Parking error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get parking status: {str(e)}"
        )