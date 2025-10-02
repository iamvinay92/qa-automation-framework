"""
API client for Objects endpoints.
"""
from typing import Dict, Any, List, Optional
import requests
from api_tests.api_clients.base_client import BaseAPIClient
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


class ObjectsClient(BaseAPIClient):
    """Client for Objects API operations."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize ObjectsClient.
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        super().__init__(base_url, timeout)
        self.created_ids: List[str] = []
        logger.info("ObjectsClient initialized")
    
    def create_object(self, data: Dict[str, Any]) -> requests.Response:
        """
        Create a new object.
        
        Args:
            data: Object data
            
        Returns:
            requests.Response: Response object
        """
        logger.info("Creating new object")
        response = self.post("/objects", json=data)
        
        # Track created object ID for cleanup
        if response.status_code == 200:
            try:
                object_id = response.json().get('id')
                if object_id:
                    self.created_ids.append(str(object_id))
                    logger.info(f"Object created with ID: {object_id}")
            except Exception as e:
                logger.warning(f"Could not track created object ID: {e}")
        
        return response
    
    def get_object(self, object_id: str) -> requests.Response:
        """
        Get an object by ID.
        
        Args:
            object_id: Object ID
            
        Returns:
            requests.Response: Response object
        """
        logger.info(f"Getting object: {object_id}")
        return self.get(f"/objects/{object_id}")
    
    def get_all_objects(self, params: Optional[Dict] = None) -> requests.Response:
        """
        Get all objects.
        
        Args:
            params: Optional query parameters
            
        Returns:
            requests.Response: Response object
        """
        logger.info("Getting all objects")
        return self.get("/objects", params=params)
    
    def update_object(self, object_id: str, data: Dict[str, Any]) -> requests.Response:
        """
        Update an object (PUT - full update).
        
        Args:
            object_id: Object ID
            data: Updated object data
            
        Returns:
            requests.Response: Response object
        """
        logger.info(f"Updating object: {object_id}")
        return self.put(f"/objects/{object_id}", json=data)
    
    def partial_update_object(self, object_id: str, data: Dict[str, Any]) -> requests.Response:
        """
        Partially update an object (PATCH).
        
        Args:
            object_id: Object ID
            data: Partial object data
            
        Returns:
            requests.Response: Response object
        """
        logger.info(f"Partially updating object: {object_id}")
        return self.patch(f"/objects/{object_id}", json=data)
    
    def delete_object(self, object_id: str) -> requests.Response:
        """
        Delete an object.
        
        Args:
            object_id: Object ID
            
        Returns:
            requests.Response: Response object
        """
        logger.info(f"Deleting object: {object_id}")
        response = self.delete(f"/objects/{object_id}")
        
        # Remove from tracked IDs if present
        if str(object_id) in self.created_ids:
            self.created_ids.remove(str(object_id))
        
        return response
    
    def verify_object_exists(self, object_id: str) -> bool:
        """
        Verify an object exists.
        
        Args:
            object_id: Object ID
            
        Returns:
            bool: True if object exists
        """
        response = self.get_object(object_id)
        exists = response.status_code == 200
        logger.info(f"Object {object_id} exists: {exists}")
        return exists
    
    def verify_object_deleted(self, object_id: str) -> bool:
        """
        Verify an object has been deleted.
        
        Args:
            object_id: Object ID
            
        Returns:
            bool: True if object is deleted (404)
        """
        response = self.get_object(object_id)
        deleted = response.status_code == 404
        logger.info(f"Object {object_id} deleted: {deleted}")
        return deleted


