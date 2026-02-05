"""
Data models for test users
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserModel:
    """Represents a test user account with validation"""
    
    email: str
    password: str
    role: str
    active: bool
    created_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate data immediately after initialization"""
        # Email validation
        if "@" not in self.email or "." not in self.email.split("@")[1]:
            raise ValueError(f"Invalid email format: {self.email}")
        
        # Password strength
        if len(self.password) < 8:
            raise ValueError(f"Password too short (min 8 chars): {len(self.password)} chars")
        
        # Role whitelist
        valid_roles = {"user", "admin", "viewer", "editor"}
        if self.role not in valid_roles:
            raise ValueError(f"Invalid role '{self.role}'. Must be one of {valid_roles}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "active": self.active,
            "created_at": self.created_at
        }
    
    def is_privileged(self) -> bool:
        """Check if user has elevated permissions"""
        return self.role in {"admin", "editor"}
    
    def __repr__(self) -> str:
        """Clean representation for debugging"""
        status = "active" if self.active else "inactive"
        return f"UserModel(email='{self.email}', role='{self.role}', {status})"
