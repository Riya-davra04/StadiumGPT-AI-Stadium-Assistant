"""
Stadium Models Module
=====================
Defines Pydantic models for stadium structure, sections, and facilities.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class GateType(str, Enum):
    """Gate types in the stadium."""
    MAIN = "main"
    VIP = "vip"
    GENERAL = "general"
    ACCESSIBLE = "accessible"
    EMERGENCY = "emergency"
    STAFF = "staff"


class GateStatus(str, Enum):
    """Gate operational status."""
    OPEN = "open"
    CLOSED = "closed"
    CONGESTED = "congested"
    MAINTENANCE = "maintenance"


class CrowdLevel(str, Enum):
    """Crowd density levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FacilityType(str, Enum):
    """Facility types in the stadium."""
    FOOD = "food"
    RESTROOM = "restroom"
    FIRST_AID = "first_aid"
    MERCH = "merch"
    ATM = "atm"
    INFORMATION = "information"


class Section(BaseModel):
    """
    Stadium section model.
    
    Attributes:
        id: Section identifier
        name: Section name
        capacity: Maximum capacity
        current_occupancy: Current number of people
        gates: Connected gates
        facilities: Nearby facilities
        crowd_level: Current crowd density level
        last_updated: Last update timestamp
    """
    id: str = Field(..., description="Section ID")
    name: str = Field(..., description="Section name")
    capacity: int = Field(..., gt=0, description="Maximum capacity")
    current_occupancy: int = Field(0, ge=0, description="Current occupancy")
    gates: List[str] = Field(default=[], description="Connected gates")
    facilities: List[str] = Field(default=[], description="Nearby facilities")
    crowd_level: CrowdLevel = Field(default=CrowdLevel.LOW)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('current_occupancy')
    @classmethod
    def validate_occupancy(cls, v: int, info) -> int:
        """Ensure occupancy doesn't exceed capacity."""
        if 'capacity' in info.data and v > info.data['capacity']:
            raise ValueError('Occupancy cannot exceed capacity')
        return v


class Gate(BaseModel):
    """
    Stadium gate model.
    
    Attributes:
        id: Gate identifier
        name: Gate name
        type: Gate type
        status: Current operational status
        crowd_level: Current crowd density
        queue_length: Current queue length
        average_wait_time: Average wait time in minutes
    """
    id: str = Field(..., description="Gate ID")
    name: str = Field(..., description="Gate name")
    type: GateType = Field(default=GateType.GENERAL)
    status: GateStatus = Field(default=GateStatus.OPEN)
    crowd_level: CrowdLevel = Field(default=CrowdLevel.LOW)
    queue_length: int = Field(0, ge=0, description="Queue length")
    average_wait_time: int = Field(0, ge=0, description="Average wait time in minutes")
    coordinates: Optional[Dict[str, float]] = Field(None, description="GPS coordinates")
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class StadiumLayout(BaseModel):
    """
    Complete stadium layout model.
    
    Attributes:
        id: Stadium identifier
        name: Stadium name
        location: Stadium location
        total_capacity: Total capacity
        sections: List of all sections
        gates: List of all gates
        facilities: List of all facilities
        event: Current event name
        current_attendance: Current attendance
        updated_at: Last update timestamp
    """
    id: str = Field(..., description="Stadium ID")
    name: str = Field(..., description="Stadium name")
    location: str = Field(..., description="Stadium location")
    total_capacity: int = Field(..., gt=0)
    sections: List[Section] = Field(default=[])
    gates: List[Gate] = Field(default=[])
    facilities: List[Facility] = Field(default=[])
    event: str = Field(default="FIFA World Cup")
    current_attendance: int = Field(0, ge=0)
    max_attendance: int = Field(..., gt=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    emergency_exits: List[str] = Field(default=[])
    accessibility_features: List[str] = Field(default=[])

    @field_validator('current_attendance')
    @classmethod
    def validate_attendance(cls, v: int, info) -> int:
        """Ensure attendance doesn't exceed maximum capacity."""
        if 'max_attendance' in info.data and v > info.data['max_attendance']:
            raise ValueError('Current attendance cannot exceed maximum capacity')
        return v