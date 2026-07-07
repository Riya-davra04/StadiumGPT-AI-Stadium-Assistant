from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class GateType(str, Enum):
    """Gate types"""
    MAIN = "main"
    VIP = "vip"
    GENERAL = "general"
    ACCESSIBLE = "accessible"
    EMERGENCY = "emergency"
    STAFF = "staff"


class GateStatus(str, Enum):
    """Gate status"""
    OPEN = "open"
    CLOSED = "closed"
    CONGESTED = "congested"
    MAINTENANCE = "maintenance"


class CrowdLevel(str, Enum):
    """Crowd level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FacilityType(str, Enum):
    """Facility types"""
    FOOD = "food"
    RESTROOM = "restroom"
    FIRST_AID = "first_aid"
    MERCH = "merch"
    ATM = "atm"
    INFORMATION = "information"


class Section(BaseModel):
    """Stadium section model"""
    id: str = Field(..., description="Section ID")
    name: str = Field(..., description="Section name")
    capacity: int = Field(..., gt=0, description="Maximum capacity")
    current_occupancy: int = Field(0, ge=0, description="Current occupancy")
    gates: List[str] = Field(default=[], description="Connected gates")
    facilities: List[str] = Field(default=[], description="Nearby facilities")
    crowd_level: CrowdLevel = CrowdLevel.LOW
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    @validator('current_occupancy')
    def validate_occupancy(cls, v, values):
        if 'capacity' in values and v > values['capacity']:
            raise ValueError('Occupancy cannot exceed capacity')
        return v


class Gate(BaseModel):
    """Gate model"""
    id: str = Field(..., description="Gate ID")
    name: str = Field(..., description="Gate name")
    type: GateType = GateType.GENERAL
    status: GateStatus = GateStatus.OPEN
    crowd_level: CrowdLevel = CrowdLevel.LOW
    queue_length: int = Field(0, ge=0, description="Queue length")
    average_wait_time: int = Field(0, ge=0, description="Average wait time in minutes")
    coordinates: Optional[Dict[str, float]] = Field(None, description="GPS coordinates")
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class Facility(BaseModel):
    """Facility model"""
    id: str = Field(..., description="Facility ID")
    name: str = Field(..., description="Facility name")
    type: FacilityType
    location: str = Field(..., description="Location description")
    capacity: int = Field(..., gt=0, description="Maximum capacity")
    current_load: int = Field(0, ge=0, description="Current load")
    avg_wait_time: int = Field(0, ge=0, description="Average wait time in minutes")
    status: str = Field("available", description="Status: available, busy, closed")
    operating_hours: Optional[Dict[str, str]] = None
    coordinates: Optional[Dict[str, float]] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class StadiumLayout(BaseModel):
    """Stadium layout model"""
    id: str = Field(..., description="Stadium ID")
    name: str = Field(..., description="Stadium name")
    location: str = Field(..., description="Stadium location")
    total_capacity: int = Field(..., gt=0)
    sections: List[Section] = Field(default=[])
    gates: List[Gate] = Field(default=[])
    facilities: List[Facility] = Field(default=[])
    event: str = "FIFA World Cup"
    current_attendance: int = Field(0, ge=0)
    max_attendance: int = Field(..., gt=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    emergency_exits: List[str] = Field(default=[])
    accessibility_features: List[str] = Field(default=[])

    @validator('current_attendance')
    def validate_attendance(cls, v, values):
        if 'max_attendance' in values and v > values['max_attendance']:
            raise ValueError('Current attendance cannot exceed maximum capacity')
        return v


class StadiumData(BaseModel):
    """Stadium data model - simplified version for API responses"""
    id: str = Field(..., description="Stadium ID")
    name: str = Field(..., description="Stadium name")
    location: str = Field(..., description="Stadium location")
    total_capacity: int = Field(..., gt=0)
    current_attendance: int = Field(0, ge=0)
    event: str = "FIFA World Cup"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    sections: List[Section] = Field(default=[])
    gates: List[Gate] = Field(default=[])
    facilities: List[Facility] = Field(default=[])


class CrowdData(BaseModel):
    """Crowd data model"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sections: Dict[str, float] = Field(default={}, description="Section -> density mapping")
    gates: Dict[str, float] = Field(default={}, description="Gate -> density mapping")
    overall_density: float = Field(..., ge=0, le=1)
    crowd_level: CrowdLevel
    hotspots: List[Dict[str, Any]] = Field(default=[])
    predictions: Dict[str, Any] = Field(default={})
    recommendations: List[str] = Field(default=[])


class QueueData(BaseModel):
    """Queue data model"""
    establishment_id: str
    queue_length: int = Field(..., ge=0)
    estimated_wait_time: int = Field(..., ge=0, description="Minutes")
    status: str
    capacity: int = Field(..., gt=0)
    current_load_percentage: float = Field(..., ge=0, le=100)
    recommendations: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TransportInfo(BaseModel):
    """Transport information model"""
    type: str = Field(..., description="Transport type: metro, bus, taxi, parking")
    name: str = Field(..., description="Transport name")
    distance: float = Field(..., description="Distance in meters")
    estimated_time: int = Field(..., description="Estimated time in minutes")
    crowd_level: CrowdLevel = CrowdLevel.LOW
    availability: str = Field("available", description="available, limited, unavailable")
    waiting_time: Optional[int] = Field(None, description="Waiting time in minutes")
    cost: Optional[float] = Field(None, description="Estimated cost")
    directions: List[str] = Field(default=[])
    last_updated: datetime = Field(default_factory=datetime.utcnow)