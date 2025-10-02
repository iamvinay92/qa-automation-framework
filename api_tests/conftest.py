"""
Pytest configuration and fixtures for API tests.
"""
import pytest
import yaml
import os
from pathlib import Path
from api_tests.api_clients.objects_client import ObjectsClient
from api_tests.api_clients.ipstack_client import IpstackClient
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def api_config():
    """
    Load API configuration from YAML file.
    
    Returns:
        dict: API configuration
    """
    config_path = Path(__file__).parent / "config" / "config.yml"
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    logger.info(f"Loaded API configuration from {config_path}")
    return config


@pytest.fixture(scope="session")
def base_url(api_config):
    """
    Get base URL from configuration or environment.
    
    Returns:
        str: Base URL for API
    """
    url = os.getenv("API_BASE_URL", api_config['api']['base_url'])
    logger.info(f"Using base URL: {url}")
    return url


@pytest.fixture(scope="function")
def objects_client(base_url, api_config):
    """
    Create ObjectsClient instance for API testing.
    
    Args:
        base_url: Base URL for API
        api_config: API configuration
        
    Returns:
        ObjectsClient: Configured API client
    """
    client = ObjectsClient(
        base_url=base_url,
        timeout=api_config['api']['timeout']
    )
    logger.info("ObjectsClient created")
    
    yield client
    
    # Cleanup: Delete any test objects created
    if hasattr(client, 'created_ids'):
        for object_id in client.created_ids:
            try:
                client.delete_object(object_id)
                logger.info(f"Cleaned up test object: {object_id}")
            except Exception as e:
                logger.warning(f"Failed to cleanup object {object_id}: {e}")


@pytest.fixture(scope="function")
def sample_object_data():
    """
    Provide sample object data for testing.
    
    Returns:
        dict: Sample object data
    """
    return {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2023,
            "price": 2499.99,
            "CPU model": "Apple M3 Pro",
            "Hard disk size": "512 GB"
        }
    }


@pytest.fixture(scope="function")
def create_test_object(objects_client, sample_object_data):
    """
    Create a test object and return its ID.
    
    Args:
        objects_client: API client
        sample_object_data: Sample data
        
    Returns:
        str: Created object ID
    """
    response = objects_client.create_object(sample_object_data)
    assert response.status_code == 200, "Failed to create test object"
    
    object_id = response.json()['id']
    logger.info(f"Created test object with ID: {object_id}")
    
    yield object_id
    
    # Cleanup
    try:
        objects_client.delete_object(object_id)
        logger.info(f"Deleted test object: {object_id}")
    except Exception as e:
        logger.warning(f"Failed to delete test object {object_id}: {e}")


@pytest.fixture(scope="session")
def test_data_dir():
    """
    Get test data directory path.
    
    Returns:
        Path: Test data directory path
    """
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def ipstack_base_url(api_config):
    """
    Get ipstack base URL from configuration.
    
    Returns:
        str: Base URL for ipstack API
    """
    url = api_config['ipstack']['base_url']
    logger.info(f"Using ipstack base URL: {url}")
    return url


@pytest.fixture(scope="session")
def ipstack_access_key(api_config):
    """
    Get ipstack access key from configuration or environment.
    
    Returns:
        str: Access key for ipstack API
    """
    key = os.getenv("IPSTACK_ACCESS_KEY", api_config['ipstack']['access_key'])
    logger.info("ipstack access key loaded")
    return key


@pytest.fixture(scope="function")
def ipstack_client(ipstack_base_url, ipstack_access_key, api_config):
    """
    Create IpstackClient instance for API testing.
    
    Args:
        ipstack_base_url: Base URL for ipstack API
        ipstack_access_key: Access key for authentication
        api_config: API configuration
        
    Returns:
        IpstackClient: Configured ipstack API client
    """
    client = IpstackClient(
        base_url=ipstack_base_url,
        access_key=ipstack_access_key,
        timeout=api_config['ipstack']['timeout']
    )
    logger.info("IpstackClient created")
    
    yield client
    
    # No cleanup needed for read-only API
    logger.info("IpstackClient session closed")


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test start and end information."""
    test_name = request.node.nodeid
    logger.info(f"{'='*80}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'='*80}")
    
    yield
    
    logger.info(f"{'='*80}")
    logger.info(f"Finished test: {test_name}")
    logger.info(f"{'='*80}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and attach request/response data to reports.
    
    Args:
        item: Test item
        call: Test call info
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Add request/response data to allure report if available
        if hasattr(item, "funcargs") and "objects_client" in item.funcargs:
            client = item.funcargs["objects_client"]
            
            if hasattr(client, 'last_request') and hasattr(client, 'last_response'):
                try:
                    import allure
                    
                    # Attach request details
                    allure.attach(
                        str(client.last_request),
                        name="Last Request",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Attach response details
                    allure.attach(
                        str(client.last_response),
                        name="Last Response",
                        attachment_type=allure.attachment_type.JSON
                    )
                except ImportError:
                    pass


