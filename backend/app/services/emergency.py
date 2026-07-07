from typing import Dict, List, Any
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)

class EmergencyService:
    def __init__(self):
        self.emergency_stations = [
            {"id": "station_1", "name": "First Aid Station A", "location": "Section A", "status": "available"},
            {"id": "station_2", "name": "First Aid Station B", "location": "Section C", "status": "available"},
            {"id": "station_3", "name": "First Aid Station C", "location": "Section E", "status": "available"}
        ]
        self.medical_team = [
            {"id": "team_1", "name": "Medical Team Alpha", "available": True},
            {"id": "team_2", "name": "Medical Team Bravo", "available": True}
        ]
        self.active_alerts = []
    
    async def handle_emergency(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation"""
        try:
            emergency_type = data.get("type", "medical")
            location = data.get("location", "unknown")
            severity = data.get("severity", "medium")
            description = data.get("description", "")
            
            alert = {
                "id": f"emergency_{datetime.utcnow().timestamp()}",
                "type": emergency_type,
                "location": location,
                "severity": severity,
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "active"
            }
            
            self.active_alerts.append(alert)
            response = await self._determine_response(alert)
            await self._send_notifications(alert, response)
            
            alert["response"] = response
            alert["status"] = "responded"
            
            return {
                "alert": alert,
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Emergency handling error: {e}")
            return {"error": "Could not process emergency"}
    
    async def _determine_response(self, alert: Dict) -> Dict:
        """Determine appropriate emergency response"""
        response = {
            "actions": [],
            "teams_dispatched": [],
            "instructions": []
        }
        
        if alert["severity"] == "high":
            response["actions"].append("Immediate medical response needed")
            response["teams_dispatched"] = [team["name"] for team in self.medical_team]
            response["instructions"].append("Clear the area immediately")
            response["instructions"].append("Send stretcher team")
        elif alert["severity"] == "medium":
            response["actions"].append("Medical team alerted")
            response["teams_dispatched"] = [self.medical_team[0]["name"]]
            response["instructions"].append("Keep the area clear")
            response["instructions"].append("Wait for medical team")
        else:
            response["actions"].append("First aid station alerted")
            response["instructions"].append("Direct to nearest first aid station")
        
        nearby_station = await self._find_nearest_station(alert["location"])
        if nearby_station:
            response["nearest_station"] = nearby_station
            response["instructions"].append(f"Nearest station: {nearby_station['name']}")
        
        return response
    
    async def _find_nearest_station(self, location: str) -> Dict:
        """Find nearest emergency station"""
        return self.emergency_stations[0]
    
    async def _send_notifications(self, alert: Dict, response: Dict):
        """Send notifications to relevant parties"""
        logger.info(f"Emergency alert: {alert}")
        logger.info(f"Response: {response}")
        await asyncio.sleep(0.5)
        return True
    
    async def get_active_alerts(self) -> List[Dict]:
        """Get all active emergency alerts"""
        return [alert for alert in self.active_alerts if alert["status"] != "resolved"]
    
    async def resolve_emergency(self, alert_id: str) -> Dict:
        """Resolve an emergency"""
        for alert in self.active_alerts:
            if alert["id"] == alert_id:
                alert["status"] = "resolved"
                alert["resolved_at"] = datetime.utcnow().isoformat()
                return {
                    "alert": alert,
                    "message": "Emergency resolved successfully"
                }
        
        return {"error": "Alert not found"}