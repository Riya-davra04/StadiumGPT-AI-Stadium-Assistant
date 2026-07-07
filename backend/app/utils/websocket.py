from typing import List, Dict, Any
from fastapi import WebSocket
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connections_map: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Add a new connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connections_map[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, client_id: str):
        """Remove a connection"""
        try:
            if client_id in self.connections_map:
                websocket = self.connections_map[client_id]
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)
                del self.connections_map[client_id]
                logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
    
    async def send_personal_message(self, message: Dict[str, Any], client_id: str):
        """Send a message to a specific client"""
        try:
            if client_id in self.connections_map:
                websocket = self.connections_map[client_id]
                await websocket.send_json(message)
            else:
                logger.warning(f"Client {client_id} not found for personal message")
        except Exception as e:
            logger.error(f"Personal message error: {e}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Send a message to all connected clients"""
        message["broadcast_time"] = datetime.utcnow().isoformat()
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast error to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            if connection in self.active_connections:
                self.active_connections.remove(connection)
    
    async def broadcast_to_role(self, message: Dict[str, Any], role: str):
        """Broadcast message to clients with a specific role"""
        message["target_role"] = role
        message["broadcast_time"] = datetime.utcnow().isoformat()
        
        for client_id, websocket in self.connections_map.items():
            try:
                # In production, check client's role from authentication
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Role broadcast error: {e}")
    
    async def close_all_connections(self):
        """Close all connections"""
        for connection in self.active_connections:
            try:
                await connection.close()
            except Exception as e:
                logger.error(f"Close connection error: {e}")
        
        self.active_connections.clear()
        self.connections_map.clear()
        logger.info("All connections closed")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_active_clients(self) -> List[str]:
        """Get list of active client IDs"""
        return list(self.connections_map.keys())