from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict ,Any
from datetime import datetime
from enum import Enum


class EmergencyType(str, Enum):
    """Emergency types"""
    MEDICAL = "medical"
    FIRE = "fire"
    SECURITY = "security"
    CROWD = "crowd"
    NATURAL = "natural"
    TERROR = "terror"
    INFRASTRUCTURE = "infrastructure"


class EmergencySeverity(str, Enum):
    """Emergency severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyStatus(str, Enum):
    """Emergency status"""
    ACTIVE = "active"
    RESPONDED = "responded"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class EmergencyAlert(BaseModel):
    """Emergency alert model"""
    id: str = Field(..., description="Alert ID")
    type: EmergencyType
    severity: EmergencySeverity
    location: str = Field(..., description="Location description")
    section: Optional[str] = None
    gate: Optional[str] = None
    description: str = Field(..., description="Detailed description")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: EmergencyStatus = EmergencyStatus.ACTIVE
    reported_by: Optional[str] = None
    response_team: List[str] = Field(default=[])
    actions_taken: List[str] = Field(default=[])
    instructions: List[str] = Field(default=[])
    resolved_at: Optional[datetime] = None
    coordinates: Optional[Dict[str, float]] = None
    severity_score: float = Field(0.0, ge=0, le=1)
    affected_areas: List[str] = Field(default=[])
    notifications_sent: List[str] = Field(default=[])

    @validator('severity_score')
    def validate_severity_score(cls, v):
        return min(max(v, 0.0), 1.0)


class EmergencyResponse(BaseModel):
    """Emergency response model"""
    alert_id: str
    actions: List[str] = Field(default=[])
    teams_dispatched: List[str] = Field(default=[])
    instructions: List[str] = Field(default=[])
    nearest_station: Optional[Dict[str, Any]] = None
    estimated_response_time: int = Field(..., description="Estimated response time in minutes")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MedicalEmergency(BaseModel):
    """Medical emergency specific data"""
    patient_condition: str = Field(..., description="Patient condition description")
    consciousness: bool = True
    breathing: bool = True
    pulse: Optional[str] = None
    injuries: List[str] = Field(default=[])
    allergies: List[str] = Field(default=[])
    medical_history: Optional[str] = None
    first_aid_given: List[str] = Field(default=[])
    required_equipment: List[str] = Field(default=[])


class SecurityIncident(BaseModel):
    """Security incident specific data"""
    incident_type: str = Field(..., description="Type of security incident")
    description: str = Field(...)
    involved_parties: List[str] = Field(default=[])
    witnesses: List[str] = Field(default=[])
    evidence: List[str] = Field(default=[])
    security_actions: List[str] = Field(default=[])
    police_notified: bool = False
    police_arrival_time: Optional[datetime] = None


class EmergencyStation(BaseModel):
    """Emergency station model"""
    id: str
    name: str
    location: str
    type: str = Field(..., description="first_aid, fire, police, security")
    status: str = Field("available", description="available, busy, offline")
    staff_count: int = Field(..., ge=0)
    equipment: List[str] = Field(default=[])
    contact_number: str
    coordinates: Optional[Dict[str, float]] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)