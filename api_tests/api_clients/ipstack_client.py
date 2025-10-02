"""
API Client for ipstack Geolocation API.

This client handles interactions with the ipstack API for IP geolocation lookups.
API Documentation: https://ipstack.com/documentation
"""
from typing import Optional
from api_tests.api_clients.base_client import BaseAPIClient
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


class IpstackClient(BaseAPIClient):
    """Client for ipstack Geolocation API operations."""
    
    def __init__(self, base_url: str, access_key: str, timeout: int = 30):
        """
        Initialize ipstack API client.
        
        Args:
            base_url: Base URL for ipstack API
            access_key: API access key for authentication
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, timeout)
        self.access_key = access_key
        logger.info(f"IpstackClient initialized with base URL: {base_url}")
    
    def lookup_ip(self, ip_address: str, fields: Optional[str] = None) -> dict:
        """
        Lookup geolocation information for a specific IP address.
        
        Args:
            ip_address: IP address to lookup (e.g., "134.201.250.155")
            fields: Optional comma-separated list of fields to return
            
        Returns:
            Response object from requests library
        """
        endpoint = f"/{ip_address}"
        params = {"access_key": self.access_key}
        
        if fields:
            params["fields"] = fields
        
        logger.info(f"Looking up IP: {ip_address}")
        response = self.get(endpoint, params=params)
        
        if response.status_code == 200:
            logger.info(f"✓ IP lookup successful for {ip_address}")
        else:
            logger.warning(f"✗ IP lookup failed: {response.status_code}")
        
        return response
    
    def lookup_current_ip(self) -> dict:
        """
        Lookup geolocation information for the current/requester's IP.
        
        Returns:
            Response object from requests library
        """
        endpoint = "/check"
        params = {"access_key": self.access_key}
        
        logger.info("Looking up current IP")
        response = self.get(endpoint, params=params)
        
        if response.status_code == 200:
            logger.info("✓ Current IP lookup successful")
        
        return response
    
    def lookup_with_security(self, ip_address: str) -> dict:
        """
        Lookup IP with security information.
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Response object with security data
        """
        endpoint = f"/{ip_address}"
        params = {
            "access_key": self.access_key,
            "security": 1
        }
        
        logger.info(f"Looking up IP with security data: {ip_address}")
        response = self.get(endpoint, params=params)
        
        return response
    
    def lookup_with_hostname(self, ip_address: str) -> dict:
        """
        Lookup IP with hostname information.
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Response object with hostname data
        """
        endpoint = f"/{ip_address}"
        params = {
            "access_key": self.access_key,
            "hostname": 1
        }
        
        logger.info(f"Looking up IP with hostname: {ip_address}")
        response = self.get(endpoint, params=params)
        
        return response
    
    def bulk_lookup(self, ip_addresses: list) -> dict:
        """
        Lookup multiple IP addresses (bulk operation).
        Note: This requires a paid plan.
        
        Args:
            ip_addresses: List of IP addresses
            
        Returns:
            Response object with bulk lookup results
        """
        endpoint = f"/{','.join(ip_addresses)}"
        params = {"access_key": self.access_key}
        
        logger.info(f"Bulk lookup for {len(ip_addresses)} IPs")
        response = self.get(endpoint, params=params)
        
        return response


