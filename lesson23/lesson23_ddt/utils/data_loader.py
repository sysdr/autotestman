"""
Data Loader Module for DDT
Handles reading and validating test data from JSON files.
"""

from pathlib import Path
import json
from typing import List, Dict, Any

class DataLoader:
    """Loads and validates test data from JSON files"""
    
    def __init__(self, data_dir: Path = Path(__file__).parent.parent / "data"):
        self.data_dir = data_dir
    
    def load_credentials(self, filename: str = "credentials.json") -> List[Dict[str, Any]]:
        """
        Load credentials from JSON file with validation.
        
        Args:
            filename: Name of the JSON file in data directory
            
        Returns:
            List of credential dictionaries
            
        Raises:
            FileNotFoundError: If credentials file doesn't exist
            ValueError: If JSON structure is invalid
        """
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Credentials file not found: {file_path}")
        
        with file_path.open("r") as f:
            data = json.load(f)
        
        # Validate structure
        required_fields = ["role", "email", "password", "expected_dashboard"]
        for i, entry in enumerate(data):
            missing = [field for field in required_fields if field not in entry]
            if missing:
                raise ValueError(
                    f"Entry {i} missing required fields: {missing}"
                )
        
        return data
    
    def get_credential_ids(self, credentials: List[Dict[str, Any]]) -> List[str]:
        """Extract role names for test IDs"""
        return [cred["role"] for cred in credentials]


# Module-level function for pytest parametrize
def load_credentials() -> List[Dict[str, Any]]:
    """Convenience function for pytest.mark.parametrize"""
    loader = DataLoader()
    return loader.load_credentials()


def get_test_ids(credential: Dict[str, Any]) -> str:
    """Extract test ID from credential dict"""
    return credential["role"]
