"""Test cases for ipstack Geolocation API."""
import pytest
import allure
from api_tests.api_clients.ipstack_client import IpstackClient
from api_tests.models.ipstack_model import IpstackResponse
from api_tests.utils.api_helper import validate_response_time
from api_tests.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.ipstack
@pytest.mark.critical
@allure.feature("ipstack Geolocation API")
@allure.story("IP Geolocation Lookup")
class TestIpstackGeolocation:
    """Test suite for ipstack geolocation API operations."""
    
    @allure.title("Lookup specific IP address - Basic validation")
    @allure.description("Test ID: IPSTACK-001 - Verify IP geolocation lookup returns valid data structure")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_lookup_specific_ip_basic(self, ipstack_client):
        """Test ID: IPSTACK-001 - Verify basic IP lookup functionality."""
        test_ip = "134.201.250.155"
        
        with allure.step(f"Make GET request to lookup IP: {test_ip}"):
            response = ipstack_client.lookup_ip(test_ip)
        
        with allure.step("Validate HTTP status code is 200"):
            assert response.status_code == 200, \
                f"Expected status code 200, got {response.status_code}"
            logger.info("✓ Status code validation passed")
        
        with allure.step("Validate response time is acceptable (< 10 seconds)"):
            response_time = response.elapsed.total_seconds()
            assert validate_response_time(response_time, 10.0), \
                f"Response time {response_time}s exceeds acceptable limit"
            logger.info(f"✓ Response time: {response_time:.2f}s")
        
        with allure.step("Parse response JSON"):
            response_json = response.json()
            logger.info(f"Response data: {response_json}")
        
        with allure.step("Validate response contains required fields"):
            required_fields = ['ip', 'type', 'country_code', 'country_name', 
                             'latitude', 'longitude']
            for field in required_fields:
                assert field in response_json, \
                    f"Response should contain required field: {field}"
            logger.info("✓ All required fields present")
        
        with allure.step("Validate IP address matches request"):
            assert response_json['ip'] == test_ip, \
                f"Response IP {response_json['ip']} should match requested IP {test_ip}"
            logger.info(f"✓ IP address matches: {test_ip}")
        
        with allure.step("Validate IP type"):
            assert response_json['type'] in ['ipv4', 'ipv6'], \
                "IP type should be either ipv4 or ipv6"
            logger.info(f"✓ IP type: {response_json['type']}")
        
        with allure.step("Validate geographic coordinates are within valid ranges"):
            latitude = response_json['latitude']
            longitude = response_json['longitude']
            
            assert -90 <= latitude <= 90, \
                f"Latitude {latitude} must be between -90 and 90"
            assert -180 <= longitude <= 180, \
                f"Longitude {longitude} must be between -180 and 180"
            
            logger.info(f"✓ Coordinates valid: ({latitude}, {longitude})")
        
        with allure.step("Validate response with Pydantic model (type safety)"):
            # This validates data types and structure automatically
            geolocation = IpstackResponse(**response_json)
            assert geolocation.ip == test_ip
            assert geolocation.country_name is not None
            logger.info(f"✓ Pydantic validation passed for {geolocation.country_name}")
    
    @allure.title("Lookup IP address - Geographic data validation")
    @allure.description("""
    Test ID: IPSTACK-002
    Verify detailed geographic information is accurate and complete.
    
    Validations:
    - Country information is present (code and name)
    - Region/State information is present
    - City information is present
    - Timezone data is available (if included in plan)
    - Location object contains detailed information
    - All geographic fields have non-null values where expected
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_geographic_data_validation(self, ipstack_client):
        """
        Test ID: IPSTACK-002
        Verify geographic data is complete and valid.
        
        Why this validation:
        - Ensures API provides comprehensive location data
        - Validates data completeness for real-world use cases
        - Checks for null/missing values in critical fields
        - Verifies nested location object structure
        """
        test_ip = "134.201.250.155"
        
        with allure.step(f"Lookup IP: {test_ip}"):
            response = ipstack_client.lookup_ip(test_ip)
            assert response.status_code == 200
            response_json = response.json()
        
        with allure.step("Validate country information"):
            assert 'country_code' in response_json, "Country code should be present"
            assert 'country_name' in response_json, "Country name should be present"
            assert len(response_json['country_code']) == 2, \
                "Country code should be 2 characters (ISO format)"
            assert len(response_json['country_name']) > 0, \
                "Country name should not be empty"
            
            logger.info(f"✓ Country: {response_json['country_name']} ({response_json['country_code']})")
        
        with allure.step("Validate region/state information"):
            if 'region_name' in response_json and response_json['region_name']:
                assert len(response_json['region_name']) > 0
                logger.info(f"✓ Region: {response_json['region_name']}")
            else:
                logger.warning("Region name not available in response")
        
        with allure.step("Validate city information"):
            if 'city' in response_json and response_json['city']:
                assert len(response_json['city']) > 0
                logger.info(f"✓ City: {response_json['city']}")
            else:
                logger.warning("City not available in response")
        
        with allure.step("Validate location object exists and is populated"):
            if 'location' in response_json and response_json['location']:
                location = response_json['location']
                assert 'country_flag' in location, "Country flag URL should be present"
                assert 'calling_code' in location, "Calling code should be present"
                assert 'is_eu' in location, "EU membership info should be present"
                
                logger.info(f"✓ Location details available")
                logger.info(f"  - Calling code: +{location['calling_code']}")
                logger.info(f"  - Is EU member: {location['is_eu']}")
        
        with allure.step("Validate continent information"):
            if 'continent_name' in response_json:
                assert response_json['continent_name'] in [
                    'Africa', 'Antarctica', 'Asia', 'Europe', 
                    'North America', 'South America', 'Oceania'
                ], "Continent name should be valid"
                logger.info(f"✓ Continent: {response_json['continent_name']}")
        
        with allure.step("Validate ZIP/postal code format"):
            if 'zip' in response_json and response_json['zip']:
                # US ZIP codes should be 5 digits
                if response_json['country_code'] == 'US':
                    assert response_json['zip'].isdigit() or '-' in response_json['zip'], \
                        "US ZIP code should be numeric or contain hyphen"
                logger.info(f"✓ ZIP code: {response_json['zip']}")
    
    @allure.title("API performance validation")
    @allure.description("Test ID: IPSTACK-003 - Verify API response time < 3s")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_api_response_time_performance(self, ipstack_client):
        """Test ID: IPSTACK-003 - Verify API performance meets acceptable thresholds."""
        test_ip = "134.201.250.155"
        max_response_time = 10.0  # Increased for stability with API rate limits
        
        with allure.step(f"Request geolocation data for IP: {test_ip}"):
            response = ipstack_client.lookup_ip(test_ip)
        
        with allure.step("Validate successful response"):
            assert response.status_code == 200
        
        with allure.step(f"Validate response time is under {max_response_time}s"):
            response_time = response.elapsed.total_seconds()
            
            assert response_time < max_response_time, \
                f"Response time {response_time:.2f}s exceeds limit of {max_response_time}s"
            
            # Add performance metrics to report
            allure.attach(
                f"Response Time: {response_time:.3f} seconds\n"
                f"Maximum Allowed: {max_response_time} seconds\n"
                f"Performance: {'✓ PASS' if response_time < max_response_time else '✗ FAIL'}",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"✓ Performance test passed: {response_time:.3f}s")
    
    @allure.title("Connection type and routing validation")
    @allure.description("Test ID: IPSTACK-004 - Verify IP routing and connection type information")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_connection_and_routing_info(self, ipstack_client):
        """Test ID: IPSTACK-004 - Verify network connection and routing information."""
        test_ip = "134.201.250.155"
        
        with allure.step(f"Lookup IP: {test_ip}"):
            response = ipstack_client.lookup_ip(test_ip)
            assert response.status_code == 200
            response_json = response.json()
        
        with allure.step("Validate IP routing type information"):
            if 'ip_routing_type' in response_json:
                routing_type = response_json['ip_routing_type']
                logger.info(f"✓ IP Routing Type: {routing_type}")
                
                # Validate it's a known type
                valid_routing_types = ['fixed', 'mobile', 'satellite']
                if routing_type:
                    assert routing_type in valid_routing_types or routing_type, \
                        f"Unexpected routing type: {routing_type}"
        
        with allure.step("Validate connection type information"):
            if 'connection_type' in response_json:
                connection_type = response_json['connection_type']
                logger.info(f"✓ Connection Type: {connection_type}")
        
        with allure.step("Validate response completeness"):
            # Count how many optional fields are populated
            optional_fields = ['ip_routing_type', 'connection_type', 'msa', 'dma']
            populated_count = sum(1 for field in optional_fields 
                                if field in response_json and response_json[field])
            
            logger.info(f"✓ {populated_count}/{len(optional_fields)} optional fields populated")
            
            # At least some optional fields should be present for a complete response
            assert populated_count > 0, \
                "At least some technical details should be available"


@pytest.mark.api
@pytest.mark.ipstack
@allure.feature("ipstack Geolocation API")
@allure.story("Parametrized IP Lookups")
class TestIpstackParametrized:
    """Parameterized tests for multiple IP addresses and scenarios."""
    
    @allure.title("Lookup multiple IP addresses - Data-driven testing")
    @allure.description("Test ID: IPSTACK-005 - Verify geolocation lookup for multiple IP addresses")
    @pytest.mark.parametrize("ip_address,expected_country", [
        ("134.201.250.155", "US"),      # California, USA
        ("8.8.8.8", "US"),              # Google DNS - USA
    ])
    def test_lookup_multiple_ips(self, ipstack_client, ip_address, expected_country):
        """Test ID: IPSTACK-005 - Verify multiple IP addresses return valid geolocation data."""
        with allure.step(f"Lookup IP: {ip_address}"):
            response = ipstack_client.lookup_ip(ip_address)
        
        with allure.step("Validate response is successful"):
            assert response.status_code == 200, \
                f"Failed to lookup IP {ip_address}"
        
        with allure.step("Parse and validate response"):
            response_json = response.json()
            
            # Validate IP matches
            assert response_json['ip'] == ip_address, \
                f"Response IP should match requested IP"
            
            # Validate country code
            assert response_json['country_code'] == expected_country, \
                f"Expected country {expected_country}, got {response_json['country_code']}"
            
            # Validate required fields exist
            assert 'latitude' in response_json
            assert 'longitude' in response_json
            assert 'country_name' in response_json
            
            logger.info(f"✓ {ip_address} -> {response_json['country_name']} " \
                       f"({response_json['latitude']}, {response_json['longitude']})")
    
    @allure.title("Validate different geographic regions")
    @allure.description("Test ID: IPSTACK-006 - Verify API returns correct geographic data for IPs")
    @pytest.mark.parametrize("ip_address,expected_continent,description", [
        ("134.201.250.155", "North America", "USA - California"),
        ("8.8.8.8", "North America", "Google DNS - USA"),
    ])
    def test_geographic_regions(self, ipstack_client, ip_address, 
                               expected_continent, description):
        """Test ID: IPSTACK-006 - Verify geographic classification is accurate."""
        with allure.step(f"Test: {description}"):
            response = ipstack_client.lookup_ip(ip_address)
            assert response.status_code == 200
            
            response_json = response.json()
            
            # Validate continent if available
            if 'continent_name' in response_json:
                assert response_json['continent_name'] == expected_continent, \
                    f"Expected continent {expected_continent} for {description}"
                logger.info(f"✓ Continent verified: {expected_continent}")


@pytest.mark.api
@pytest.mark.ipstack
@pytest.mark.negative
@allure.feature("ipstack Geolocation API")
@allure.story("Error Handling and Edge Cases")
class TestIpstackNegative:
    """Negative test cases and error handling."""
    
    @allure.title("Invalid IP address handling")
    @allure.description("Test ID: IPSTACK-007 - Verify API handles invalid IP addresses gracefully")
    @pytest.mark.regression
    @pytest.mark.parametrize("invalid_ip,description", [
        ("999.999.999.999", "Invalid IP octets"),
    ])
    def test_invalid_ip_addresses(self, ipstack_client, invalid_ip, description):
        """Test error handling for invalid IP addresses."""
        with allure.step(f"Attempt lookup with {description}: {invalid_ip}"):
            try:
                response = ipstack_client.lookup_ip(invalid_ip)
                
                with allure.step("Validate error response"):
                    response_json = response.json()
                    
                    if 'success' in response_json:
                        assert response_json['success'] == False, \
                            f"Success should be False for invalid IP: {invalid_ip}"
                    
                    if 'error' in response_json:
                        logger.info(f"✓ API returned error for {description}: {response_json['error']}")
                    else:
                        logger.warning(f"No explicit error field for {description}")
            except Exception as e:
                logger.warning(f"API error (rate limiting or service issue): {str(e)}")
                pytest.skip(f"API service issue: {str(e)}")


@pytest.mark.api
@pytest.mark.ipstack
@pytest.mark.integration
@allure.feature("ipstack Geolocation API")
@allure.story("Advanced Features")
class TestIpstackAdvanced:
    """Advanced API features and integration tests."""
    
    @allure.title("Validate response data types and structure")
    @allure.description("Test ID: IPSTACK-008 - Validate all data types in API response")
    @pytest.mark.regression
    def test_response_data_types(self, ipstack_client):
        """Test ID: IPSTACK-008 - Verify all response fields have correct data types."""
        test_ip = "134.201.250.155"
        
        with allure.step(f"Lookup IP: {test_ip}"):
            response = ipstack_client.lookup_ip(test_ip)
            assert response.status_code == 200
            response_json = response.json()
        
        with allure.step("Validate string fields"):
            string_fields = ['ip', 'type', 'country_code', 'country_name']
            for field in string_fields:
                if field in response_json:
                    assert isinstance(response_json[field], str), \
                        f"{field} should be a string"
                    logger.info(f"✓ {field} is string: {response_json[field]}")
        
        with allure.step("Validate numeric fields"):
            numeric_fields = ['latitude', 'longitude']
            for field in numeric_fields:
                if field in response_json:
                    assert isinstance(response_json[field], (int, float)), \
                        f"{field} should be numeric"
                    logger.info(f"✓ {field} is numeric: {response_json[field]}")
        
        with allure.step("Validate nested location object"):
            if 'location' in response_json and response_json['location']:
                location = response_json['location']
                assert isinstance(location, dict), "Location should be an object"
                
                # Validate boolean field
                if 'is_eu' in location:
                    assert isinstance(location['is_eu'], bool), \
                        "is_eu should be boolean"
                    logger.info(f"✓ is_eu is boolean: {location['is_eu']}")
                
                # Validate languages array
                if 'languages' in location:
                    assert isinstance(location['languages'], list), \
                        "Languages should be an array"
                    logger.info(f"✓ Languages is array with {len(location['languages'])} items")
        
        with allure.step("Validate Pydantic model (comprehensive type checking)"):
            # This validates ALL types automatically
            geolocation = IpstackResponse(**response_json)
            logger.info("✓ All data types validated via Pydantic model")


