from fastapi import APIRouter, HTTPException, Depends, Query, WebSocket
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.services.crowd_management import CrowdManagementService
from app.services.gemini_service import GeminiService
from app.models.user import User
from app.models.stadium import CrowdData
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
crowd_service = CrowdManagementService()
gemini_service = GeminiService()


@router.get("/heatmap")
async def get_heatmap_data(
    section: Optional[str] = Query(None, description="Specific section"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get crowd heatmap data for the stadium
    
    Args:
        section: Optional section filter
        current_user: Current authenticated user
    
    Returns:
        Heatmap data with density information
    """
    try:
        heatmap_data = await crowd_service.get_heatmap_data(section)
        
        # Add AI insights
        ai_insights = await gemini_service.analyze_crowd({
            "density": heatmap_data.get("sections", {}),
            "timestamp": datetime.utcnow().isoformat(),
            "event": "FIFA World Cup"
        })
        
        return {
            "heatmap": heatmap_data,
            "insights": ai_insights,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Heatmap error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get heatmap data: {str(e)}"
        )


@router.get("/status")
async def get_crowd_status(
    area: Optional[str] = Query(None, description="Area to check"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get overall crowd status
    
    Args:
        area: Optional area filter
        current_user: Current authenticated user
    
    Returns:
        Crowd status information
    """
    try:
        status = await crowd_service.get_current_status(area)
        
        return {
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Crowd status error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get crowd status: {str(e)}"
        )


@router.post("/analyze")
async def analyze_crowd(
    data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyze crowd data and get recommendations
    
    Args:
        data: Crowd data to analyze
        current_user: Current authenticated user
    
    Returns:
        Analysis results with recommendations
    """
    try:
        analysis = await crowd_service.analyze_crowd(data)
        
        # Add AI-powered recommendations
        if analysis.get("crowd_level") in ["high", "critical"]:
            ai_recommendations = await gemini_service.process_query(
                f"Provide crowd management recommendations for {analysis.get('crowd_level')} congestion",
                {"data": analysis}
            )
            analysis["ai_recommendations"] = ai_recommendations.get("response", "")
        
        logger.info(f"Crowd analysis completed for user {current_user.get('id')}")
        
        return {
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Crowd analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze crowd: {str(e)}"
        )


@router.get("/predictions")
async def get_crowd_predictions(
    minutes: int = Query(15, description="Prediction timeframe in minutes"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get crowd predictions for the future
    
    Args:
        minutes: Prediction timeframe in minutes
        current_user: Current authenticated user
    
    Returns:
        Crowd predictions
    """
    try:
        predictions = await crowd_service.predict_crowd(minutes)
        
        return {
            "timeframe": f"{minutes} minutes",
            "predictions": predictions,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get predictions: {str(e)}"
        )


@router.get("/hotspots")
async def get_crowd_hotspots(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current crowd hotspots
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        List of hotspots
    """
    try:
        hotspots = await crowd_service.get_hotspots()
        
        return {
            "hotspots": hotspots,
            "count": len(hotspots),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Hotspots error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get hotspots: {str(e)}"
        )


@router.get("/recommendations")
async def get_crowd_recommendations(
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get crowd management recommendations
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        List of recommendations
    """
    try:
        recommendations = await crowd_service.get_recommendations()
        
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


@router.post("/update")
async def update_crowd_data(
    data: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Update crowd data in real-time
    
    Args:
        data: Crowd data to update
        current_user: Current authenticated user
    
    Returns:
        Update confirmation
    """
    try:
        # Only organizers and admins can update crowd data
        if current_user.get("role") not in ["organizer", "admin"]:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        
        result = await crowd_service.update_crowd_data(data)
        
        logger.info(f"Crowd data updated by {current_user.get('id')}")
        
        return {
            "message": "Crowd data updated successfully",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update crowd data: {str(e)}"
        )