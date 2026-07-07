from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load stadium knowledge base"""
        knowledge_docs = [
            {
                "id": "stadium_layout_1",
                "content": "Main Stadium has 5 gates: A, B, C, D, E. Gate A is main entrance with VIP access. Gate B is for general admission. Gate C has accessible entrances. Gate D is for staff. Gate E is for emergency exits.",
                "category": "layout"
            },
            {
                "id": "concession_1",
                "content": "Food options include: Food Court A (upper deck) with burgers and pizzas, Food Court B (main concourse) with local cuisine, Food Court C (lower level) with quick service. Halal options available at Food Court B. Vegetarian options at all food courts.",
                "category": "food"
            },
            {
                "id": "accessibility_1",
                "content": "Accessibility features: Wheelchair access at Gate C. Hearing assistance devices available at Guest Services. Visual assistance available with app. Elevators located near Gates A, C, and E. Accessible seating sections: Sections A1, B2, C3.",
                "category": "accessibility"
            },
            {
                "id": "emergency_1",
                "content": "Emergency procedures: First aid stations at Sections A, C, E. Emergency exits at Gate E. Assembly points: North parking lot. Medical team contact: 111. Emergency response time: under 3 minutes.",
                "category": "emergency"
            },
            {
                "id": "transport_1",
                "content": "Transportation: Metro station 5-minute walk from Gate A. Bus stop at Gate B. Parking P1 (VIP), P2 (General), P3 (Accessible). Ride-share dropoff at Gate D. Estimated walk times: Metro - 5 mins, Bus - 8 mins, Parking - 10-15 mins.",
                "category": "transport"
            }
        ]
        
        self.documents = knowledge_docs
        self.build_index()
        
    def build_index(self):
        """Build FAISS index for retrieval"""
        if not self.documents:
            return
            
        texts = [doc["content"] for doc in self.documents]
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
    async def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant documents"""
        try:
            query_embedding = self.model.encode([query])
            
            distances, indices = self.index.search(
                np.array(query_embedding).astype('float32'),
                min(top_k, len(self.documents))
            )
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.documents):
                    results.append({
                        "id": self.documents[idx]["id"],
                        "content": self.documents[idx]["content"],
                        "category": self.documents[idx]["category"],
                        "relevance_score": float(1 / (1 + distance))
                    })
                    
            return results
        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")
            return []
    
    async def get_context(self, query: str) -> Dict[str, Any]:
        """Get context for a query"""
        docs = await self.retrieve(query)
        
        context = {}
        for doc in docs:
            if doc["category"] not in context:
                context[doc["category"]] = []
            context[doc["category"]].append(doc["content"])
            
        return {
            "query": query,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        }