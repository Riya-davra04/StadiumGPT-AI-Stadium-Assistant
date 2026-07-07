"""API Documentation generator"""

from typing import Dict, Any

def generate_api_docs() -> Dict[str, Any]:
    """Generate API documentation dictionary"""
    return {
        "name": "StadiumGPT API",
        "version": "1.0.0",
        "description": "AI-powered smart stadium assistant",
        "endpoints": {
            "auth": {
                "register": {
                    "method": "POST",
                    "path": "/api/auth/register",
                    "description": "Register a new user",
                    "body": {
                        "name": "string (required)",
                        "email": "string (required)",
                        "password": "string (required)",
                        "role": "string (optional, default: fan)",
                        "language": "string (optional, default: English)"
                    }
                },
                "login": {
                    "method": "POST",
                    "path": "/api/auth/login",
                    "description": "Login user",
                    "body": {
                        "email": "string (required)",
                        "password": "string (required)"
                    }
                },
                "me": {
                    "method": "GET",
                    "path": "/api/auth/me",
                    "description": "Get current user profile",
                    "auth": "Bearer token required"
                }
            },
            "navigation": {
                "route": {
                    "method": "GET",
                    "path": "/api/navigation/route",
                    "description": "Get route between two locations",
                    "auth": "Bearer token required"
                }
            },
            "crowds": {
                "heatmap": {
                    "method": "GET",
                    "path": "/api/crowds/heatmap",
                    "description": "Get crowd heatmap data",
                    "auth": "Bearer token required"
                }
            },
            "queues": {
                "all": {
                    "method": "GET",
                    "path": "/api/queues/all",
                    "description": "Get all queue status",
                    "auth": "Bearer token required"
                }
            },
            "emergency": {
                "report": {
                    "method": "POST",
                    "path": "/api/emergency/report",
                    "description": "Report an emergency",
                    "auth": "Bearer token required"
                }
            },
            "transport": {
                "options": {
                    "method": "GET",
                    "path": "/api/transport/options",
                    "description": "Get transport options",
                    "auth": "Bearer token required"
                }
            },
            "accessibility": {
                "features": {
                    "method": "GET",
                    "path": "/api/accessibility/features",
                    "description": "Get accessibility features",
                    "auth": "Bearer token required"
                }
            }
        }
    }