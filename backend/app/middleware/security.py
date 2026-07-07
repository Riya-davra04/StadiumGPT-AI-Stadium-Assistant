"""
Security middleware for FastAPI
================================
Provides security headers and rate limiting for the StadiumGPT API.
"""

import os
import time
from typing import Dict

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.
    
    Headers added:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Strict-Transport-Security: max-age=31536000; includeSubDomains
    - Content-Security-Policy: Allows Swagger UI and CDN resources
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: geolocation=()
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # ✅ Updated CSP to allow Swagger UI and CDN resources
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


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse.
    
    Limits requests per IP address within a time window.
    Skips rate limiting in test environment.
    
    Attributes:
        limit (int): Maximum number of requests allowed per window
        window (int): Time window in seconds
        requests (Dict[str, list]): Stores request timestamps per IP
    """
    
    def __init__(self, app, limit: int = 60, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        # ✅ Skip rate limiting in test environment
        if os.getenv("ENVIRONMENT") == "test":
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean old requests
        now = time.time()
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip] 
                if now - t < self.window
            ]
        
        # Check limit
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.limit:
            return Response(
                content="Rate limit exceeded. Please try again later.",
                status_code=429,
                headers={"Retry-After": str(self.window)}
            )
        
        # Add current request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(now)
        
        return await call_next(request)