"""
Rate Limiting Middleware
=========================
Prevents API abuse by limiting requests per IP.
"""

import os
import time
from typing import Dict, List
from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""
    
    def __init__(self, app, limit: int = 60, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next):
        # Skip in test environment
        if os.getenv("ENVIRONMENT") == "test":
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.window]
        
        # Check limit
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.limit:
            return Response(
                content="Rate limit exceeded. Try again later.",
                status_code=429,
                headers={"Retry-After": str(self.window)}
            )
        
        # Add current request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(now)
        
        return await call_next(request)