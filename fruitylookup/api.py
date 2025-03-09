import requests
from typing import Optional, Dict, Any
from .models import Fruit


class FruitAPIClient:
    """Client for interacting with the FruityVice API."""
    
    BASE_URL = "https://www.fruityvice.com/api/fruit"
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the FruitAPIClient.
        
        Args:
            base_url: Optional custom base URL for the API
        """
        self.base_url = base_url or self.BASE_URL
    
    def get_fruit_by_name(self, name: str) -> Fruit:
        """Get fruit information by name.
        
        Args:
            name: Name of the fruit to look up
            
        Returns:
            Fruit object with the fruit information
            
        Raises:
            ValueError: If the fruit is not found
            ConnectionError: If there's an issue with the API connection
        """
        try:
            response = requests.get(f"{self.base_url}/{name}")
            
            if response.status_code == 404:
                raise ValueError(f"Fruit '{name}' not found")
            
            response.raise_for_status()
            
            return Fruit.from_dict(response.json())
        except requests.RequestException as e:
            if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
                raise ValueError(f"Fruit '{name}' not found") from e
            raise ConnectionError(f"Failed to connect to FruityVice API: {str(e)}") from e