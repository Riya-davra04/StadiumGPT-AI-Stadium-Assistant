from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Analytics service for stadium data processing"""
    
    def __init__(self):
        self.data_cache = {}
        self.historical_data = []
        self.thresholds = {
            "crowd": {"low": 0.3, "medium": 0.6, "high": 0.8},
            "queue": {"short": 5, "medium": 15, "long": 30}
        }
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze crowd data"""
        try:
            density = data.get("density", {})
            timestamp = data.get("timestamp", datetime.utcnow())
            
            # Calculate statistics
            densities = list(density.values())
            avg_density = np.mean(densities) if densities else 0
            max_density = max(densities) if densities else 0
            min_density = min(densities) if densities else 0
            std_density = np.std(densities) if densities else 0
            
            # Identify hotspots
            hotspots = []
            for location, value in density.items():
                if value > self.thresholds["crowd"]["high"]:
                    hotspots.append({
                        "location": location,
                        "density": value,
                        "severity": "high"
                    })
                elif value > self.thresholds["crowd"]["medium"]:
                    hotspots.append({
                        "location": location,
                        "density": value,
                        "severity": "medium"
                    })
            
            # Determine crowd level
            if avg_density < self.thresholds["crowd"]["low"]:
                crowd_level = "low"
            elif avg_density < self.thresholds["crowd"]["medium"]:
                crowd_level = "medium"
            else:
                crowd_level = "high"
            
            # Generate predictions
            predictions = await self._predict_crowd(density)
            
            return {
                "average_density": avg_density,
                "max_density": max_density,
                "min_density": min_density,
                "std_density": std_density,
                "crowd_level": crowd_level,
                "hotspots": hotspots,
                "predictions": predictions,
                "timestamp": timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {"error": str(e)}
    
    async def _predict_crowd(self, current_data: Dict) -> Dict[str, Any]:
        """Predict future crowd patterns"""
        try:
            # Simple prediction model
            predictions = {
                "15_min": {},
                "30_min": {},
                "60_min": {}
            }
            
            for location, value in current_data.items():
                # Simple linear prediction
                predictions["15_min"][location] = min(1.0, value * 1.1)
                predictions["30_min"][location] = min(1.0, value * 1.2)
                predictions["60_min"][location] = min(1.0, value * 0.9)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {}
    
    async def analyze_queue(self, queue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze queue data"""
        try:
            queue_length = queue_data.get("queue_length", 0)
            service_time = queue_data.get("avg_service_time", 0)
            capacity = queue_data.get("capacity", 0)
            
            # Calculate metrics
            load_percentage = (queue_length / capacity) * 100 if capacity > 0 else 0
            estimated_wait = queue_length * service_time
            
            # Determine status
            if load_percentage < 50:
                status = "available"
            elif load_percentage < 80:
                status = "moderate"
            else:
                status = "busy"
            
            return {
                "queue_length": queue_length,
                "load_percentage": load_percentage,
                "estimated_wait": estimated_wait,
                "status": status,
                "efficiency": max(0, 100 - load_percentage)
            }
            
        except Exception as e:
            logger.error(f"Queue analysis error: {e}")
            return {"error": str(e)}
    
    async def generate_insights(self, data_type: str, data: Dict) -> List[str]:
        """Generate insights from data"""
        insights = []
        
        if data_type == "crowd":
            if data.get("crowd_level") == "high":
                insights.append("High crowd levels detected. Consider additional staffing.")
                insights.append("Monitor entry and exit points closely.")
                insights.append("Prepare for potential delays.")
            elif data.get("crowd_level") == "medium":
                insights.append("Moderate crowd levels. Normal operations.")
                insights.append("Watch for developing congestion.")
            else:
                insights.append("Low crowd levels. Operations running smoothly.")
                
            # Hotspot insights
            hotspots = data.get("hotspots", [])
            if hotspots:
                insights.append(f"Hotspot identified: {hotspots[0]['location']}")
                
        elif data_type == "queue":
            if data.get("status") == "busy":
                insights.append("Queue is busy. Consider opening additional counters.")
                insights.append(f"Estimated wait time: {data.get('estimated_wait')} minutes")
                
        return insights
    
    async def get_statistics(self, metric_type: str) -> Dict[str, Any]:
        """Get statistics for a specific metric"""
        try:
            stats = {
                "crowd": {
                    "avg_density": np.random.uniform(0.2, 0.8),
                    "peak_density": np.random.uniform(0.6, 1.0),
                    "total_capacity": 80000,
                    "current_occupancy": int(np.random.uniform(30000, 70000))
                },
                "queue": {
                    "avg_wait_time": np.random.uniform(2, 15),
                    "max_wait_time": np.random.uniform(10, 30),
                    "total_queues": 20,
                    "active_queues": np.random.randint(5, 15)
                },
                "emergency": {
                    "active_alerts": np.random.randint(0, 3),
                    "today_incidents": np.random.randint(1, 10),
                    "response_time": np.random.uniform(1, 5)
                }
            }
            
            return stats.get(metric_type, {})
            
        except Exception as e:
            logger.error(f"Statistics error: {e}")
            return {}