from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime, timedelta
import random
import logging
from app.utils.batch import CacheManager

logger = logging.getLogger(__name__)


class QueueManagementService:
    def __init__(self):
        self.establishments = {
            "food_a": {"type": "food", "capacity": 50, "avg_service_time": 3},
            "food_b": {"type": "food", "capacity": 40, "avg_service_time": 2.5},
            "food_c": {"type": "food", "capacity": 60, "avg_service_time": 3.5},
            "restroom_1": {"type": "restroom", "capacity": 10, "avg_service_time": 1},
            "restroom_2": {"type": "restroom", "capacity": 12, "avg_service_time": 1},
            "restroom_3": {"type": "restroom", "capacity": 8, "avg_service_time": 1},
            "merch_1": {"type": "merch", "capacity": 20, "avg_service_time": 2},
            "merch_2": {"type": "merch", "capacity": 15, "avg_service_time": 2.5}
        }
        self.cache = CacheManager(default_ttl=5)
        self.queue_data = {}
    
    async def predict_wait_time(self, establishment: str) -> Dict[str, Any]:
        """Predict wait time with caching"""
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
        """Get alternative establishments"""
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
    
    async def get_all_queues(self) -> Dict[str, Any]:
        """Get all queue statuses efficiently"""
        results = {}
        for name in self.establishments:
            results[name] = await self.predict_wait_time(name)
        
        return {
            "queues": results,
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "food_queues": [name for name in results if name.startswith("food")],
                "restroom_queues": [name for name in results if name.startswith("restroom")],
                "merch_queues": [name for name in results if name.startswith("merch")]
            }
        }
    
    async def find_best_option(self, category: str, max_wait: int = 10) -> Optional[Dict]:
        """
        Find the best queue option based on category and max wait time
        
        Args:
            category (str): Category to search (food, restroom, merch)
            max_wait (int): Maximum acceptable wait time in minutes
        
        Returns:
            Optional[Dict]: Best option found, or None
        """
        try:
            options = []
            
            for name, data in self.establishments.items():
                if name.startswith(category):
                    status = await self.predict_wait_time(name)
                    wait_time = status.get("estimated_wait", 999)
                    if wait_time <= max_wait:
                        options.append({
                            "name": name,
                            "wait_time": wait_time,
                            "status": status.get("status", "unknown"),
                            "queue_length": status.get("queue_length", 0)
                        })
            
            if options:
                return min(options, key=lambda x: x["wait_time"])
            
            return None
            
        except Exception as e:
            logger.error(f"Find best option error: {e}")
            return None
    
    async def get_recommendations(self, current_location: str, category: str = None) -> List[Dict]:
        """Get personalized queue recommendations"""
        recommendations = []
        
        for name, data in self.establishments.items():
            if category and not name.startswith(category):
                continue
            status = await self.predict_wait_time(name)
            if status.get("status") == "available" and status.get("queue_length", 0) < 10:
                recommendations.append({
                    "name": name,
                    "wait_time": status.get("estimated_wait", 0),
                    "queue_length": status.get("queue_length", 0),
                    "status": "Recommended"
                })
        
        return sorted(recommendations, key=lambda x: x["wait_time"])[:5]
    
    async def update_queue(self, data: Dict) -> Dict:
        """Update queue data"""
        try:
            establishment = data.get("establishment")
            queue_length = data.get("queue_length")
            
            if establishment and queue_length is not None:
                self.queue_data[establishment] = queue_length
                # Clear cache for this establishment
                self.cache.clear(f"queue:{establishment}")
            
            return {"status": "updated", "timestamp": datetime.utcnow().isoformat()}
        except Exception as e:
            logger.error(f"Update queue error: {e}")
            raise