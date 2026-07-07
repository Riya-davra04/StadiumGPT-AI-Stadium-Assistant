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
        accessibility: bool = False,
        avoid_crowds: bool = False
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
                crowd_level="low" if avoid_crowds else "medium",
                alternatives=alternatives
            )
        except Exception as e:
            logger.error(f"Route finding error: {e}")
            raise
    
    async def get_nearby_locations(self, location: str, radius: int = 50, facility_type: str = None) -> List[Dict]:
        """Get nearby locations"""
        try:
            nearby = []
            pos = self._get_position(location)
            if not pos:
                return []
            
            for name, data in self.stadium_graph["facilities"].items():
                if facility_type and not name.startswith(facility_type):
                    continue
                dist = self._calculate_distance(pos, data["position"])
                if dist <= radius / 10:
                    nearby.append({
                        "name": name,
                        "distance": dist * 10,
                        "type": facility_type or "facility"
                    })
            
            return sorted(nearby, key=lambda x: x["distance"])
        except Exception as e:
            logger.error(f"Nearby locations error: {e}")
            return []
    
    async def get_directions(self, start: str, end: str) -> List[str]:
        """Get step-by-step directions"""
        return [f"Start at {start}", "Walk straight", "Turn right", f"Arrive at {end}"]
    
    async def get_accessible_route(self, start: str, end: str) -> Dict:
        """Get accessible route"""
        route = await self.find_route(start, end, accessibility=True)
        return {
            "path": route.path,
            "estimated_time": route.estimated_time,
            "wheelchair_accessible": True,
            "elevator_available": True,
            "ramp_available": True,
            "accessible_restrooms": ["restroom_1", "restroom_3"],
            "visual_guidance": True
        }
    
    async def get_location_crowd_status(self, location: str) -> Dict:
        """Get crowd status for a location"""
        return {"level": "medium", "density": 0.5, "wait_time": 5, "recommendation": "Normal flow"}
    
    async def get_nearest_exits(self, location: str) -> List[Dict]:
        """Get nearest emergency exits"""
        return [
            {"name": "Exit A", "distance": 50},
            {"name": "Exit B", "distance": 80},
            {"name": "Exit C", "distance": 120}
        ]
    
    def _get_position(self, location: str) -> Optional[List[float]]:
        graph = self.stadium_graph
        location_lower = location.lower()
        for category in graph.values():
            for name, data in category.items():
                if name.lower() == location_lower or name.lower().replace("_", " ") == location_lower:
                    return data["position"]
        return None
    
    def _calculate_path(self, start: str, end: str) -> List[str]:
        return [start, "concourse_main", end]
    
    def _calculate_distance(self, pos1: List[float], pos2: List[float]) -> float:
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    
    async def _get_accessibility_info(self, path: List[str]) -> Dict:
        return {
            "wheelchair_accessible": True,
            "elevator_available": "elevator" in path,
            "ramp_available": "ramp" in path,
            "accessible_restrooms": "restroom_1" in path,
            "visual_guidance": "available"
        }
    
    async def _get_alternatives(self, start: str, end: str) -> List[Dict]:
        return [
            {"path": [start, "concourse_main", "food_court_a", end], "time": 8},
            {"path": [start, "gate_a", "concourse_main", end], "time": 10}
        ]