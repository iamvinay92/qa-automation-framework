"""
Common data generation utilities.
"""
import random
import string
from datetime import datetime
from faker import Faker

fake = Faker()


def generate_random_string(length: int = 10) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the string
        
    Returns:
        str: Random string
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_unique_email() -> str:
    """
    Generate a unique email address.
    
    Returns:
        str: Unique email address
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"test_{timestamp}@example.com"


def generate_unique_name(prefix: str = "Test") -> str:
    """
    Generate a unique name with timestamp.
    
    Args:
        prefix: Prefix for the name
        
    Returns:
        str: Unique name
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{timestamp}"


def generate_phone_number() -> str:
    """
    Generate a random phone number.
    
    Returns:
        str: Phone number
    """
    return fake.phone_number()


def generate_address() -> dict:
    """
    Generate a random address.
    
    Returns:
        dict: Address information
    """
    return {
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip_code": fake.zipcode(),
        "country": fake.country()
    }


def generate_user_data() -> dict:
    """
    Generate random user data.
    
    Returns:
        dict: User information
    """
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": generate_unique_email(),
        "phone": generate_phone_number(),
        "address": generate_address()
    }


