from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.services.emergency import EmergencyService
from app.services.gemini_service import GeminiService
from app.models.emergency import EmergencyAlert, EmergencyType, EmergencySeverity
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
emergency_service = EmergencyService()
gemini_service = GeminiService()


@router.post("/report")
async def report_emergency(
    alert_data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Report an emergency
    """
    try:
        # Add reporter info
        alert_data["reported_by"] = current_user.get("id")
        alert_data["reporter_name"] = current_user.get("name")
        
        # Handle emergency
        response = await emergency_service.handle_emergency(alert_data)
        
        # ✅ Return response directly
        logger.warning(f"Emergency reported by {current_user.get('id')}: {alert_data.get('type')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Emergency report error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to report emergency: {str(e)}"
        )


@router.get("/active")
async def get_active_emergencies(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get all active emergencies
    """
    try:
        alerts = await emergency_service.get_active_alerts()
        
        return {
            "alerts": alerts,
            "count": len(alerts),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Active emergencies error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get active emergencies: {str(e)}"
        )


@router.get("/{alert_id}")
async def get_emergency_details(
    alert_id: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get details of a specific emergency
    """
    try:
        alert = await emergency_service.get_alert(alert_id)
        if not alert:
            raise HTTPException(
                status_code=404,
                detail="Emergency not found"
            )
        
        return {
            "alert": alert,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Emergency details error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get emergency details: {str(e)}"
        )


@router.post("/resolve/{alert_id}")
async def resolve_emergency(
    alert_id: str,
    resolution_notes: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Resolve an emergency
    """
    try:
        # Only organizers, staff, and admins can resolve emergencies
        if current_user.get("role") not in ["organizer", "staff", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        
        result = await emergency_service.resolve_emergency(
            alert_id,
            resolution_notes,
            current_user.get("id")
        )
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Emergency not found"
            )
        
        logger.info(f"Emergency {alert_id} resolved by {current_user.get('id')}")
        
        return {
            "message": "Emergency resolved successfully",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resolve emergency error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to resolve emergency: {str(e)}"
        )


@router.get("/stations")
async def get_emergency_stations(
    location: Optional[str] = Query(None, description="Current location"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get emergency stations
    """
    try:
        stations = await emergency_service.get_stations(location)
        
        return {
            "stations": stations,
            "count": len(stations),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stations error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stations: {str(e)}"
        )


@router.get("/medical")
async def get_medical_emergencies(
    severity: Optional[EmergencySeverity] = Query(None, description="Filter by severity"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get medical emergencies
    """
    try:
        emergencies = await emergency_service.get_medical_emergencies(severity)
        
        return {
            "emergencies": emergencies,
            "count": len(emergencies),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Medical emergencies error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get medical emergencies: {str(e)}"
        )