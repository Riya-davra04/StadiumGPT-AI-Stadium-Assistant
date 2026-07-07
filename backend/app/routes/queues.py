from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.services.queue_management import QueueManagementService
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
queue_service = QueueManagementService()


@router.get("/status/{establishment_id}")
async def get_queue_status(
    establishment_id: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get queue status for a specific establishment
    
    Args:
        establishment_id: ID of the establishment (e.g., food_a, restroom_1)
        current_user: Current authenticated user
    
    Returns:
        Queue status with wait time and availability
    """
    try:
        status = await queue_service.predict_wait_time(establishment_id)
        
        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Queue status error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get queue status: {str(e)}"
        )


@router.get("/all")
async def get_all_queues(
    category: Optional[str] = Query(None, description="Filter by category: food, restroom, merch"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get status of all queues
    
    Args:
        category: Optional category filter
        current_user: Current authenticated user
    
    Returns:
        All queue statuses with summary
    """
    try:
        queues = await queue_service.get_all_queues()
        
        # Filter by category if specified
        if category:
            filtered_queues = {
                k: v for k, v in queues.get("queues", {}).items()
                if k.startswith(category)
            }
            queues["queues"] = filtered_queues
        
        return queues
        
    except Exception as e:
        logger.error(f"All queues error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get queues: {str(e)}"
        )


@router.get("/best-option")
async def get_best_queue_option(
    category: str = Query(..., description="Category: food, restroom, merch"),
    max_wait: Optional[int] = Query(10, description="Maximum acceptable wait time in minutes"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the best queue option based on wait time
    
    Args:
        category: Category to search (food, restroom, merch)
        max_wait: Maximum acceptable wait time in minutes
        current_user: Current authenticated user
    
    Returns:
        Best queue option with wait time and status
    """
    try:
        best_option = await queue_service.find_best_option(category, max_wait)
        
        return {
            "best_option": best_option if best_option else {
                "message": f"No options available in {category} under {max_wait} minutes"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Best option error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find best option: {str(e)}"
        )


@router.get("/wait-times")
async def get_wait_times(
    locations: List[str] = Query(..., description="List of establishment IDs"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get wait times for multiple locations
    
    Args:
        locations: List of establishment IDs
        current_user: Current authenticated user
    
    Returns:
        Wait times for specified locations
    """
    try:
        wait_times = {}
        for location in locations:
            status = await queue_service.predict_wait_time(location)
            wait_times[location] = status.get("estimated_wait", 0)
        
        return {
            "wait_times": wait_times,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Wait times error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get wait times: {str(e)}"
        )


@router.post("/update")
async def update_queue_status(
    data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Update queue status (organizer/staff only)
    
    Args:
        data: Queue update data
        current_user: Current authenticated user
    
    Returns:
        Update confirmation
    """
    try:
        # Only organizers, staff, and admins can update queues
        if current_user.get("role") not in ["organizer", "staff", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        
        result = await queue_service.update_queue(data)
        
        logger.info(f"Queue updated by {current_user.get('id')}")
        
        return {
            "message": "Queue updated successfully",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update queue: {str(e)}"
        )


@router.get("/recommendations")
async def get_queue_recommendations(
    current_location: str = Query(..., description="Current location"),
    category: Optional[str] = Query(None, description="Filter by category"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get personalized queue recommendations
    
    Args:
        current_location: User's current location
        category: Optional category filter
        current_user: Current authenticated user
    
    Returns:
        Personalized recommendations
    """
    try:
        recommendations = await queue_service.get_recommendations(
            current_location,
            category
        )
        
        return {
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get recommendations: {str(e)}"
        )