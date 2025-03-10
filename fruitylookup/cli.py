import argparse
import sys
from typing import List, Optional

from .api import FruitAPIClient
from .formatters import get_formatter


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: List of command-line arguments
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Look up fruit information from the FruityVice API"
    )
    
    parser.add_argument(
        "fruit_name", 
        help="Name of the fruit to look up"
    )
    
    parser.add_argument(
        "--format", 
        choices=["human", "machine"], 
        default="human",
        help="Output format (human-readable or machine-readable)"
    )
    
    parser.add_argument(
        "--api-url", 
        help="Custom API URL (defaults to https://www.fruityvice.com/api/fruit)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parsed_args = parse_args(args)
    
    try:
        client = FruitAPIClient(parsed_args.api_url)
        fruit = client.get_fruit_by_name(parsed_args.fruit_name)
        
        formatter = get_formatter(parsed_args.format)
        output = formatter.format(fruit)
        
        print(output)
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Connection error: {str(e)}", file=sys.stderr)
        return 2


def lookup_fruit(name: str, format_type: str = "human", api_url: Optional[str] = None) -> str:
    """Look up a fruit by name and return the formatted information.
    
    This is the main function for programmatic use.
    
    Args:
        name: Name of the fruit to look up
        format_type: Output format ('human' or 'machine')
        api_url: Optional custom API URL
        
    Returns:
        Formatted fruit information
        
    Raises:
        ValueError: If the fruit is not found
        ConnectionError: If there's an issue with the API connection
    """
    client = FruitAPIClient(api_url)
    fruit = client.get_fruit_by_name(name)
    
    formatter = get_formatter(format_type)
    return formatter.format(fruit)


if __name__ == "__main__":
    sys.exit(main())