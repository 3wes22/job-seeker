from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class BaseEvent:
    """Base class for all events"""
    event_id: str
    timestamp: str
    service_name: str
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# User Service Events
@dataclass
class UserCreatedEvent(BaseEvent):
    """Event published when a new user is created"""
    user_id: int
    username: str
    email: str
    user_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

@dataclass
class UserUpdatedEvent(BaseEvent):
    """Event published when a user is updated"""
    user_id: int
    username: str
    email: str
    user_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    changes: Dict[str, Any] = None

@dataclass
class UserDeletedEvent(BaseEvent):
    """Event published when a user is deleted"""
    user_id: int
    username: str

# Job Service Events
@dataclass
class JobCreatedEvent(BaseEvent):
    """Event published when a new job is created"""
    job_id: int
    title: str
    company_id: int
    employer_id: int
    job_type: str
    location: str
    is_remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None

@dataclass
class JobUpdatedEvent(BaseEvent):
    """Event published when a job is updated"""
    job_id: int
    title: str
    company_id: int
    employer_id: int
    changes: Dict[str, Any] = None

@dataclass
class JobDeletedEvent(BaseEvent):
    """Event published when a job is deleted"""
    job_id: int
    employer_id: int

# Company Events
@dataclass
class CompanyCreatedEvent(BaseEvent):
    """Event published when a new company is created"""
    company_id: int
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None