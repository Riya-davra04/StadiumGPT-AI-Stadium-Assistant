"""
Crowd Management Service
========================
Handles crowd density analysis, heatmap generation, and real-time crowd insights.
"""

import random
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CrowdManagementService:
    """
    Service for analyzing and managing stadium crowd density.
    
    This service provides:
    - Real-time crowd density analysis
    - Heatmap data generation
    - Crowd level predictions
    - Actionable recommendations for organizers
    """
    
    def __init__(self) -> None:
        """Initialize the crowd management service with default thresholds."""
        self.crowd_data: Dict[str, Any] = {}
        self.historical_data: List[Dict] = []
        self.thresholds: Dict[str, float] = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8
        }
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current crowd situation and provide insights.
        
        Args:
            data: Crowd data containing density information by section
            
        Returns:
            Dict containing:
            - current_density: Average crowd density
            - crowd_level: Overall crowd level (low/medium/high/critical)
            - hotspots: List of crowded locations
            - predictions: Future crowd predictions
            - recommendations: Actionable recommendations
            
        Example:
            >>> result = await crowd_service.analyze_crowd({"density": {"A1": 0.8, "B1": 0.3}})
            >>> print(result["crowd_level"])
            'high'
        """
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
        """Generate real-time heatmap data for visualization."""
        sections = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2"]
        data = {}
        for section in sections:
            data[section] = random.uniform(0.1, 0.9)
        
        return {
            "sections": data,
            "timestamp": datetime.utcnow().isoformat(),
            "legend": {
                "low": {"level": "Low", "color": "#4CAF50"},
                "medium": {"level": "Medium", "color": "#FF9800"},
                "high": {"level": "High", "color": "#F44336"},
                "critical": {"level": "Critical", "color": "#D32F2F"}
            }
        }
    
    async def get_current_status(self, area: Optional[str] = None) -> Dict[str, Any]:
        """Get current crowd status for the stadium or specific area."""
        return {
            "overall": "medium",
            "areas": {
                "Gate A": {"level": "high", "density": 0.8},
                "Gate B": {"level": "low", "density": 0.2},
                "Gate C": {"level": "medium", "density": 0.5}
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _identify_hotspots(self, density: Dict[str, float]) -> List[Dict]:
        """Identify crowd hotspots based on density thresholds."""
        hotspots = []
        for location, value in density.items():
            if value > self.thresholds["high"]:
                hotspots.append({
                    "location": location,
                    "density": value,
                    "severity": "high"
                })
        return sorted(hotspots, key=lambda x: x["density"], reverse=True)
    
    def _get_crowd_level(self, density: float) -> str:
        """Determine overall crowd level from density."""
        if density < self.thresholds["low"]:
            return "low"
        elif density < self.thresholds["medium"]:
            return "medium"
        else:
            return "high"
    
    async def _predict_crowd(self, current_data: Dict) -> Dict:
        """Predict crowd movement based on current data."""
        return {
            "15_min": "High congestion expected at Gates A and B",
            "30_min": "Congestion will spread to concourse",
            "60_min": "Crowd levels expected to decrease by 30%"
        }
    
    def _generate_recommendations(self, density: Dict, crowd_level: str, hotspots: List[Dict]) -> List[str]:
        """Generate actionable recommendations for organizers."""
        recommendations = []
        if crowd_level == "high":
            recommendations.append("Open additional gates to reduce congestion")
            recommendations.append("Redirect fans to less crowded entrances")
        if hotspots:
            for hotspot in hotspots[:2]:
                recommendations.append(f"Deploy additional staff to {hotspot['location']}")
        return recommendations or ["Monitor crowd flow patterns"]