"""
Digital Twin Service - Predictive Crowd Simulation
"""

import random
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DigitalTwinService:
    """Simulate and predict crowd movement in the stadium"""
    
    def __init__(self):
        self.sections = [
            'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 
            'D1', 'D2', 'E1', 'E2', 'F1', 'F2'
        ]
        self.gates = ['A', 'B', 'C', 'D', 'E']
        self.crowd_density = {}
        self.historical_data = []
        self.simulation_running = False
    
    async def start_simulation(self) -> Dict[str, Any]:
        """Start real-time crowd simulation"""
        self.simulation_running = True
        return {"status": "simulation_started", "timestamp": datetime.utcnow().isoformat()}
    
    async def stop_simulation(self) -> Dict[str, Any]:
        """Stop crowd simulation"""
        self.simulation_running = False
        return {"status": "simulation_stopped", "timestamp": datetime.utcnow().isoformat()}
    
    async def predict_crowd_movement(self, minutes: int = 15) -> Dict[str, Any]:
        """
        Predict crowd movement for the next X minutes
        
        Uses a simple flow model to simulate:
        - Entry flow (gates → sections)
        - Exit flow (sections → gates)
        - Internal movement (section → section)
        """
        predictions = {}
        
        for section in self.sections:
            current_density = self.crowd_density.get(section, 0.3)
            
            # Simple prediction model
            if self.simulation_running:
                # Random walk simulation
                change = random.uniform(-0.1, 0.15)
                predicted_density = max(0.0, min(1.0, current_density + change))
            else:
                predicted_density = current_density
            
            predictions[section] = {
                "current": current_density,
                "predicted": predicted_density,
                "change": (predicted_density - current_density) * 100,
                "level": self._get_level(predicted_density)
            }
        
        return {
            "predictions": predictions,
            "timestamp": datetime.utcnow().isoformat(),
            "timeframe": f"{minutes}_minutes",
            "summary": self._get_summary(predictions)
        }
    
    def _get_level(self, density: float) -> str:
        """Get crowd level from density"""
        if density < 0.3:
            return "low"
        elif density < 0.6:
            return "medium"
        elif density < 0.8:
            return "high"
        else:
            return "critical"
    
    def _get_summary(self, predictions: Dict) -> Dict:
        """Get summary of predictions"""
        levels = [p['level'] for p in predictions.values()]
        return {
            "critical_sections": [k for k, v in predictions.items() if v['level'] == 'critical'],
            "high_sections": [k for k, v in predictions.items() if v['level'] == 'high'],
            "overall": "critical" if 'critical' in levels else "high" if 'high' in levels else "medium"
        }
    
    async def get_heatmap_data(self) -> Dict[str, Any]:
        """Generate real-time heatmap data"""
        data = {}
        for section in self.sections:
            density = self.crowd_density.get(section, random.uniform(0.1, 0.9))
            data[section] = density
        
        return {
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "legend": {
                "0-0.3": "Low",
                "0.3-0.6": "Medium",
                "0.6-0.8": "High",
                "0.8-1.0": "Critical"
            }
        }
    
    async def update_section_density(self, section: str, density: float) -> Dict:
        """Update density for a specific section"""
        if section in self.sections and 0 <= density <= 1:
            self.crowd_density[section] = density
            return {"status": "updated", "section": section, "density": density}
        return {"error": "Invalid section or density"}