"""
StadiumGPT - Main Application Entry Point
==========================================
FIFA World Cup Smart Stadium Assistant (Challenge 4).

Chosen vertical: Smart Stadiums & Tournament Operations.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Routes
from app.routes import (
    accessibility,
    analytics,
    auth,
    crowds,
    digital_twin,
    emergency,
    monitoring,
    navigation,
    predictive,
    queues,
    transport,
    volunteer,
)

# Services
from app.services import (
    CrowdManagementService,
    DigitalTwinService,
    EmergencyService,
    GeminiService,
    NavigationService,
    QueueManagementService,
)

# Middleware
from app.middleware.security import RateLimitMiddleware, SecurityHeadersMiddleware
from app.utils.database import Database
from app.utils.websocket import ConnectionManager

# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _utcnow_iso() -> str:
    """Return current UTC time in ISO-8601 format (timezone-aware)."""
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------
# Shared service singletons
# --------------------------------------------------------------------------
gemini_service = GeminiService()
crowd_service = CrowdManagementService()
queue_service = QueueManagementService()
emergency_service = EmergencyService()
navigation_service = NavigationService()
digital_twin_service = DigitalTwinService()
db = Database()
manager = ConnectionManager()


# --------------------------------------------------------------------------
# Lifespan (replaces deprecated @app.on_event)
# --------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(_: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    logger.info("Starting StadiumGPT service...")
    yield
    logger.info("Shutting down StadiumGPT...")
    await manager.close_all_connections()
    await db.close_connection()


# --------------------------------------------------------------------------
# App
# --------------------------------------------------------------------------
app = FastAPI(
    title="StadiumGPT - AI Smart Stadium Assistant",
    description="AI-powered stadium operations platform for FIFA World Cup.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication endpoints"},
        {"name": "Navigation", "description": "Stadium navigation and routing"},
        {"name": "Crowd Management", "description": "Crowd analytics and heatmaps"},
        {"name": "Queue Management", "description": "Queue prediction and management"},
        {"name": "Emergency", "description": "Emergency handling and alerts"},
        {"name": "Transport", "description": "Transportation information"},
        {"name": "Volunteer", "description": "Volunteer support tools"},
        {"name": "Accessibility", "description": "Accessibility features"},
        {"name": "Digital Twin", "description": "Stadium simulation and predictions"},
        {"name": "Analytics", "description": "Analytics and insights"},
        {"name": "Predictive Analytics", "description": "15/60 min crowd predictions"},
        {"name": "Monitoring", "description": "Real-time stadium monitoring"},
    ],
)


# --------------------------------------------------------------------------
# Global exception handler
# --------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return a safe JSON response for any unhandled exception."""
    logger.error("Unhandled exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An unexpected error occurred", "timestamp": _utcnow_iso()},
    )


# --------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8000,"
        "https://stadiumgpt.vercel.app,"
        "https://stadiumgpt-ai-stadium-assistant.onrender.com,"
        "https://stadiumgpt-ai-stadium-assistant-1.onrender.com",
    ).split(",")
    if o.strip()
]

TRUSTED_HOSTS = [
    h.strip() for h in os.getenv("TRUSTED_HOSTS", "*").split(",") if h.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=TRUSTED_HOSTS)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    limit=int(os.getenv("RATE_LIMIT_REQUESTS", "60")),
    window=int(os.getenv("RATE_LIMIT_WINDOW", "60")),
)


# --------------------------------------------------------------------------
# Routers
# --------------------------------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
app.include_router(crowds.router, prefix="/api/crowds", tags=["Crowd Management"])
app.include_router(queues.router, prefix="/api/queues", tags=["Queue Management"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency"])
app.include_router(transport.router, prefix="/api/transport", tags=["Transport"])
app.include_router(volunteer.router, prefix="/api/volunteer", tags=["Volunteer"])
app.include_router(accessibility.router, prefix="/api/accessibility", tags=["Accessibility"])
app.include_router(digital_twin.router, prefix="/api/digital-twin", tags=["Digital Twin"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(predictive.router, prefix="/api/predictive", tags=["Predictive Analytics"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])


# --------------------------------------------------------------------------
# Basic endpoints
# --------------------------------------------------------------------------
@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """Return service metadata."""
    return {
        "name": "StadiumGPT",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": _utcnow_iso(),
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "websocket": "/ws/{client_id}"
        },
    }


@app.get("/health", tags=["Root"])
async def health_check() -> Dict[str, Any]:
    """Report service health for orchestrators."""
    return {
        "status": "healthy",
        "timestamp": _utcnow_iso(),
        "services": {
            "database": await db.check_connection(),
            "gemini": await gemini_service.check_health(),
            "websocket": len(manager.active_connections),
        },
    }


@app.get("/openapi.json", tags=["Root"])
async def get_openapi() -> Dict[str, Any]:
    """Serve OpenAPI JSON."""
    return app.openapi()


# --------------------------------------------------------------------------
# WebSocket
# --------------------------------------------------------------------------
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:
    """Bidirectional real-time channel for the stadium assistant."""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "crowd_update":
                result = await crowd_service.analyze_crowd(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "crowd_response", "data": result}, client_id
                )
                await manager.broadcast(
                    {"type": "crowd_broadcast", "data": result, "timestamp": _utcnow_iso()}
                )

            elif message_type == "emergency":
                result = await emergency_service.handle_emergency(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "emergency_response", "data": result}, client_id
                )
                await manager.broadcast(
                    {"type": "emergency_alert", "data": result, "timestamp": _utcnow_iso()}
                )

            elif message_type == "navigation":
                route = await navigation_service.find_route(
                    start=data.get("start"),
                    end=data.get("end"),
                    preferences=data.get("preferences", []),
                    accessibility=data.get("accessibility", False),
                )
                await manager.send_personal_message(
                    {"type": "navigation_response", "data": route.__dict__}, client_id
                )

            elif message_type == "queue_query":
                result = await queue_service.predict_wait_time(data.get("establishment"))
                await manager.send_personal_message(
                    {"type": "queue_response", "data": result}, client_id
                )

            elif message_type == "chat":
                context = data.get("context", {})
                query = data.get("content", "")
                result = await gemini_service.process_query(query, context)
                await manager.send_personal_message(
                    {"type": "ai_response", "content": result.get("response", "")}, client_id
                )

            else:
                await manager.send_personal_message(
                    {"type": "error", "message": f"Unknown message type: {message_type}"},
                    client_id,
                )

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info("Client %s disconnected", client_id)
    except Exception as exc:
        logger.error("WebSocket error for %s: %s", client_id, exc)
        try:
            await manager.send_personal_message({"type": "error", "message": str(exc)}, client_id)
        except Exception:
            pass
        finally:
            manager.disconnect(client_id)


# --------------------------------------------------------------------------
# Main entry point
# --------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("AUTO_RELOAD", "False").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )