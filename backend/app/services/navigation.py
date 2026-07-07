from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Route:
    path: List[str]
    estimated_time: int
    accessibility_info: Optional[Dict]
    crowd_level: str
    alternatives: List[Dict]

class NavigationService:
    def __init__(self):
        self.stadium_graph = self._build_stadium_graph()
        
    def _build_stadium_graph(self) -> Dict:
        """Build stadium navigation graph"""
        return {
            "gates": {
                "A": {"position": [0, 0], "connections": ["concourse_main", "vip_lounge"]},
                "B": {"position": [10, 0], "connections": ["concourse_main", "food_court_a"]},
                "C": {"position": [5, -5], "connections": ["concourse_main", "access_ramp"]},
                "D": {"position": [15, 5], "connections": ["concourse_main", "staff_area"]},
                "E": {"position": [0, 10], "connections": ["concourse_main", "emergency_exit"]}
            },
            "sections": {
                "A1": {"position": [2, 2], "connections": ["gate_a"]},
                "A2": {"position": [4, 3], "connections": ["gate_a", "concourse_main"]},
                "B1": {"position": [12, 2], "connections": ["gate_b"]},
                "B2": {"position": [14, 3], "connections": ["gate_b", "concourse_main"]},
                "C1": {"position": [6, -2], "connections": ["gate_c"]},
                "C2": {"position": [8, -3], "connections": ["gate_c", "concourse_main"]}
            },
            "facilities": {
                "food_court_a": {"position": [3, -3], "connections": ["concourse_main"]},
                "food_court_b": {"position": [13, -3], "connections": ["concourse_main"]},
                "food_court_c": {"position": [8, -5], "connections": ["concourse_main"]},
                "restroom_1": {"position": [1, 5], "connections": ["concourse_main"]},
                "restroom_2": {"position": [9, 5], "connections": ["concourse_main"]},
                "restroom_3": {"position": [16, 5], "connections": ["concourse_main"]},
                "first_aid": {"position": [7, 0], "connections": ["concourse_main"]},
                "guest_services": {"position": [8, 0], "connections": ["concourse_main"]}
            }
        }
    
    async def find_route(
        self,
        start: str,
        end: str,
        preferences: List[str] = None,
        accessibility: bool = False
    ) -> Route:
        """Find optimal route"""
        try:
            start_pos = self._get_position(start)
            end_pos = self._get_position(end)
            
            if not start_pos or not end_pos:
                return Route(
                    path=[],
                    estimated_time=0,
                    accessibility_info=None,
                    crowd_level="unknown",
                    alternatives=[]
                )
            
            path = self._calculate_path(start, end)
            distance = self._calculate_distance(start_pos, end_pos)
            time_estimate = distance * 2
            
            accessibility_info = None
            if accessibility:
                accessibility_info = await self._get_accessibility_info(path)
            
            alternatives = await self._get_alternatives(start, end)
            
            return Route(
                path=path,
                estimated_time=time_estimate,
                accessibility_info=accessibility_info,
                crowd_level="medium",
                alternatives=alternatives
            )
        except Exception as e:
            logger.error(f"Route finding error: {e}")
            raise
    
    def _get_position(self, location: str) -> Optional[List[float]]:
        """Get coordinates for a location"""
        graph = self.stadium_graph
        for category in graph.values():
            if location in category:
                return category[location]["position"]
        return None
    
    def _calculate_path(self, start: str, end: str) -> List[str]:
        """Calculate path using BFS or simple heuristic"""
        return [start, "concourse_main", end]
    
    def _calculate_distance(self, pos1: List[float], pos2: List[float]) -> float:
        """Calculate Euclidean distance"""
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    async def _get_accessibility_info(self, path: List[str]) -> Dict:
        """Get accessibility information for a route"""
        return {
            "wheelchair_accessible": True,
            "elevator_available": "elevator" in path,
            "ramp_available": "ramp" in path,
            "accessible_restrooms": "restroom_1" in path,
            "visual_guidance": "available"
        }
    
    async def _get_alternatives(self, start: str, end: str) -> List[Dict]:
        """Get alternative routes"""
        return [
            {"path": [start, "concourse_main", "food_court_a", end], "time": 8},
            {"path": [start, "gate_a", "concourse_main", end], "time": 10}
        ]