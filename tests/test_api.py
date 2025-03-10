import unittest
from unittest.mock import patch, MagicMock
import requests

from fruitylookup.api import FruitAPIClient
from fruitylookup.models import Fruit


class TestFruitAPIClient(unittest.TestCase):
    """Tests for the FruitAPIClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = FruitAPIClient()
        
        # Sample API response
        self.sample_response = {
            "id": 1,
            "name": "Apple",
            "family": "Rosaceae",
            "genus": "Malus",
            "order": "Rosales",
            "nutritions": {
                "carbohydrates": 11.4,
                "protein": 0.3,
                "fat": 0.4,
                "calories": 52,
                "sugar": 10.3
            }
        }
    
    @patch("fruitylookup.api.requests.get")
    def test_get_fruit_by_name_success(self, mock_get):
        """Test successful fruit lookup."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_response
        mock_get.return_value = mock_response
        
        # Call the method
        fruit = self.client.get_fruit_by_name("apple")
        
        # Verify the result
        self.assertIsInstance(fruit, Fruit)
        self.assertEqual(fruit.name, "Apple")
        self.assertEqual(fruit.id, 1)
        self.assertEqual(fruit.family, "Rosaceae")
        self.assertEqual(fruit.nutrition.sugar, 10.3)
        self.assertEqual(fruit.nutrition.carbohydrates, 11.4)
        
        # Verify the API was called correctly
        mock_get.assert_called_once_with(f"{self.client.BASE_URL}/apple")
    
    @patch("fruitylookup.api.requests.get")
    def test_get_fruit_by_name_not_found(self, mock_get):
        """Test fruit lookup with a non-existent fruit."""
        # Set up mock response for a 404 error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Call the method and expect a ValueError
        with self.assertRaises(ValueError) as context:
            self.client.get_fruit_by_name("nonexistentfruit")
        
        # Verify the error message
        self.assertIn("not found", str(context.exception))
    
    @patch("fruitylookup.api.requests.get")
    def test_get_fruit_by_name_connection_error(self, mock_get):
        """Test fruit lookup with a connection error."""
        # Set up mock to raise an exception
        mock_get.side_effect = requests.RequestException("Connection error")
        
        # Call the method and expect a ConnectionError
        with self.assertRaises(ConnectionError) as context:
            self.client.get_fruit_by_name("apple")
        
        # Verify the error message
        self.assertIn("Failed to connect", str(context.exception))


if __name__ == "__main__":
    unittest.main()