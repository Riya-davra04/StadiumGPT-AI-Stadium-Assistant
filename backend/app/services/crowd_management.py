from typing import Dict, List, Any
import numpy as np
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class CrowdManagementService:
    def __init__(self):
        self.crowd_data = {}
        self.historical_data = []
        self.thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8
        }
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current crowd situation"""
        try:
            density = data.get("density", {})
            timestamp = data.get("timestamp", datetime.utcnow())
            
            total_density = np.mean(list(density.values()))
            max_density = max(density.values()) if density else 0
            hotspots = self._identify_hotspots(density)
            
            crowd_level = self._get_crowd_level(total_density)
            predictions = await self._predict_crowd(density)
            recommendations = self._generate_recommendations(
                density, crowd_level, hotspots
            )
            
            return {
                "current_density": total_density,
                "crowd_level": crowd_level,
                "hotspots": hotspots,
                "predictions": predictions,
                "recommendations": recommendations,
                "timestamp": timestamp.isoformat()
            }
        except Exception as e:
            logger.error(f"Crowd analysis error: {e}")
            return {"error": "Could not analyze crowd"}
    
    def _identify_hotspots(self, density: Dict[str, float]) -> List[Dict]:
        """Identify crowd hotspots"""
        hotspots = []
        threshold = self.thresholds["high"]
        
        for location, value in density.items():
            if value > threshold:
                hotspots.append({
                    "location": location,
                    "density": value,
                    "severity": "high"
                })
        
        return sorted(hotspots, key=lambda x: x["density"], reverse=True)
    
    def _get_crowd_level(self, density: float) -> str:
        """Determine crowd level"""
        if density < self.thresholds["low"]:
            return "low"
        elif density < self.thresholds["medium"]:
            return "medium"
        else:
            return "high"
    
    async def _predict_crowd(self, current_data: Dict) -> Dict:
        """Predict crowd movement"""
        return {
            "15_min": "High congestion expected at Gates A and B",
            "30_min": "Congestion will spread to concourse",
            "60_min": "Crowd levels expected to decrease by 30%"
        }
    
    def _generate_recommendations(
        self,
        density: Dict,
        crowd_level: str,
        hotspots: List[Dict]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if crowd_level == "high":
            recommendations.append("Open additional gates to reduce congestion")
            recommendations.append("Redirect fans to less crowded entrances")
            recommendations.append("Increase security presence at hotspots")
        
        if crowd_level == "medium":
            recommendations.append("Monitor crowd flow patterns")
            recommendations.append("Prepare for potential congestion")
        
        if hotspots:
            for hotspot in hotspots[:3]:
                recommendations.append(
                    f"Deploy additional staff to {hotspot['location']}"
                )
        
        return recommendations
    
    async def get_heatmap_data(self) -> Dict:
        """Generate heatmap data for visualization"""
        sections = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2"]
        data = {}
        
        for section in sections:
            data[section] = random.uniform(0.1, 0.9)
        
        return {
            "sections": data,
            "timestamp": datetime.utcnow().isoformat(),
            "legend": {
                "low": "Green",
                "medium": "Yellow",
                "high": "Red"
            }
        }