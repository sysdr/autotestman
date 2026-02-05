"""
User data model with defensive parsing capabilities.
"""
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class User:
    """
    Represents a user with validated fields and safe defaults.
    
    This dataclass demonstrates production-grade data modeling:
    - Type hints for IDE support and runtime checking
    - Optional fields with sensible defaults
    - Factory method for safe construction from untrusted data
    """
    id: int
    name: str
    age: Optional[int] = None
    email: str = ""
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: dict) -> Optional['User']:
        """
        Safely construct a User from a dictionary.
        
        This factory method is the core of defensive parsing:
        1. Uses .get() with fallbacks instead of direct key access
        2. Handles type coercion explicitly (string to int)
        3. Returns None on failure instead of crashing
        4. Logs parsing errors for production debugging
        
        Args:
            data: Raw dictionary from JSON parsing
            
        Returns:
            User instance if valid, None if parsing fails
        """
        try:
            # Extract ID with validation
            user_id = data.get('id')
            if user_id is None:
                raise ValueError("Missing required field: id")
            
            # Coerce to int, handling string IDs
            user_id = int(user_id)
            
            # Extract name with default
            name = str(data.get('name', 'Unknown User')).strip()
            if not name:
                name = 'Unknown User'
            
            # Handle age with multiple edge cases
            raw_age = data.get('age')
            age = None
            if raw_age is not None:
                try:
                    age = int(raw_age)
                    if age < 0 or age > 150:  # Sanity check
                        logger.warning(f"Suspicious age value: {age} for user {user_id}")
                        age = None
                except (ValueError, TypeError):
                    logger.warning(f"Invalid age format for user {user_id}: {raw_age}")
                    age = None
            
            # Extract email with validation
            email = str(data.get('email', '')).strip()
            
            # Extract active status
            is_active = bool(data.get('is_active', True))
            
            return cls(
                id=user_id,
                name=name,
                age=age,
                email=email,
                is_active=is_active
            )
            
        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Failed to parse user record: {e}, data: {data}")
            return None
    
    def is_adult(self) -> bool:
        """Check if user is an adult (age > 18)."""
        return self.age is not None and self.age > 18
    
    def __repr__(self) -> str:
        """Human-readable representation."""
        age_str = f"{self.age}y" if self.age else "age unknown"
        status = "[OK]" if self.is_active else "[X]"
        return f"User(id={self.id}, name='{self.name}', {age_str}, {status})"
