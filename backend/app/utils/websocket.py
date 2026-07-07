"""WebSocket connection manager."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage active WebSocket connections keyed by client id."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []
        self.connections_map: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        # Replace any stale connection for this client id.
        if client_id in self.connections_map:
            self.disconnect(client_id)
        self.active_connections.append(websocket)
        self.connections_map[client_id] = websocket
        logger.info(
            "Client %s connected. Total connections: %d",
            client_id,
            len(self.active_connections),
        )

    def disconnect(self, client_id: str) -> None:
        websocket = self.connections_map.pop(client_id, None)
        if websocket and websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(
                "Client %s disconnected. Total connections: %d",
                client_id,
                len(self.active_connections),
            )

    async def send_personal_message(self, message: Dict[str, Any], client_id: str) -> None:
        websocket = self.connections_map.get(client_id)
        if not websocket:
            logger.warning("Client %s not found for personal message", client_id)
            return
        try:
            await websocket.send_json(message)
        except Exception as exc:
            logger.error("Personal message to %s failed: %s", client_id, exc)
            self.disconnect(client_id)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        message["broadcast_time"] = datetime.now(timezone.utc).isoformat()
        stale: List[str] = []
        for client_id, websocket in list(self.connections_map.items()):
            try:
                await websocket.send_json(message)
            except Exception as exc:
                logger.error("Broadcast to %s failed: %s", client_id, exc)
                stale.append(client_id)
        for client_id in stale:
            self.disconnect(client_id)

    async def broadcast_to_role(self, message: Dict[str, Any], role: str) -> None:
        message["target_role"] = role
        await self.broadcast(message)

    async def close_all_connections(self) -> None:
        for websocket in list(self.active_connections):
            try:
                await websocket.close()
            except Exception as exc:
                logger.warning("Error closing connection: %s", exc)
        self.active_connections.clear()
        self.connections_map.clear()
        logger.info("All connections closed")

    def get_connection_count(self) -> int:
        return len(self.active_connections)

    def get_active_clients(self) -> List[str]:
        return list(self.connections_map.keys())