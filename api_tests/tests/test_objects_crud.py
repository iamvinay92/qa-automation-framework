"""
Test cases for Objects API CRUD operations.

This test suite covers:
- Create (POST)
- Read (GET)
- Update (PUT)
- Delete (DELETE)
- List all objects (GET)
"""
import pytest
import allure
import json
from pathlib import Path
from api_tests.api_clients.objects_client import ObjectsClient
from api_tests.models.object_model import ObjectResponse, ObjectRequest
from api_tests.utils.api_helper import validate_response_time, generate_unique_name
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.crud
@pytest.mark.critical
@pytest.mark.skip(reason="Objects API daily limit reached (100 requests/day)")
@allure.feature("Objects API")
@allure.story("CRUD Operations")
class TestObjectsCRUD:
    """Test suite for Objects CRUD operations."""
    
    @allure.title("Create a new object")
    @allure.description("Test creating a new object with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_object(self, objects_client, sample_object_data):
        """
        Test ID: API-001
        Verify object creation with valid data.
        """
        with allure.step("Make POST request to create object"):
            response = objects_client.create_object(sample_object_data)
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response time is acceptable"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 35.0), \
                f"Response time {response_time}s exceeds limit"
        
        with allure.step("Verify response contains required fields"):
            response_json = response.json()
            assert 'id' in response_json, "Response should contain 'id'"
            assert 'name' in response_json, "Response should contain 'name'"
            assert response_json['name'] == sample_object_data['name'], \
                "Response name should match request"
        
        with allure.step("Validate response with Pydantic model"):
            object_response = ObjectResponse(**response_json)
            assert object_response.name == sample_object_data['name']
            logger.info(f"✓ Object created successfully with ID: {object_response.id}")
    
    @allure.title("Get object by ID")
    @allure.description("Test retrieving an object by its ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_get_object(self, objects_client, create_test_object):
        """
        Test ID: API-002
        Verify retrieving an object by ID.
        """
        object_id = create_test_object
        
        with allure.step(f"Make GET request for object ID: {object_id}"):
            response = objects_client.get_object(object_id)
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response time is acceptable"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 35.0), \
                f"Response time {response_time}s exceeds limit"
        
        with allure.step("Verify response contains object data"):
            response_json = response.json()
            assert response_json['id'] == object_id, \
                f"Expected ID {object_id}, got {response_json['id']}"
            assert 'name' in response_json, "Response should contain 'name'"
            logger.info(f"✓ Object retrieved successfully: {response_json['name']}")
    
    @allure.title("Update object (PUT)")
    @allure.description("Test full update of an object")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_update_object(self, objects_client, create_test_object):
        """
        Test ID: API-003
        Verify full object update (PUT).
        """
        object_id = create_test_object
        
        update_data = {
            "name": "Updated MacBook Pro 16",
            "data": {
                "year": 2024,
                "price": 2799.99,
                "CPU model": "Apple M3 Max",
                "Hard disk size": "1 TB"
            }
        }
        
        with allure.step(f"Make PUT request to update object {object_id}"):
            response = objects_client.update_object(object_id, update_data)
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response time is acceptable"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 35.0), \
                f"Response time {response_time}s exceeds limit"
        
        with allure.step("Verify updated data in response"):
            response_json = response.json()
            assert response_json['name'] == update_data['name'], \
                "Updated name should match request"
            assert 'updatedAt' in response_json, \
                "Response should contain updatedAt timestamp"
            logger.info(f"✓ Object updated successfully")
        
        with allure.step("Verify update by GET request"):
            get_response = objects_client.get_object(object_id)
            assert get_response.status_code == 200
            assert get_response.json()['name'] == update_data['name']
            logger.info("✓ Update verified with GET request")
    
    @allure.title("Delete object")
    @allure.description("Test deleting an object")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_delete_object(self, objects_client, create_test_object):
        """
        Test ID: API-004
        Verify object deletion.
        """
        object_id = create_test_object
        
        with allure.step(f"Make DELETE request for object {object_id}"):
            response = objects_client.delete_object(object_id)
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response time is acceptable"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 35.0), \
                f"Response time {response_time}s exceeds limit"
        
        with allure.step("Verify object is deleted"):
            # Try to get the deleted object
            get_response = objects_client.get_object(object_id)
            assert get_response.status_code == 404, \
                "Deleted object should return 404"
            logger.info(f"✓ Object deleted successfully and verified")
    
    @allure.title("Get all objects")
    @allure.description("Test retrieving list of all objects")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_all_objects(self, objects_client):
        """
        Test ID: API-005
        Verify retrieving list of all objects.
        """
        with allure.step("Make GET request for all objects"):
            response = objects_client.get_all_objects()
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response time is acceptable"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 35.0), \
                f"Response time {response_time}s exceeds limit"
        
        with allure.step("Verify response is a list"):
            response_json = response.json()
            assert isinstance(response_json, list), \
                "Response should be a list of objects"
            logger.info(f"✓ Retrieved {len(response_json)} objects")
    
    @allure.title("Partial update object (PATCH)")
    @allure.description("Test partial update of an object")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_partial_update_object(self, objects_client, create_test_object):
        """
        Test ID: API-006
        Verify partial object update (PATCH).
        """
        object_id = create_test_object
        
        # Get original object
        original_response = objects_client.get_object(object_id)
        original_data = original_response.json()
        
        partial_update = {
            "name": "Partially Updated Name"
        }
        
        with allure.step(f"Make PATCH request to partially update object {object_id}"):
            response = objects_client.partial_update_object(object_id, partial_update)
        
        with allure.step("Verify status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify only specified fields are updated"):
            response_json = response.json()
            assert response_json['name'] == partial_update['name'], \
                "Name should be updated"
            # Data field should remain unchanged
            if 'data' in original_data:
                assert response_json['data'] == original_data['data'], \
                    "Data field should remain unchanged"
            logger.info("✓ Partial update successful")


@pytest.mark.api
@pytest.mark.crud
@allure.feature("Objects API")
@allure.story("Parameterized CRUD Tests")
class TestObjectsCRUDParameterized:
    """Parameterized tests for multiple data sets."""
    
    @allure.title("Create objects with different data")
    @allure.description("Test creating multiple objects with various data")
    @pytest.mark.parametrize("device_name,device_data", [
        ("Apple iPhone 15", {"color": "Blue", "price": 999, "capacity": "128 GB"}),
        ("Samsung Galaxy S24", {"color": "Black", "price": 899, "capacity": "256 GB"}),
        ("Google Pixel 8", {"color": "Obsidian", "price": 699, "capacity": "128 GB"}),
    ])
    @pytest.mark.skip(reason="API endpoint returning 405 Method Not Allowed")
    def test_create_multiple_devices(self, objects_client, device_name, device_data):
        """
        Test ID: API-007
        Verify creating objects with different data sets.
        """
        payload = {
            "name": device_name,
            "data": device_data
        }
        
        with allure.step(f"Create object: {device_name}"):
            response = objects_client.create_object(payload)
        
        assert response.status_code == 200
        assert response.json()['name'] == device_name
        logger.info(f"✓ Successfully created: {device_name}")


@pytest.mark.api
@pytest.mark.performance
@allure.feature("Objects API")
@allure.story("Performance Tests")
class TestObjectsPerformance:
    """Performance tests for Objects API."""
    
    @allure.title("Verify response time for object creation")
    @allure.description("Ensure object creation completes within acceptable time")
    @pytest.mark.skip(reason="API endpoint returning 405 Method Not Allowed")
    def test_create_object_performance(self, objects_client, sample_object_data):
        """
        Test ID: API-008
        Verify API performance for object creation.
        """
        response = objects_client.create_object(sample_object_data)
        
        assert response.status_code == 200
        
        response_time = response.elapsed.total_seconds()
        max_time = 2.0
        
        assert response_time < max_time, \
            f"Response time {response_time:.2f}s exceeds acceptable limit of {max_time}s"
        
        logger.info(f"✓ Performance test passed: {response_time:.2f}s")


