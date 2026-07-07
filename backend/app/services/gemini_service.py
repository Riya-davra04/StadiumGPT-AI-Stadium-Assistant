import google.generativeai as genai
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            logger.warning("⚠️ No Gemini API key found. AI features will be disabled.")
            self.model = None
            self.chat_model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                self.chat_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✅ Gemini service initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini: {e}")
                self.model = None
                self.chat_model = None
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user query with context using Gemini"""
        if not self.model:
            return {
                "response": "⚠️ AI service is not available. Please check your GEMINI_API_KEY.",
                "error": "Missing API key",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            prompt = self._build_prompt(query, context)
            response = self.model.generate_content(prompt)
            
            return {
                "response": response.text,
                "timestamp": datetime.utcnow().isoformat(),
                "query": query
            }
        except Exception as e:
            logger.error(f"❌ Gemini query error: {e}")
            return {
                "error": "Unable to process query",
                "fallback": "Please try again later",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get navigation route using Gemini"""
        if not self.model:
            return {
                "error": "AI service not available",
                "fallback": {
                    "path": ["Gate A", "Concourse", "Section B", "Gate C"],
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
            # Try to parse JSON response
            try:
                return json.loads(response.text)
            except:
                # Fallback if response is not valid JSON
                return {
                    "path": ["Gate A", "Concourse", data.get('end', 'Destination')],
                    "estimated_time": 8,
                    "crowd_level": "medium",
                    "accessibility_info": {"wheelchair_accessible": True},
                    "alternative_routes": []
                }
        except Exception as e:
            logger.error(f"❌ Route generation error: {e}")
            return {"error": "Could not generate route"}
    
    async def analyze_crowd(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze crowd data and provide insights"""
        if not self.model:
            return {
                "crowd_level": "medium",
                "recommendations": ["Monitor crowd flow", "Prepare for congestion"],
                "timestamp": datetime.utcnow().isoformat()
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
            except:
                return {
                    "congestion_prediction": "medium",
                    "recommendations": ["Monitor crowd flow", "Open additional gates"],
                    "hotspots": ["Gate A", "Food Court"]
                }
        except Exception as e:
            logger.error(f"❌ Crowd analysis error: {e}")
            return {"error": "Could not analyze crowd data"}
    
    async def check_health(self) -> bool:
        """Check if Gemini service is healthy"""
        return self.model is not None
    
    def _build_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build prompt with context for Gemini"""
        return f"""
        Context: You are StadiumGPT, an AI assistant for FIFA World Cup stadiums.
        Help fans, volunteers, and staff with stadium-related queries.
        
        Current Context:
        - Stadium: {context.get('stadium', '')}
        - Section: {context.get('section', '')}
        - Event: {context.get('event', '')}
        - Time: {context.get('time', '')}
        - Language: {context.get('language', 'English')}
        
        User Query: {query}
        
        Provide helpful, accurate, and safe assistance. Be concise and friendly.
        """