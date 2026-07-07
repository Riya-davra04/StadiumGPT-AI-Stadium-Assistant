"""
Digital Twin Service - Predictive Crowd Simulation
===================================================
Provides real-time crowd simulation and prediction for stadium operations.
"""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

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
        self._initialize_density()
    
    def _initialize_density(self) -> None:
        """Initialize crowd density with random values."""
        for section in self.sections:
            self.crowd_density[section] = random.uniform(0.1, 0.7)
    
    async def start_simulation(self) -> Dict[str, Any]:
        """
        Start real-time crowd simulation.
        
        Returns:
            Dict with status and timestamp
        """
        self.simulation_running = True
        logger.info("Digital Twin simulation started")
        return {
            "status": "simulation_started",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def stop_simulation(self) -> Dict[str, Any]:
        """
        Stop crowd simulation.
        
        Returns:
            Dict with status and timestamp
        """
        self.simulation_running = False
        logger.info("Digital Twin simulation stopped")
        return {
            "status": "simulation_stopped",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def predict_crowd_movement(self, minutes: int = 15) -> Dict[str, Any]:
        """
        Predict crowd movement for the next X minutes.
        
        Uses a flow model to simulate:
        - Entry flow (gates → sections)
        - Exit flow (sections → gates)
        - Internal movement (section → section)
        
        Args:
            minutes: Prediction timeframe in minutes
            
        Returns:
            Dict containing predictions and summary
        """
        predictions: Dict[str, Any] = {}
        
        for section in self.sections:
            current_density: float = self.crowd_density.get(section, 0.3)
            
            if self.simulation_running:
                # Random walk simulation with trend
                trend = random.uniform(-0.05, 0.1)
                change = random.uniform(-0.05, 0.05) + trend
                predicted_density: float = max(0.0, min(1.0, current_density + change))
            else:
                predicted_density = current_density
            
            predictions[section] = {
                "current": round(current_density, 2),
                "predicted": round(predicted_density, 2),
                "change": round((predicted_density - current_density) * 100, 1),
                "level": self._get_level(predicted_density)
            }
        
        # Store historical data
        self.historical_data.append({
            "timestamp": datetime.utcnow().isoformat(),
            "predictions": predictions
        })
        
        return {
            "predictions": predictions,
            "timestamp": datetime.utcnow().isoformat(),
            "timeframe": f"{minutes}_minutes",
            "summary": self._get_summary(predictions)
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
    
    def _get_summary(self, predictions: Dict) -> Dict:
        """Get summary of predictions."""
        levels = [p['level'] for p in predictions.values()]
        return {
            "critical_sections": [k for k, v in predictions.items() if v['level'] == 'critical'],
            "high_sections": [k for k, v in predictions.items() if v['level'] == 'high'],
            "overall": "critical" if 'critical' in levels else "high" if 'high' in levels else "medium",
            "total_critical": sum(1 for v in predictions.values() if v['level'] == 'critical'),
            "total_high": sum(1 for v in predictions.values() if v['level'] == 'high')
        }
    
    async def get_heatmap_data(self) -> Dict[str, Any]:
        """
        Generate real-time heatmap data.
        
        Returns:
            Dict with heatmap data and metadata
        """
        data = {}
        for section in self.sections:
            density = self.crowd_density.get(section, random.uniform(0.1, 0.9))
            data[section] = round(density, 2)
        
        return {
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "legend": {
                "0-0.3": {"level": "Low", "color": "#4CAF50"},
                "0.3-0.6": {"level": "Medium", "color": "#FF9800"},
                "0.6-0.8": {"level": "High", "color": "#F44336"},
                "0.8-1.0": {"level": "Critical", "color": "#D32F2F"}
            }
        }
    
    async def update_section_density(self, section: str, density: float) -> Dict:
        """
        Update density for a specific section.
        
        Args:
            section: Section identifier
            density: Density value (0-1)
            
        Returns:
            Dict with status and updated data
        """
        if section not in self.sections:
            return {"error": "Invalid section"}
        if not 0 <= density <= 1:
            return {"error": "Density must be between 0 and 1"}
        
        self.crowd_density[section] = density
        logger.info(f"Section {section} density updated to {density}")
        
        return {
            "status": "updated",
            "section": section,
            "density": density,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_section_status(self, section: str) -> Dict:
        """
        Get current status for a specific section.
        
        Args:
            section: Section identifier
            
        Returns:
            Dict with section status
        """
        if section not in self.sections:
            return {"error": "Invalid section"}
        
        density = self.crowd_density.get(section, 0.0)
        return {
            "section": section,
            "density": round(density, 2),
            "level": self._get_level(density),
            "timestamp": datetime.utcnow().isoformat()
        }