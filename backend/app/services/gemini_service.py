"""
Gemini AI Service Module
========================
Provides AI-powered features using Google's Gemini API including:
- Natural language query processing
- Route optimization
- Crowd analysis
- Emergency response guidance
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from app.services.base_service import BaseService
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class GeminiService(BaseService):
    """
    Gemini AI Service for StadiumGPT.
    
    This service integrates Google's Gemini AI to provide:
    - Conversational AI for fans
    - Smart route recommendations
    - Crowd density analysis
    - Emergency response guidance
    
    Attributes:
        api_key (str): Gemini API key from environment
        model: Gemini Pro model instance
        chat_model: Gemini Flash model for faster responses
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("GeminiService")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None
        self.chat_model = None
        self._initialize()
    
    def _initialize(self) -> None:
        """
        Initialize Gemini AI models.
        
        If API key is missing or invalid, service will gracefully degrade
        with fallback responses.
        """
        if not self.api_key:
            self.log_warning("No Gemini API key found. AI features will be disabled.")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.chat_model = genai.GenerativeModel('gemini-1.5-flash')
            self.log_info("Gemini service initialized successfully")
        except Exception as e:
            self.log_error("Failed to initialize Gemini", e)
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user query with context using Gemini AI.
        
        Args:
            query (str): User's question or request
            context (Dict[str, Any]): Additional context (stadium, section, language)
            
        Returns:
            Dict[str, Any]: Response with AI-generated text and metadata
            
        Example:
            >>> result = await gemini.process_query(
            ...     "How do I get to Gate B?",
            ...     {"stadium": "FIFA World Cup Stadium", "language": "English"}
            ... )
            >>> print(result["response"])
            "Head straight for 50 meters, then turn right..."
        """
        if not self.model:
            return self._get_fallback_response("AI service not available")
        
        try:
            prompt = self._build_prompt(query, context)
            response = self.model.generate_content(prompt)
            
            return {
                "response": response.text,
                "timestamp": self.get_timestamp(),
                "query": query,
                "model": "gemini-1.5-pro"
            }
        except Exception as e:
            self.log_error("Gemini query error", e)
            return self._get_fallback_response("Unable to process query")
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze crowd data and provide actionable insights.
        
        Args:
            data (Dict[str, Any]): Crowd density data by section
            
        Returns:
            Dict[str, Any]: Analysis with predictions and recommendations
        """
        if not self.model:
            return {
                "crowd_level": "medium",
                "recommendations": ["Monitor crowd flow", "Prepare for congestion"],
                "timestamp": self.get_timestamp()
            }
        
        try:
            prompt = f"""
            Analyze stadium crowd data and return ONLY valid JSON:
            - Current density: {data.get('density', {})}
            - Time: {data.get('time', '')}
            - Event: {data.get('event', 'FIFA World Cup')}
            
            Return JSON with:
            1. congestion_prediction: "low", "medium", or "high"
            2. recommendations: list of 2-3 actionable recommendations
            3. hotspots: list of crowded locations
            """
            
            response = self.model.generate_content(prompt)
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "congestion_prediction": "medium",
                    "recommendations": ["Monitor crowd flow", "Open additional gates"],
                    "hotspots": ["Gate A", "Food Court"]
                }
        except Exception as e:
            self.log_error("Crowd analysis error", e)
            return {
                "congestion_prediction": "medium",
                "recommendations": ["Monitor crowd flow"],
                "hotspots": []
            }
    
    async def get_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate optimal route based on preferences and conditions.
        
        Args:
            data (Dict[str, Any]): Route parameters including start, end, preferences
            
        Returns:
            Dict[str, Any]: Route details with path, time, and alternatives
        """
        if not self.model:
            return {
                "error": "AI service not available",
                "fallback": {
                    "path": ["Gate A", "Concourse", "Section B"],
                    "estimated_time": 8,
                    "crowd_level": "medium"
                }
            }
        
        try:
            prompt = f"""
            Provide the optimal route in a stadium based on:
            - Start: {data.get('start', '')}
            - End: {data.get('end', '')}
            - Preferences: {data.get('preferences', ['shortest'])}
            - Crowd density: {data.get('crowd_density', 'medium')}
            - Accessibility needs: {data.get('accessibility', None)}
            
            Return ONLY valid JSON with:
            - path: list of waypoints
            - estimated_time: minutes (integer)
            - accessibility_info: accessibility features (object)
            - crowd_level: "low", "medium", or "high"
            - alternative_routes: list of alternatives
            """
            
            response = self.model.generate_content(prompt)
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "path": ["Gate A", "Concourse", data.get('end', 'Destination')],
                    "estimated_time": 8,
                    "crowd_level": "medium",
                    "accessibility_info": {"wheelchair_accessible": True},
                    "alternative_routes": []
                }
        except Exception as e:
            self.log_error("Route generation error", e)
            return {"error": "Could not generate route"}
    
    async def check_health(self) -> bool:
        """Check if Gemini service is healthy and ready."""
        return self.model is not None
    
    def _build_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """
        Build a structured prompt for Gemini AI.
        
        Args:
            query (str): User's question
            context (Dict[str, Any]): Context information
            
        Returns:
            str: Formatted prompt for Gemini
        """
        return f"""
        Context: You are StadiumGPT, an AI assistant for FIFA World Cup stadiums.
        Help fans, volunteers, and staff with stadium-related queries.
        
        Current Context:
        - Stadium: {context.get('stadium', 'FIFA World Cup Stadium')}
        - Section: {context.get('section', 'Unknown')}
        - Event: {context.get('event', 'FIFA World Cup')}
        - Time: {context.get('time', 'Current')}
        - Language: {context.get('language', 'English')}
        
        User Query: {query}
        
        Provide helpful, accurate, and safe assistance. Be concise and friendly.
        """
    
    def _get_fallback_response(self, error_message: str) -> Dict[str, Any]:
        """
        Generate a graceful fallback response when AI is unavailable.
        
        Args:
            error_message (str): The error that occurred
            
        Returns:
            Dict[str, Any]: Fallback response with error details
        """
        return {
            "response": f"⚠️ {error_message}. Please try again later.",
            "error": error_message,
            "timestamp": self.get_timestamp(),
            "fallback": True
        }