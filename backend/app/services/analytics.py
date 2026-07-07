from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self) -> None:
        self.data_cache: Dict[str, Any] = {}
        self.historical_data: List[Dict] = []
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            density = data.get("density", {})
            densities = list(density.values())
            
            if not densities:
                return {"error": "No density data provided"}
            
            avg_density = sum(densities) / len(densities)
            max_density = max(densities)
            min_density = min(densities)
            
            return {
                "average_density": round(avg_density, 2),
                "max_density": round(max_density, 2),
                "min_density": round(min_density, 2),
                "crowd_level": self._get_crowd_level(avg_density),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {"error": str(e)}
    
    def _get_crowd_level(self, density: float) -> str:
        if density < 0.3:
            return "low"
        elif density < 0.6:
            return "medium"
        elif density < 0.8:
            return "high"
        return "critical"