from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from typing import Dict, Any, List
import logging
from datetime import datetime
import json

# Import routes
from app.routes import (
    auth, 
    navigation, 
    crowds, 
    queues,
    emergency, 
    transport, 
    volunteer, 
    accessibility
)

# Import services
from app.services import (
    GeminiService, 
    AnalyticsService,
    CrowdManagementService,
    QueueManagementService,
    EmergencyService,
    NavigationService
)

# Import models
from app.models import User
# or
from app.models import User, StadiumLayout

# Import utilities
from app.utils.database import Database
from app.utils.websocket import ConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StadiumGPT - AI Smart Stadium Assistant",
    description="Revolutionary AI-powered stadium operations platform for FIFA World Cup",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication endpoints"},
        {"name": "Navigation", "description": "Stadium navigation and routing"},
        {"name": "Crowd Management", "description": "Crowd analytics and heatmaps"},
        {"name": "Queue Management", "description": "Queue prediction and management"},
        {"name": "Emergency", "description": "Emergency handling and alerts"},
        {"name": "Transport", "description": "Transportation information"},
        {"name": "Volunteer", "description": "Volunteer support tools"},
        {"name": "Accessibility", "description": "Accessibility features"}
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure for production
)

# ============================================
# ✅ FIXED: Initialize services only ONCE
# ============================================
gemini_service = GeminiService()
crowd_service = CrowdManagementService()
queue_service = QueueManagementService()
emergency_service = EmergencyService()
navigation_service = NavigationService()
db = Database()  # ✅ Only ONE database instance
manager = ConnectionManager()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
app.include_router(crowds.router, prefix="/api/crowds", tags=["Crowd Management"])
app.include_router(queues.router, prefix="/api/queues", tags=["Queue Management"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency"])
app.include_router(transport.router, prefix="/api/transport", tags=["Transport"])
app.include_router(volunteer.router, prefix="/api/volunteer", tags=["Volunteer"])
app.include_router(accessibility.router, prefix="/api/accessibility", tags=["Accessibility"])

# WebSocket for real-time updates
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Handle WebSocket connections for real-time updates"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "crowd_update":
                # Process crowd data
                result = await crowd_service.analyze_crowd(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "crowd_response", "data": result},
                    client_id
                )
                # Broadcast to all connected clients
                await manager.broadcast({
                    "type": "crowd_broadcast",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            elif message_type == "emergency":
                # Handle emergency
                result = await emergency_service.handle_emergency(data.get("data", {}))
                await manager.send_personal_message(
                    {"type": "emergency_response", "data": result},
                    client_id
                )
                # Broadcast emergency to all clients
                await manager.broadcast({
                    "type": "emergency_alert",
                    "data": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            elif message_type == "navigation":
                # Process navigation request
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
                # Get queue information
                result = await queue_service.predict_wait_time(data.get("establishment"))
                await manager.send_personal_message(
                    {"type": "queue_response", "data": result},
                    client_id
                )
                
            elif message_type == "chat":
                # Process chat message with Gemini
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

# Root endpoint
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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": await db.check_connection(),
            "gemini": await gemini_service.check_health(),
            "websocket": len(manager.active_connections)
        }
    }

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
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