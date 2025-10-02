"""
API helper utilities for common operations.
"""
import json
from typing import Dict, Any
from jsonschema import validate, ValidationError
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate JSON data against a schema.
    
    Args:
        data: JSON data to validate
        schema: JSON schema
        
    Returns:
        bool: True if valid, raises exception if invalid
    """
    try:
        validate(instance=data, schema=schema)
        logger.info("JSON schema validation passed")
        return True
    except ValidationError as e:
        logger.error(f"JSON schema validation failed: {e.message}")
        raise


def validate_response_time(response_time: float, max_time: float) -> bool:
    """
    Validate response time is within acceptable limits.
    
    Args:
        response_time: Actual response time in seconds
        max_time: Maximum acceptable time in seconds
        
    Returns:
        bool: True if within limits
    """
    if response_time <= max_time:
        logger.info(f"Response time {response_time:.2f}s is within limit {max_time}s")
        return True
    else:
        logger.warning(f"Response time {response_time:.2f}s exceeds limit {max_time}s")
        return False


def validate_status_code(actual: int, expected: int) -> bool:
    """
    Validate status code matches expected value.
    
    Args:
        actual: Actual status code
        expected: Expected status code
        
    Returns:
        bool: True if match
    """
    if actual == expected:
        logger.info(f"Status code validation passed: {actual}")
        return True
    else:
        logger.error(f"Status code mismatch: expected {expected}, got {actual}")
        return False


def compare_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any], ignore_keys: list = None) -> bool:
    """
    Compare two dictionaries, optionally ignoring certain keys.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        ignore_keys: List of keys to ignore in comparison
        
    Returns:
        bool: True if dictionaries match
    """
    if ignore_keys is None:
        ignore_keys = []
    
    # Create copies to avoid modifying originals
    d1 = {k: v for k, v in dict1.items() if k not in ignore_keys}
    d2 = {k: v for k, v in dict2.items() if k not in ignore_keys}
    
    match = d1 == d2
    if match:
        logger.info("Dictionary comparison passed")
    else:
        logger.error(f"Dictionary comparison failed. Diff: {set(d1.items()) ^ set(d2.items())}")
    
    return match


def pretty_print_json(data: Dict[str, Any]) -> str:
    """
    Pretty print JSON data.
    
    Args:
        data: JSON data
        
    Returns:
        str: Formatted JSON string
    """
    return json.dumps(data, indent=2, sort_keys=True)


def extract_value_from_response(response_json: Dict[str, Any], key_path: str) -> Any:
    """
    Extract value from nested JSON response using dot notation.
    
    Args:
        response_json: Response JSON
        key_path: Path to key in dot notation (e.g., "data.user.name")
        
    Returns:
        Any: Extracted value
    """
    keys = key_path.split('.')
    value = response_json
    
    try:
        for key in keys:
            value = value[key]
        logger.debug(f"Extracted value from {key_path}: {value}")
        return value
    except (KeyError, TypeError) as e:
        logger.error(f"Failed to extract value from {key_path}: {e}")
        raise


def generate_unique_name(base_name: str) -> str:
    """
    Generate a unique name with timestamp.
    
    Args:
        base_name: Base name for the object
        
    Returns:
        str: Unique name
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    unique_name = f"{base_name}_{timestamp}"
    logger.debug(f"Generated unique name: {unique_name}")
    return unique_name


