import json
from typing import Dict, Any
from .models import Fruit


class OutputFormatter:
    """Base class for output formatters."""
    
    def format(self, fruit: Fruit) -> str:
        """Format a fruit object into a string.
        
        Args:
            fruit: Fruit object to format
            
        Returns:
            Formatted string with the fruit information
        """
        raise NotImplementedError("Subclasses must implement format()")


class HumanReadableFormatter(OutputFormatter):
    """Formatter for human-readable output."""
    
    def format(self, fruit: Fruit) -> str:
        """Format a fruit object into a human-readable string.
        
        Args:
            fruit: Fruit object to format
            
        Returns:
            Human-readable string with the fruit information
        """
        lines = [
            f"Name: {fruit.name}",
            f"ID: {fruit.id}",
            f"Family: {fruit.family}",
            f"Nutrition:",
            f"  - Sugar: {fruit.nutrition.sugar}g",
            f"  - Carbohydrates: {fruit.nutrition.carbohydrates}g"
        ]
        
        return "\n".join(lines)


class MachineReadableFormatter(OutputFormatter):
    """Formatter for machine-readable output (JSON)."""
    
    def format(self, fruit: Fruit) -> str:
        """Format a fruit object into a JSON string.
        
        Args:
            fruit: Fruit object to format
            
        Returns:
            JSON string with the fruit information
        """
        data = {
            "name": fruit.name,
            "id": fruit.id,
            "family": fruit.family,
            "nutrition": {
                "sugar": fruit.nutrition.sugar,
                "carbohydrates": fruit.nutrition.carbohydrates
            }
        }
        
        return json.dumps(data, indent=2)


def get_formatter(format_type: str) -> OutputFormatter:
    """Get the appropriate formatter for the given format type.
    
    Args:
        format_type: Type of formatter to get ('human' or 'machine')
        
    Returns:
        OutputFormatter for the given format type
        
    Raises:
        ValueError: If an invalid format type is provided
    """
    if format_type == 'human':
        return HumanReadableFormatter()
    elif format_type == 'machine':
        return MachineReadableFormatter()
    else:
        raise ValueError(f"Invalid format type: {format_type}. Use 'human' or 'machine'.")