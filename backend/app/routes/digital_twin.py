"""
Digital Twin Routes
===================
API endpoints for stadium crowd simulation and prediction.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any
from datetime import datetime
import logging

from app.services.digital_twin import DigitalTwinService
from app.routes.auth import get_current_user

router: APIRouter = APIRouter()
digital_twin: DigitalTwinService = DigitalTwinService()
logger = logging.getLogger(__name__)


@router.get("/status")
async def get_simulation_status(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current simulation status.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dict with simulation status
    """
    return {
        "running": digital_twin.simulation_running,
        "timestamp": datetime.utcnow().isoformat(),
        "sections_count": len(digital_twin.sections)
    }


@router.post("/simulation/start")
async def start_simulation(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Start crowd simulation.
    
    Args:
        current_user: Authenticated user (requires organizer/admin role)
        
    Returns:
        Dict with status and timestamp
    """
    if current_user.get("role") not in ["organizer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions. Organizer or admin role required."
        )
    
    return await digital_twin.start_simulation()


@router.post("/simulation/stop")
async def stop_simulation(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Stop crowd simulation.
    
    Args:
        current_user: Authenticated user (requires organizer/admin role)
        
    Returns:
        Dict with status and timestamp
    """
    if current_user.get("role") not in ["organizer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions. Organizer or admin role required."
        )
    
    return await digital_twin.stop_simulation()


@router.get("/predict/crowd")
async def predict_crowd(
    minutes: int = Query(15, description="Prediction timeframe in minutes"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Predict crowd movement for the next X minutes.
    
    Args:
        minutes: Prediction timeframe in minutes (default: 15)
        current_user: Authenticated user
        
    Returns:
        Dict containing predictions and summary
    """
    try:
        return await digital_twin.predict_crowd_movement(minutes)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to predict crowd: {str(e)}"
        )


@router.get("/heatmap")
async def get_heatmap_data(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get real-time heatmap data.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dict with heatmap data and legend
    """
    try:
        return await digital_twin.get_heatmap_data()
    except Exception as e:
        logger.error(f"Heatmap error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get heatmap data: {str(e)}"
        )


@router.get("/section/{section}")
async def get_section_status(
    section: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current status for a specific section.
    
    Args:
        section: Section identifier
        current_user: Authenticated user
        
    Returns:
        Dict with section status
    """
    try:
        return await digital_twin.get_section_status(section)
    except Exception as e:
        logger.error(f"Section status error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get section status: {str(e)}"
        )


@router.post("/update-section")
async def update_section_density(
    section: str = Query(..., description="Section identifier"),
    density: float = Query(..., description="Density value (0-1)"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Update density for a specific section.
    
    Args:
        section: Section identifier
        density: Density value (0-1)
        current_user: Authenticated user (requires organizer/admin role)
        
    Returns:
        Dict with status and updated data
    """
    if current_user.get("role") not in ["organizer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions. Organizer or admin role required."
        )
    
    try:
        return await digital_twin.update_section_density(section, density)
    except Exception as e:
        logger.error(f"Update section error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update section: {str(e)}"
        )