from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.services.gemini_service import GeminiService
from app.routes.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()
gemini_service = GeminiService()


@router.get("/faq")
async def get_faq(
    query: Optional[str] = Query(None, description="Search query"),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get FAQ answers
    
    Args:
        query: Search query
        current_user: Current authenticated user
    
    Returns:
        FAQ results
    """
    try:
        faqs = {
            "lost_and_found": "Visit Guest Services at Section A",
            "medical": "First aid stations at Sections A, C, E",
            "tickets": "Ticket issues: Contact Box Office at Gate A",
            "wheelchair": "Wheelchair access at Gate C",
            "food": "Food courts located throughout the stadium"
        }
        
        if query:
            result = await gemini_service.process_query(
                f"Answer this volunteer FAQ: {query}",
                {"faqs": faqs}
            )
            return {
                "query": query,
                "answer": result.get("response", ""),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        return {
            "faqs": faqs,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"FAQ error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get FAQ: {str(e)}"
        )