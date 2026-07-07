"""
Digital Twin Service - Predictive Crowd Simulation
===================================================
Provides real-time crowd simulation and prediction for stadium operations.
"""

import random
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import asyncio

logger = logging.getLogger(__name__)


class DigitalTwinService:
    """
    Digital Twin service for crowd simulation and prediction.
    
    This service simulates crowd movement in the stadium to help
    organizers make proactive decisions about:
    - Gate openings
    - Staff deployment
    - Emergency response
    - Queue management
    """
    
    def __init__(self) -> None:
        """Initialize the digital twin service."""
        self.sections: List[str] = [
            'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 
            'D1', 'D2', 'E1', 'E2', 'F1', 'F2'
        ]
        self.gates: List[str] = ['A', 'B', 'C', 'D', 'E']
        self.crowd_density: Dict[str, float] = {}
        self.historical_data: List[Dict] = []
        self.simulation_running: bool = False
        self.prediction_cache: Dict[str, Any] = {}
        self._initialize_density()
    
    def _initialize_density(self) -> None:
        """Initialize crowd density with random values."""
        for section in self.sections:
            self.crowd_density[section] = random.uniform(0.1, 0.7)
    
    async def predict_congestion(self, section: str = None, minutes: int = 30) -> Dict[str, Any]:
        """
        Predict congestion for a section or all sections.
        
        Args:
            section: Section to predict (or None for all)
            minutes: Prediction timeframe in minutes
            
        Returns:
            Dict with congestion predictions
        """
        if section and section not in self.sections:
            return {"error": f"Section {section} not found"}
        
        predictions = {}
        sections_to_predict = [section] if section else self.sections
        
        for sec in sections_to_predict:
            current = self.crowd_density.get(sec, 0.3)
            
            # Simple predictive model with trends
            trend = random.uniform(-0.02, 0.04)
            predicted = max(0.0, min(1.0, current + trend * (minutes / 15)))
            
            predictions[sec] = {
                "current": round(current, 2),
                "predicted_15min": round(current + trend * 1, 2),
                "predicted_30min": round(predicted, 2),
                "trend": "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable",
                "level": self._get_level(predicted),
                "recommendation": self._get_recommendation(sec, predicted)
            }
        
        return {
            "predictions": predictions,
            "timestamp": datetime.utcnow().isoformat(),
            "timeframe": f"{minutes}_minutes",
            "summary": self._get_summary(predictions),
            "actionable_alerts": self._get_alerts(predictions)
        }
    
    def _get_level(self, density: float) -> str:
        """Get crowd level from density value."""
        if density < 0.3:
            return "low"
        elif density < 0.6:
            return "medium"
        elif density < 0.8:
            return "high"
        else:
            return "critical"
    
    def _get_recommendation(self, section: str, density: float) -> str:
        """Get actionable recommendation based on density."""
        if density > 0.8:
            return f"Open additional gates near {section}. Deploy 2 extra staff."
        elif density > 0.6:
            return f"Monitor {section} closely. Prepare to redirect crowd."
        elif density > 0.3:
            return f"Normal flow in {section}. Continue monitoring."
        else:
            return f"Low density in {section}. Consider closing some gates."
    
    def _get_summary(self, predictions: Dict) -> Dict:
        """Get summary of predictions."""
        levels = [p['level'] for p in predictions.values() if isinstance(p, dict)]
        return {
            "critical_sections": [k for k, v in predictions.items() if isinstance(v, dict) and v.get('level') == 'critical'],
            "high_sections": [k for k, v in predictions.items() if isinstance(v, dict) and v.get('level') == 'high'],
            "overall": "critical" if 'critical' in levels else "high" if 'high' in levels else "medium",
            "total_critical": sum(1 for v in predictions.values() if isinstance(v, dict) and v.get('level') == 'critical'),
            "total_high": sum(1 for v in predictions.values() if isinstance(v, dict) and v.get('level') == 'high')
        }
    
    def _get_alerts(self, predictions: Dict) -> List[Dict]:
        """Generate actionable alerts from predictions."""
        alerts = []
        for section, data in predictions.items():
            if isinstance(data, dict) and data.get('level') in ['critical', 'high']:
                alerts.append({
                    "section": section,
                    "level": data['level'],
                    "message": f"🚨 {section} congestion level: {data['level'].upper()}",
                    "timestamp": datetime.utcnow().isoformat()
                })
        return alerts
    
    async def get_realtime_dashboard(self) -> Dict[str, Any]:
        """Get real-time dashboard data for organizers."""
        sections_status = {}
        for section in self.sections:
            density = self.crowd_density.get(section, 0.0)
            sections_status[section] = {
                "density": round(density, 2),
                "level": self._get_level(density),
                "people_estimate": int(density * 5000)  # Rough estimate
            }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "sections": sections_status,
            "summary": {
                "total_attendance": sum(int(v['people_estimate']) for v in sections_status.values()),
                "critical_sections": [k for k, v in sections_status.items() if v['level'] == 'critical'],
                "high_sections": [k for k, v in sections_status.items() if v['level'] == 'high']
            }
        }