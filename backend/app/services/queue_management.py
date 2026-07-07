"""
Queue Management Service
========================
Handles real-time queue predictions and recommendations for:
- Food stalls
- Restrooms
- Merchandise stores
"""

from typing import Dict, List, Any, Optional
import random
from datetime import datetime
import logging
from app.utils.batch import CacheManager

logger = logging.getLogger(__name__)


class QueueManagementService:
    """
    Service for predicting and managing queue wait times.
    
    This service provides:
    - Real-time queue length predictions
    - Wait time estimates
    - Alternative recommendations
    - Historical trend analysis
    """
    
    def __init__(self) -> None:
        """Initialize the queue management service."""
        self.establishments: Dict[str, Dict] = {
            "food_a": {"type": "food", "capacity": 50, "avg_service_time": 3},
            "food_b": {"type": "food", "capacity": 40, "avg_service_time": 2.5},
            "food_c": {"type": "food", "capacity": 60, "avg_service_time": 3.5},
            "restroom_1": {"type": "restroom", "capacity": 10, "avg_service_time": 1},
            "restroom_2": {"type": "restroom", "capacity": 12, "avg_service_time": 1},
            "restroom_3": {"type": "restroom", "capacity": 8, "avg_service_time": 1},
            "merch_1": {"type": "merch", "capacity": 20, "avg_service_time": 2},
            "merch_2": {"type": "merch", "capacity": 15, "avg_service_time": 2.5}
        }
        self.cache: CacheManager = CacheManager(default_ttl=5)
        self.queue_data: Dict[str, int] = {}
    
    async def predict_wait_time(self, establishment: str) -> Dict[str, Any]:
        """
        Predict wait time for a specific establishment.
        
        Args:
            establishment: Establishment ID (e.g., 'food_a', 'restroom_1')
            
        Returns:
            Dict containing:
            - queue_length: Current queue length
            - estimated_wait: Estimated wait time in minutes
            - status: 'available', 'busy', or 'crowded'
            - recommendation: Suggested alternative if wait is too long
            
        Example:
            >>> result = await queue_service.predict_wait_time('food_a')
            >>> print(result['estimated_wait'])
            '5'
        """
        if establishment not in self.establishments:
            return {"error": "Establishment not found"}
        
        # Check cache
        cache_key = f"queue:{establishment}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Get or simulate current queue length
        queue_length = self.queue_data.get(establishment, random.randint(0, 30))
        capacity = self.establishments[establishment]["capacity"]
        avg_service_time = self.establishments[establishment]["avg_service_time"]
        
        if queue_length > capacity:
            wait_time = (queue_length - capacity) * avg_service_time
            status = "busy"
        else:
            wait_time = 0
            status = "available"
        
        recommendation = None
        if wait_time > 15:
            alternatives = await self.get_alternatives(establishment)
            if alternatives:
                best_alt = min(alternatives, key=lambda x: x["wait_time"])
                recommendation = {
                    "action": f"Consider {best_alt['name']} instead",
                    "time_saved": wait_time - best_alt["wait_time"]
                }
        
        result = {
            "establishment": establishment,
            "queue_length": queue_length,
            "estimated_wait": wait_time,
            "status": status,
            "capacity": capacity,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Cache result
        self.cache.set(cache_key, result)
        return result
    
    async def get_alternatives(self, establishment: str) -> List[Dict]:
        """
        Get alternative establishments with lower wait times.
        
        Args:
            establishment: Current establishment ID
            
        Returns:
            List of alternatives with wait times
        """
        if establishment.startswith("food"):
            alternatives = [
                {"name": "food_b", "wait_time": random.randint(3, 8)},
                {"name": "food_c", "wait_time": random.randint(2, 10)}
            ]
        elif establishment.startswith("restroom"):
            alternatives = [
                {"name": "restroom_2", "wait_time": random.randint(0, 5)},
                {"name": "restroom_3", "wait_time": random.randint(0, 5)}
            ]
        else:
            alternatives = []
        
        return [alt for alt in alternatives if alt["name"] != establishment]