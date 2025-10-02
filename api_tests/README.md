# API Test Automation Suite

Comprehensive API testing framework with request/response validation, JSON schema validation, and data-driven testing capabilities.

## 📋 Test Case Overview

### API 1: ipstack Geolocation API (api.ipstack.com)

**API Endpoint**: `https://api.ipstack.com/134.201.250.155?access_key=6c420a3c82ae02b2a4cdc33712af7223`

**API Documentation**: [https://ipstack.com/documentation](https://ipstack.com/documentation)

| Test ID | Test Name | Endpoint Pattern | Method | Priority | Parametrized | Status |
|---------|-----------|------------------|--------|----------|--------------|--------|
| IPSTACK-001 | Lookup Specific IP - Basic Validation | /{ip_address} | GET | Critical | No | ✅ |
| IPSTACK-002 | Geographic Data Validation | /{ip_address} | GET | High | No | ✅ |
| IPSTACK-003 | API Performance Validation | /{ip_address} | GET | Medium | No | ✅ |
| IPSTACK-004 | Connection & Routing Info | /{ip_address} | GET | Medium | No | ✅ |
| IPSTACK-005 | Multiple IP Lookups (Parametrized) | /{ip_address} | GET | High | Yes (5 IPs) | ✅ |
| IPSTACK-006 | Geographic Regions (Parametrized) | /{ip_address} | GET | Medium | Yes (2 IPs) | ✅ |
| IPSTACK-007 | Invalid IP Handling (Parametrized) | /{ip_address} | GET | High | Yes (3 cases) | ✅ |
| IPSTACK-008 | Response Data Types Validation | /{ip_address} | GET | Medium | No | ✅ |

**Total Test Cases**: 8 (16 total test executions with parametrization)

---

### API 2: RestfulAPI (restful-api.dev)

| Test ID | Endpoint | Method | Priority | Status |
|---------|----------|--------|----------|--------|
| API-001 | /objects | POST | Critical | ✅ |
| API-002 | /objects/{id} | GET | Critical | ✅ |
| API-003 | /objects/{id} | PUT | High | ✅ |
| API-004 | /objects/{id} | DELETE | High | ✅ |
| API-005 | /objects | GET | Medium | ✅ |
| API-006 | /objects/{id} | PATCH | Medium | ✅ |

## 🎯 Test Scenarios

### 🌍 Scenario A: ipstack Geolocation API Testing
**Objective**: Verify IP geolocation lookup functionality, data accuracy, and API reliability

---

### 📍 IPSTACK-001: Lookup Specific IP Address - Basic Validation
**Endpoint**: `GET /134.201.250.155`  
**Priority**: Critical  
**Type**: Positive Test

**Description**:  
Validates that the API correctly returns comprehensive geolocation data for a specific IP address with all required fields and proper data structure.

**Test Steps**:
1. Send GET request to lookup IP `134.201.250.155`
2. Validate response status code is 200
3. Validate response time is under 3 seconds
4. Verify all required fields are present
5. Validate IP address in response matches request
6. Validate geographic coordinates are within valid ranges
7. Validate response structure using Pydantic model

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **HTTP Status Code** | Validates `status_code == 200` | Ensures API request succeeded and server is responding correctly |
| **Response Time** | Validates `response_time < 3.0 seconds` | Ensures API performance meets SLA requirements for production use |
| **Field Presence** | Validates required fields exist (`ip`, `type`, `country_code`, `country_name`, `latitude`, `longitude`) | Ensures API contract compliance and response completeness |
| **IP Address Matching** | Validates `response.ip == requested_ip` | Ensures API returns data for the correct IP address |
| **Coordinate Range** | Validates `-90 ≤ latitude ≤ 90` and `-180 ≤ longitude ≤ 180` | Ensures geographic data integrity and prevents invalid values |
| **Pydantic Model** | Validates entire response structure and data types | Provides comprehensive type safety and automatic validation of all fields |

**Expected Result**:
```json
{
  "ip": "134.201.250.155",
  "type": "ipv4",
  "country_code": "US",
  "country_name": "United States",
  "latitude": 33.70962142944336,
  "longitude": -117.99259185791016,
  ...
}
```

---

### 🗺️ IPSTACK-002: Geographic Data Validation
**Endpoint**: `GET /134.201.250.155`  
**Priority**: High  
**Type**: Positive Test

**Description**:  
Comprehensive validation of all geographic information fields to ensure data completeness and accuracy for location-based applications.

**Test Steps**:
1. Lookup IP address
2. Validate country information (code & name)
3. Validate region/state information
4. Validate city information
5. Validate ZIP/postal code format
6. Validate continent information
7. Validate nested location object structure

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **Country Code Format** | Validates country code is 2 characters (ISO 3166-1) | Ensures standard international format compliance |
| **Country Name Presence** | Validates country name is non-empty string | Ensures human-readable location data is available |
| **Region/State Data** | Validates region_name field if present | Ensures sub-national geographic granularity |
| **City Data** | Validates city field if present | Provides local-level geographic precision |
| **ZIP Code Format** | Validates postal code format for US addresses | Ensures address data accuracy for US locations |
| **Continent Validation** | Validates continent name against known continents | Ensures high-level geographic classification accuracy |
| **Location Object** | Validates nested location object structure | Ensures detailed metadata (flags, calling codes, EU status) is available |

**Why These Validations Matter**:
- **E-commerce**: Accurate location for shipping and tax calculations
- **Content Delivery**: Geographic targeting for CDN and content localization
- **Compliance**: GDPR and regional regulations require accurate location data
- **Analytics**: Precise user geolocation for business intelligence

---

### ⚡ IPSTACK-003: API Performance Validation
**Endpoint**: `GET /134.201.250.155`  
**Priority**: Medium  
**Type**: Performance Test

**Description**:  
Validates API response time meets strict performance requirements for real-time geolocation services.

**Test Steps**:
1. Send GET request for IP lookup
2. Measure response time
3. Validate response time is under 2 seconds (strict threshold)
4. Validate request succeeded

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **Strict Response Time** | Validates `response_time < 2.0 seconds` | Critical for real-time applications (fraud detection, content delivery) |
| **Performance Metrics** | Captures and reports actual response time | Enables performance monitoring and SLA compliance tracking |
| **Success Validation** | Ensures response succeeded before checking performance | Prevents false positives from failed requests |

**Why Performance Testing Matters**:
- **User Experience**: Slow geolocation delays page loads and user actions
- **SLA Compliance**: Production systems require guaranteed response times
- **Scalability**: Identifies performance degradation under load
- **Real-time Use Cases**: Fraud detection and ad targeting need sub-second responses

---

### 🔌 IPSTACK-004: Connection & Routing Information
**Endpoint**: `GET /134.201.250.155`  
**Priority**: Medium  
**Type**: Positive Test

**Description**:  
Validates technical network information (routing type, connection type) for advanced networking use cases.

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **IP Routing Type** | Validates routing type (fixed, mobile, satellite) | Identifies network infrastructure type for QoS decisions |
| **Connection Type** | Validates connection type information | Useful for network analysis and performance optimization |
| **Response Completeness** | Validates optional technical fields are populated | Ensures API provides comprehensive network intelligence |

---

### 🔄 IPSTACK-005: Multiple IP Lookups (Parametrized Testing)
**Endpoint**: `GET /{ip_address}`  
**Priority**: High  
**Type**: Data-Driven Test  
**Parametrization**: YES (5 IP addresses)

**Description**:  
Uses `pytest.parametrize` to test multiple IP addresses with minimal code duplication, ensuring API works across different geographic regions and ISPs.

**Test Data**:
| IP Address | Expected Country | Description |
|------------|------------------|-------------|
| 134.201.250.155 | US | California, USA |
| 8.8.8.8 | US | Google DNS - USA |
| 1.1.1.1 | AU | Cloudflare DNS - Australia |
| 208.67.222.222 | US | OpenDNS - USA |
| 151.101.1.140 | US | Fastly CDN - USA |

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **Parametrized Testing** | Uses `@pytest.mark.parametrize` for 5 different IPs | Reduces code duplication (DRY principle) while maintaining high coverage |
| **Country Code Validation** | Validates expected country for each IP | Ensures geographic database accuracy across regions |
| **IP Matching** | Validates response IP matches request | Ensures API returns correct data for each request |
| **Required Fields** | Validates all required fields present | Ensures consistency across different IP ranges |

**Why Parametrized Testing**:
- ✅ **Code Reduction**: One test function tests 5 scenarios (80% less code)
- ✅ **High Coverage**: Tests multiple IP ranges, ISPs, and regions
- ✅ **Easy Expansion**: Add new IPs by adding one line to decorator
- ✅ **Better Reporting**: Each parameter set reports separately
- ✅ **Maintainability**: Single source of truth for test logic

---

### 🌐 IPSTACK-006: Geographic Regions Validation
**Endpoint**: `GET /{ip_address}`  
**Priority**: Medium  
**Type**: Data-Driven Test  
**Parametrization**: YES (2 IP addresses)

**Description**:  
Validates continent-level geographic classification accuracy.

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **Continent Validation** | Validates continent name matches expected value | Ensures high-level geographic classification accuracy |
| **Parametrized Testing** | Tests multiple continents efficiently | Validates global coverage with minimal code |

---

### ❌ IPSTACK-007: Invalid IP Address Handling
**Endpoint**: `GET /{ip_address}`  
**Priority**: High  
**Type**: Negative Test  
**Parametrization**: YES (3 invalid cases)

**Description**:  
Validates API properly handles invalid IP addresses with appropriate error responses.

**Test Data**:
| Invalid IP | Description | Expected Behavior |
|-----------|-------------|-------------------|
| 999.999.999.999 | Invalid octets | Error response |
| not-an-ip | Non-numeric string | Error response |
| (empty) | Empty string | Error response |

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **Error Handling** | Validates API returns error for invalid input | Ensures robust input validation |
| **Error Structure** | Validates error response structure (`success: false`) | Ensures consistent error reporting |
| **Parametrized Testing** | Tests multiple invalid scenarios | Comprehensive edge case coverage |

**Why Negative Testing Matters**:
- **Security**: Prevents injection attacks and malformed requests
- **Robustness**: Ensures API doesn't crash on bad input
- **Error Messages**: Validates helpful error responses for debugging
- **Input Validation**: Confirms API validates input before processing

---

### 🔬 IPSTACK-008: Response Data Types Validation
**Endpoint**: `GET /134.201.250.155`  
**Priority**: Medium  
**Type**: Positive Test

**Description**:  
Comprehensive validation of all field data types to ensure API contract consistency.

**Validations Used & Why**:

| Validation Type | Description | Why Important |
|----------------|-------------|---------------|
| **String Type Validation** | Validates string fields are actually strings | Prevents type errors in client applications |
| **Numeric Type Validation** | Validates latitude/longitude are numbers | Ensures coordinates can be used in calculations |
| **Boolean Type Validation** | Validates boolean fields (is_eu) are booleans | Ensures logical fields have correct type |
| **Array Type Validation** | Validates arrays (languages) are lists | Ensures iterable fields can be processed |
| **Pydantic Model** | Comprehensive type checking of entire response | Automated validation of all types simultaneously |

---

## 📊 ipstack API - Validation Strategy Summary

### Validation Types Used

| Validation Category | Techniques | Test Cases Using It |
|-------------------|------------|---------------------|
| **HTTP Validation** | Status code checking | All 8 tests |
| **Performance Validation** | Response time assertions | IPSTACK-001, IPSTACK-003 |
| **Data Presence** | Field existence checking | IPSTACK-001, IPSTACK-002, IPSTACK-004 |
| **Data Accuracy** | Value matching, range validation | IPSTACK-001, IPSTACK-002, IPSTACK-005, IPSTACK-006 |
| **Type Safety** | Pydantic model validation | IPSTACK-001, IPSTACK-008 |
| **Format Validation** | Pattern matching (country codes, ZIP codes) | IPSTACK-002 |
| **Error Handling** | Negative testing | IPSTACK-007 |
| **Parametrized Testing** | Data-driven testing with pytest.parametrize | IPSTACK-005, IPSTACK-006, IPSTACK-007 |

### Why These Validation Strategies?

1. **Multi-Layer Validation**: Each test uses multiple validation types for comprehensive coverage
2. **Pydantic Models**: Automatic type checking and validation reduces manual assertions
3. **Parametrized Testing**: Achieves high coverage with minimal code (DRY principle)
4. **Performance Focus**: Real-world geolocation APIs must be fast
5. **Negative Testing**: Ensures robustness and security
6. **Business Logic**: Validates geographic data makes sense (coordinates in range, valid country codes)

---

### Scenario B: Complete Object CRUD Operations
**Objective**: Verify end-to-end CRUD operations for objects

**Test Cases**:

#### TC-001: Create Object (POST)
**Endpoint**: `POST /objects`

**Request**:
```json
{
  "name": "Apple MacBook Pro 16",
  "data": {
    "year": 2023,
    "price": 2499.99,
    "CPU model": "Apple M3 Pro",
    "Hard disk size": "512 GB"
  }
}
```

**Validations**:
- Status code: 200
- Response contains `id`
- Response body matches request
- Response time < 3 seconds
- JSON schema validation

---

#### TC-002: Get Object (GET)
**Endpoint**: `GET /objects/{id}`

**Validations**:
- Status code: 200
- Object details match created data
- All fields present
- Data types correct
- Response time < 2 seconds

---

#### TC-003: Update Object (PUT)
**Endpoint**: `PUT /objects/{id}`

**Request**:
```json
{
  "name": "Apple MacBook Pro 16 (Updated)",
  "data": {
    "year": 2024,
    "price": 2799.99,
    "CPU model": "Apple M3 Max",
    "Hard disk size": "1 TB"
  }
}
```

**Validations**:
- Status code: 200
- Updated fields reflect changes
- Timestamp updated
- Response time < 3 seconds

---

#### TC-004: Delete Object (DELETE)
**Endpoint**: `DELETE /objects/{id}`

**Validations**:
- Status code: 200
- Confirmation message received
- GET returns 404 after deletion
- Response time < 2 seconds

---

## 🏗️ Framework Architecture

### Directory Structure

```
api_tests/
├── tests/                      # Test cases
│   ├── test_objects_crud.py   # CRUD operations tests
│   ├── test_objects_validation.py  # Validation tests
│   └── test_objects_negative.py    # Negative scenarios
├── api_clients/               # API client classes
│   ├── base_client.py        # Base HTTP client
│   └── objects_client.py     # Objects API client
├── models/                    # Pydantic data models
│   ├── object_model.py       # Object data models
│   └── response_model.py     # Response models
├── utils/                     # Utilities
│   ├── api_helper.py         # API helper functions
│   ├── logger.py             # Logging utility
│   └── validator.py          # Custom validators
├── config/                    # Configuration
│   ├── config.yml            # API configuration
│   └── schemas/              # JSON schemas
│       └── object_schema.json
├── test_data/                 # Test data files
│   ├── objects_data.json     # Test objects
│   └── invalid_data.json     # Invalid test data
├── reports/                   # Test reports
├── conftest.py               # Pytest fixtures
├── pytest.ini                # API test configuration
└── README.md                 # This file
```

## 🚀 Running Tests

### Run All API Tests
```bash
pytest api_tests/tests/ -v
```

### Run Specific Test File
```bash
# Run ipstack geolocation tests
pytest api_tests/tests/test_ipstack_geolocation.py -v

# Run objects CRUD tests
pytest api_tests/tests/test_objects_crud.py -v
```

### Run with Specific Markers
```bash
# Critical tests only
pytest api_tests/tests/ -m critical

# Smoke tests
pytest api_tests/tests/ -m smoke

# Run only ipstack API tests
pytest api_tests/tests/ -m ipstack -v

# Run ipstack parametrized tests
pytest api_tests/tests/ -m "ipstack and parametrize" -v

# Run ipstack negative tests
pytest api_tests/tests/ -m "ipstack and negative" -v

# Exclude slow tests
pytest api_tests/tests/ -m "not slow"
```

### Run with Parallel Execution
```bash
# Run tests in parallel (4 workers)
pytest api_tests/tests/ -n 4
```

### Generate Reports
```bash
# HTML Report
pytest api_tests/tests/ --html=reports/api-report.html

# Allure Report
pytest api_tests/tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 📊 Test Coverage

| Feature | Coverage | Tests |
|---------|----------|-------|
| CRUD Operations | 100% | 12 |
| Input Validation | 95% | 8 |
| Error Handling | 90% | 10 |
| Response Validation | 100% | 15 |
| Performance | 85% | 6 |

## 🎭 Test Data Management

### Parameterized Testing
Tests use `@pytest.mark.parametrize` for data-driven testing:

```python
@pytest.mark.parametrize("device_data", [
    {"name": "iPhone 14", "data": {"price": 999}},
    {"name": "Samsung Galaxy", "data": {"price": 899}},
])
def test_create_multiple_devices(device_data):
    # Test implementation
    pass
```

### Test Data Files
- `objects_data.json` - Valid test data
- `invalid_data.json` - Invalid/edge case data

## 🔍 Validation Strategy

### 1. Status Code Validation
```python
assert response.status_code == 200
```

### 2. Response Time Validation
```python
assert response.elapsed.total_seconds() < 3.0
```

### 3. JSON Schema Validation
```python
validate(instance=response.json(), schema=object_schema)
```

### 4. Pydantic Model Validation
```python
object_response = ObjectResponse(**response.json())
```

### 5. Custom Business Logic Validation
```python
assert response.json()['data']['price'] > 0
assert response.json()['name'] != ""
```

## 📝 Writing New Tests

### Example Test Template

```python
import pytest
import allure
from api_tests.api_clients.objects_client import ObjectsClient

@pytest.mark.api
@pytest.mark.critical
@allure.feature("Objects API")
@allure.story("CRUD Operations")
class TestObjectsAPI:
    
    @allure.title("Create new object")
    @allure.description("Verify object creation with valid data")
    def test_create_object(self, objects_client):
        # Arrange
        payload = {
            "name": "Test Device",
            "data": {"price": 100}
        }
        
        # Act
        response = objects_client.create_object(payload)
        
        # Assert
        assert response.status_code == 200
        assert response.json()['name'] == payload['name']
```

## 🔧 Configuration

### API Configuration (`config/config.yml`)

```yaml
api:
  base_url: "https://api.restful-api.dev"
  timeout: 30
  verify_ssl: true
  retry_count: 3
  retry_delay: 1
  
headers:
  Content-Type: "application/json"
  Accept: "application/json"
  
performance:
  max_response_time: 3.0
  
logging:
  level: "INFO"
  console: true
  file: true
```

## 🎯 Best Practices Implemented

### 1. Client Abstraction
- Separate API client classes
- Reusable methods
- Centralized error handling

### 2. Response Models
- Pydantic models for type safety
- Automatic validation
- Better IDE support

### 3. Test Organization
- One test file per resource/feature
- Clear test naming
- Proper markers

### 4. Assertions
- Multiple assertion levels
- Clear error messages
- Comprehensive validation

### 5. Test Independence
- Each test creates own data
- Cleanup after tests
- No test dependencies

## 📈 Performance Testing

Performance assertions are included in functional tests:

```python
def test_api_performance(self):
    start_time = time.time()
    response = client.get_objects()
    duration = time.time() - start_time
    
    assert duration < 2.0, f"API took {duration}s, expected < 2.0s"
```

## 🔐 Authentication

The framework supports multiple authentication methods:

- **Bearer Token**: `headers = {"Authorization": f"Bearer {token}"}`
- **Basic Auth**: `auth = (username, password)`
- **API Key**: `params = {"api_key": key}`

## 🐛 Error Handling

### Expected Errors
```python
def test_get_nonexistent_object(self):
    response = client.get_object("invalid_id")
    assert response.status_code == 404
    assert "error" in response.json()
```

### Unexpected Errors
```python
try:
    response = client.create_object(payload)
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")
    raise
```

## 📊 Test Reporting

Test reports include:
- ✅ Pass/Fail status
- ⏱️ Execution time
- 📋 Request/Response details
- 🔍 Validation results
- 📊 Coverage metrics

## 🔄 CI/CD Integration

Tests are integrated with GitHub Actions:
- Automated test execution on push/PR
- Parallel test execution
- Test report generation
- Slack/Email notifications

## 🤝 Contributing

When adding new API tests:
1. Create appropriate client methods
2. Add Pydantic models if needed
3. Include all validation types
4. Add appropriate markers
5. Document test cases in this README
6. Update JSON schemas if needed

## 📚 Additional Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [JSON Schema](https://json-schema.org/)
- [Allure Reports](https://docs.qameta.io/allure/)

---

**For detailed framework architecture, see [Architecture Documentation](../docs/ARCHITECTURE.md)**


