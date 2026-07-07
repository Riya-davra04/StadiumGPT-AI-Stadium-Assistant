from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from typing import Dict, Any, List
import logging
from datetime import datetime
import json
import os

# Import routes
from app.routes import (
    auth, navigation, crowds, queues,
    emergency, transport, volunteer, accessibility, digital_twin
)

# Import services
from app.services import (
    GeminiService, AnalyticsService,
    CrowdManagementService, QueueManagementService,
    EmergencyService, NavigationService, DigitalTwinService
)

# Import models
from app.models import User, StadiumData

# Import utilities
from app.utils.database import Database
from app.utils.websocket import ConnectionManager

# Import security middleware
from app.middleware.security import RateLimitMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# CREATE APP
# ============================================
app = FastAPI(
    title="StadiumGPT - AI Smart Stadium Assistant",
    description="Revolutionary AI-powered stadium operations platform for FIFA World Cup",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication endpoints"},
        {"name": "Navigation", "description": "Stadium navigation and routing"},
        {"name": "Crowd Management", "description": "Crowd analytics and heatmaps"},
        {"name": "Queue Management", "description": "Queue prediction and management"},
        {"name": "Emergency", "description": "Emergency handling and alerts"},
        {"name": "Transport", "description": "Transportation information"},
        {"name": "Volunteer", "description": "Volunteer support tools"},
        {"name": "Accessibility", "description": "Accessibility features"},
        {"name": "Digital Twin", "description": "Stadium simulation and predictions"}
    ]
)


# ============================================
# GLOBAL EXCEPTION HANDLER
# ============================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================
# SECURITY MIDDLEWARE
# ============================================
class CustomSecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self' data:; "
            "connect-src 'self' https://cdn.jsdelivr.net https://*.jsdelivr.net; "
            "frame-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=()"
        return response


# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://stadiumgpt.vercel.app",
    "https://stadiumgpt-ai-stadium-assistant.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(CustomSecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, limit=60, window=60)


# ============================================
# INITIALIZE SERVICES
# ============================================
gemini_service = GeminiService()
crowd_service = CrowdManagementService()
queue_service = QueueManagementService()
emergency_service = EmergencyService()
navigation_service = NavigationService()
digital_twin_service = DigitalTwinService()
db = Database()
manager = ConnectionManager()


# ============================================
# INCLUDE ROUTERS
# ============================================
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
app.include_router(crowds.router, prefix="/api/crowds", tags=["Crowd Management"])
app.include_router(queues.router, prefix="/api/queues", tags=["Queue Management"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency"])
app.include_router(transport.router, prefix="/api/transport", tags=["Transport"])
app.include_router(volunteer.router, prefix="/api/volunteer", tags=["Volunteer"])
app.include_router(accessibility.router, prefix="/api/accessibility", tags=["Accessibility"])
app.include_router(digital_twin.router, prefix="/api/digital-twin", tags=["Digital Twin"])


# ============================================
# ENDPOINTS
# ============================================
@app.get("/openapi.json")
async def get_openapi():
    return app.openapi()


@app.get("/")
async def root():
    return {
        "name": "StadiumGPT",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "websocket": "/ws/{client_id}"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": await db.check_connection(),
            "gemini": await gemini_service.check_health(),
            "websocket": len(manager.active_connections)
        }
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "crowd_update":
                result = await crowd_service.analyze_crowd(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "crowd_response", "data": result},
                    client_id
                )
                await manager.broadcast({
                    "type": "crowd_broadcast",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            elif message_type == "emergency":
                result = await emergency_service.handle_emergency(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "emergency_response", "data": result},
                    client_id
                )
                await manager.broadcast({
                    "type": "emergency_alert",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            elif message_type == "navigation":
                route = await navigation_service.find_route(
                    start=data.get("start"),
                    end=data.get("end"),
                    preferences=data.get("preferences", []),
                    accessibility=data.get("accessibility", False)
                )
                await manager.send_personal_message(
                    {"type": "navigation_response", "data": route.__dict__},
                    client_id
                )
                
            elif message_type == "queue_query":
                result = await queue_service.predict_wait_time(data.get("establishment"))
                await manager.send_personal_message(
                    {"type": "queue_response", "data": result},
                    client_id
                )
                
            elif message_type == "chat":
                context = data.get("context", {})
                query = data.get("content", "")
                result = await gemini_service.process_query(query, context)
                await manager.send_personal_message(
                    {"type": "ai_response", "content": result.get("response", "")},
                    client_id
                )
                
            else:
                await manager.send_personal_message(
                    {"type": "error", "message": f"Unknown message type: {message_type}"},
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.send_personal_message(
            {"type": "error", "message": str(e)},
            client_id
        )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down StadiumGPT...")
    await manager.close_all_connections()
    await db.close_connection()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        workers=4
    )