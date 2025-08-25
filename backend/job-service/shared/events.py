from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime

# User Service Events
@dataclass
class UserCreatedEvent:
    """Event published when a new user is created"""
    event_id: str
    timestamp: str
    service_name: str
    user_id: int
    username: str
    email: str
    user_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class UserUpdatedEvent:
    """Event published when a user is updated"""
    event_id: str
    timestamp: str
    service_name: str
    user_id: int
    username: str
    email: str
    user_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    changes: Dict[str, Any] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class UserDeletedEvent:
    """Event published when a user is deleted"""
    event_id: str
    timestamp: str
    service_name: str
    user_id: int
    username: str
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# Job Service Events
@dataclass
class JobCreatedEvent:
    """Event published when a new job is created"""
    event_id: str
    timestamp: str
    service_name: str
    job_id: int
    title: str
    company_id: int
    employer_id: int
    job_type: str
    location: str
    is_remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class JobUpdatedEvent:
    """Event published when a job is updated"""
    event_id: str
    timestamp: str
    service_name: str
    job_id: int
    title: str
    company_id: int
    employer_id: int
    changes: Dict[str, Any] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class JobDeletedEvent:
    """Event published when a job is deleted"""
    event_id: str
    timestamp: str
    service_name: str
    job_id: int
    employer_id: int
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# Company Events
@dataclass
class CompanyCreatedEvent:
    """Event published when a new company is created"""
    event_id: str
    timestamp: str
    service_name: str
    company_id: int
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self) 