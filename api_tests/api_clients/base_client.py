"""
Base API client with common HTTP methods.
"""
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAPIClient:
    """Base class for API clients."""
    
    def __init__(self, base_url: str, timeout: int = 30, verify_ssl: bool = True):
        """
        Initialize BaseAPIClient.
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = self._create_session()
        self.last_request = None
        self.last_response = None
        
        logger.info(f"Initialized API client with base URL: {self.base_url}")
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.
        
        Returns:
            requests.Session: Configured session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            str: Full URL
        """
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log request details."""
        logger.info(f"Request: {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"Request body: {kwargs['json']}")
        if 'params' in kwargs:
            logger.debug(f"Request params: {kwargs['params']}")
    
    def _log_response(self, response: requests.Response):
        """Log response details."""
        logger.info(f"Response: {response.status_code} - Time: {response.elapsed.total_seconds():.2f}s")
        try:
            logger.debug(f"Response body: {response.json()}")
        except:
            logger.debug(f"Response body: {response.text}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        headers = headers or {}
        
        self._log_request("GET", url, params=params)
        
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        self.last_request = {"method": "GET", "url": url, "params": params}
        self.last_response = response
        
        self._log_response(response)
        return response
    
    def post(self, endpoint: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            headers: Additional headers
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        headers = headers or {"Content-Type": "application/json"}
        
        self._log_request("POST", url, json=json)
        
        response = self.session.post(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        self.last_request = {"method": "POST", "url": url, "json": json}
        self.last_response = response
        
        self._log_response(response)
        return response
    
    def put(self, endpoint: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send PUT request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            headers: Additional headers
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        headers = headers or {"Content-Type": "application/json"}
        
        self._log_request("PUT", url, json=json)
        
        response = self.session.put(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        self.last_request = {"method": "PUT", "url": url, "json": json}
        self.last_response = response
        
        self._log_response(response)
        return response
    
    def patch(self, endpoint: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send PATCH request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            headers: Additional headers
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        headers = headers or {"Content-Type": "application/json"}
        
        self._log_request("PATCH", url, json=json)
        
        response = self.session.patch(
            url,
            json=json,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        self.last_request = {"method": "PATCH", "url": url, "json": json}
        self.last_response = response
        
        self._log_response(response)
        return response
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        headers = headers or {}
        
        self._log_request("DELETE", url)
        
        response = self.session.delete(
            url,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        self.last_request = {"method": "DELETE", "url": url}
        self.last_response = response
        
        self._log_response(response)
        return response
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("API client session closed")


