from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Nutrition:
    """Nutrition information for a fruit."""
    carbohydrates: float
    protein: float
    fat: float
    calories: float
    sugar: float


@dataclass
class Fruit:
    """Fruit information from the FruityVice API."""
    id: int
    name: str
    family: str
    genus: str
    order: str
    nutrition: Nutrition

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fruit':
        """Create a Fruit object from a dictionary.
        
        Args:
            data: Dictionary containing fruit data from the API
            
        Returns:
            Fruit object with the data
        """
        nutrition_data = data.get('nutritions', {})
        nutrition = Nutrition(
            carbohydrates=nutrition_data.get('carbohydrates', 0.0),
            protein=nutrition_data.get('protein', 0.0),
            fat=nutrition_data.get('fat', 0.0),
            calories=nutrition_data.get('calories', 0.0),
            sugar=nutrition_data.get('sugar', 0.0)
        )
        
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            family=data.get('family', ''),
            genus=data.get('genus', ''),
            order=data.get('order', ''),
            nutrition=nutrition
        )