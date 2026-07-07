from typing import Dict, List, Any
import numpy as np
from datetime import datetime
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
            
            densities = list(density.values())
            avg_density = np.mean(densities) if densities else 0
            max_density = max(densities) if densities else 0
            
            hotspots = self._identify_hotspots(density)
            crowd_level = self._get_crowd_level(avg_density)
            predictions = await self._predict_crowd(density)
            recommendations = self._generate_recommendations(density, crowd_level, hotspots)
            
            return {
                "current_density": avg_density,
                "crowd_level": crowd_level,
                "hotspots": hotspots,
                "predictions": predictions,
                "recommendations": recommendations,
                "timestamp": timestamp.isoformat()
            }
        except Exception as e:
            logger.error(f"Crowd analysis error: {e}")
            return {"error": "Could not analyze crowd"}
    
    async def get_heatmap_data(self) -> Dict[str, Any]:
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
    
    async def get_current_status(self, area: str = None) -> Dict[str, Any]:
        """Get current crowd status"""
        return {
            "overall": "medium",
            "areas": {
                "Gate A": {"level": "high", "density": 0.8},
                "Gate B": {"level": "low", "density": 0.2},
                "Gate C": {"level": "medium", "density": 0.5}
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def predict_crowd(self, minutes: int = 15) -> Dict:
        """Predict crowd movement"""
        return {
            "15_min": "High congestion expected at Gates A and B",
            "30_min": "Congestion will spread to concourse",
            "60_min": "Crowd levels expected to decrease by 30%"
        }
    
    async def get_hotspots(self) -> List[Dict]:
        """Get current crowd hotspots"""
        return [
            {"location": "Gate A", "density": 0.85, "severity": "high"},
            {"location": "Food Court", "density": 0.75, "severity": "medium"}
        ]
    
    async def get_recommendations(self) -> List[str]:
        """Get crowd management recommendations"""
        return [
            "Open additional gates to reduce congestion",
            "Redirect fans to less crowded entrances",
            "Increase security presence at hotspots"
        ]
    
    async def update_crowd_data(self, data: Dict) -> Dict:
        """Update crowd data"""
        self.crowd_data.update(data)
        return {"status": "updated", "timestamp": datetime.utcnow().isoformat()}
    
    def _identify_hotspots(self, density: Dict[str, float]) -> List[Dict]:
        hotspots = []
        for location, value in density.items():
            if value > self.thresholds["high"]:
                hotspots.append({"location": location, "density": value, "severity": "high"})
        return sorted(hotspots, key=lambda x: x["density"], reverse=True)
    
    def _get_crowd_level(self, density: float) -> str:
        if density < self.thresholds["low"]:
            return "low"
        elif density < self.thresholds["medium"]:
            return "medium"
        else:
            return "high"
    
    async def _predict_crowd(self, current_data: Dict) -> Dict:
        return {
            "15_min": "High congestion expected at Gates A and B",
            "30_min": "Congestion will spread to concourse",
            "60_min": "Crowd levels expected to decrease by 30%"
        }
    
    def _generate_recommendations(self, density: Dict, crowd_level: str, hotspots: List[Dict]) -> List[str]:
        recommendations = []
        if crowd_level == "high":
            recommendations.append("Open additional gates to reduce congestion")
            recommendations.append("Redirect fans to less crowded entrances")
        if hotspots:
            for hotspot in hotspots[:2]:
                recommendations.append(f"Deploy additional staff to {hotspot['location']}")
        return recommendations or ["Monitor crowd flow patterns"]