from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.services.navigation import NavigationService
from app.services.gemini_service import GeminiService
from app.models.user import User
from app.utils.validators import validate_location
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)

# ✅ Create router instance
router = APIRouter()

# Initialize services
navigation_service = NavigationService()
gemini_service = GeminiService()


@router.get("/route")
async def get_route(
    start: str = Query(..., description="Starting location"),
    end: str = Query(..., description="Destination location"),
    preferences: Optional[List[str]] = Query(None, description="Route preferences"),
    accessibility: bool = Query(False, description="Enable accessibility mode"),
    avoid_crowds: bool = Query(False, description="Avoid crowded areas"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the optimal route between two locations in the stadium
    """
    try:
        # Validate locations
        if not validate_location(start):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid start location: {start}"
            )
        if not validate_location(end):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid end location: {end}"
            )
        
        # Get route from navigation service
        route = await navigation_service.find_route(
            start=start,
            end=end,
            preferences=preferences or [],
            accessibility=accessibility,
            avoid_crowds=avoid_crowds
        )
        
        # Convert Route object to dictionary
        route_dict = {
            "path": route.path,
            "estimated_time": route.estimated_time,
            "accessibility_info": route.accessibility_info,
            "crowd_level": route.crowd_level,
            "alternatives": route.alternatives
        }
        
        # Add AI-powered recommendations
        context = {
            "start": start,
            "end": end,
            "preferences": preferences,
            "accessibility": accessibility
        }
        ai_recommendation = await gemini_service.process_query(
            f"Provide tips for navigating from {start} to {end} in the stadium",
            context
        )
        route_dict["ai_recommendation"] = ai_recommendation.get("response", "")
        
        logger.info(f"Route found from {start} to {end} for user {current_user.get('id')}")
        
        return {
            "route": route_dict,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Route error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find route: {str(e)}"
        )


@router.get("/nearby")
async def get_nearby_locations(
    location: str = Query(..., description="Current location"),
    radius: int = Query(50, description="Radius in meters"),
    facility_type: Optional[str] = Query(None, description="Filter by facility type"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get nearby facilities and points of interest
    """
    try:
        nearby = await navigation_service.get_nearby_locations(
            location=location,
            radius=radius,
            facility_type=facility_type
        )
        
        return {
            "location": location,
            "radius": radius,
            "facilities": nearby,
            "count": len(nearby),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Nearby locations error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get nearby locations: {str(e)}"
        )


@router.get("/directions")
async def get_directions(
    start: str = Query(..., description="Starting location"),
    end: str = Query(..., description="Destination location"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get step-by-step directions
    """
    try:
        directions = await navigation_service.get_directions(start, end)
        
        # Add AI-powered voice guidance
        context = {
            "start": start,
            "end": end,
            "directions": directions
        }
        voice_guidance = await gemini_service.process_query(
            f"Generate voice guidance for these directions: {directions}",
            context
        )
        
        return {
            "directions": directions,
            "voice_guidance": voice_guidance.get("response", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Directions error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get directions: {str(e)}"
        )


@router.get("/accessibility-routes")
async def get_accessibility_routes(
    start: str = Query(..., description="Starting location"),
    end: str = Query(..., description="Destination location"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get accessible routes for users with disabilities
    """
    try:
        route = await navigation_service.get_accessible_route(start, end)
        
        return {
            "route": route,
            "accessibility_features": {
                "wheelchair_accessible": route.get("wheelchair_accessible", True),
                "elevator_available": route.get("elevator_available", False),
                "ramp_available": route.get("ramp_available", False),
                "accessible_restrooms": route.get("accessible_restrooms", []),
                "visual_guidance": route.get("visual_guidance", True)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Accessibility route error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get accessibility route: {str(e)}"
        )


@router.get("/crowd-status")
async def get_crowd_status(
    location: str = Query(..., description="Location to check"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get crowd status for a specific location
    """
    try:
        status = await navigation_service.get_location_crowd_status(location)
        
        return {
            "location": location,
            "crowd_level": status.get("level", "low"),
            "density": status.get("density", 0),
            "wait_time": status.get("wait_time", 0),
            "recommendation": status.get("recommendation", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Crowd status error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get crowd status: {str(e)}"
        )


@router.get("/emergency-exits")
async def get_emergency_exits(
    current_location: str = Query(..., description="Current location"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get nearest emergency exits
    """
    try:
        exits = await navigation_service.get_nearest_exits(current_location)
        
        return {
            "current_location": current_location,
            "nearest_exits": exits,
            "total_exits": len(exits),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Emergency exits error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get emergency exits: {str(e)}"
        )