"""
Production-grade JSON parsing utilities with error boundaries.
"""
import json
from pathlib import Path
from typing import List
import logging

from utils.user_model import User

logger = logging.getLogger(__name__)


def parse_users_from_file(filepath: Path) -> List[User]:
    """
    Parse users from a JSON file with comprehensive error handling.
    
    This function demonstrates error boundaries in test infrastructure:
    - File I/O errors don't crash the pipeline
    - JSON parsing errors are caught and logged
    - Individual record failures don't affect other records
    - Always returns a valid list (possibly empty)
    
    Args:
        filepath: Path to JSON file containing user data
        
    Returns:
        List of successfully parsed User objects
    """
    # Validate file exists
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        return []
    
    # Read and parse JSON with error boundary
    try:
        with filepath.open('r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        return []
    except Exception as e:
        logger.error(f"Failed to read {filepath}: {e}")
        return []
    
    # Validate data structure
    if not isinstance(raw_data, list):
        logger.error(f"Expected JSON array, got {type(raw_data)}")
        return []
    
    # Parse each record with individual error boundaries
    users: List[User] = []
    failed_count = 0
    
    for idx, record in enumerate(raw_data):
        if not isinstance(record, dict):
            logger.warning(f"Record {idx} is not a dict: {type(record)}")
            failed_count += 1
            continue
        
        user = User.from_dict(record)
        if user is not None:
            users.append(user)
        else:
            failed_count += 1
    
    # Log parsing statistics
    total = len(raw_data)
    success_rate = (len(users) / total * 100) if total > 0 else 0
    logger.info(
        f"Parsed {len(users)}/{total} users ({success_rate:.1f}% success rate)"
    )
    
    if failed_count > 0:
        logger.warning(f"{failed_count} records failed to parse")
    
    return users


def filter_adults(users: List[User]) -> List[User]:
    """
    Filter for adult users (age > 18).
    
    Args:
        users: List of User objects
        
    Returns:
        List containing only users with age > 18
    """
    adults = [u for u in users if u.is_adult()]
    
    logger.info(
        f"Filtered {len(adults)} adults from {len(users)} total users"
    )
    
    return adults


def filter_active_adults(users: List[User]) -> List[User]:
    """
    Filter for active adult users.
    
    Demonstrates chaining filters for complex business logic.
    """
    active_adults = [
        u for u in users 
        if u.is_adult() and u.is_active
    ]
    
    logger.info(
        f"Filtered {len(active_adults)} active adults from {len(users)} users"
    )
    
    return active_adults
