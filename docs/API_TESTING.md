# API Testing Guide

## Overview

This document provides comprehensive information about the API test automation framework, including implementation patterns, validation strategies, and best practices.

## Framework Components

### 1. API Client Architecture

#### BaseAPIClient

Foundation class for all API clients:

```python
class BaseAPIClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = base_url
        self.session = self._create_session()
    
    def get(self, endpoint, params=None):
        return self.session.get(url, params=params, timeout=self.timeout)
    
    def post(self, endpoint, json=None):
        return self.session.post(url, json=json, timeout=self.timeout)
```

**Features**:
- Session management with connection pooling
- Automatic retry on failure
- Request/Response logging
- Timeout configuration

#### Creating Custom Clients

```python
from api_tests.api_clients.base_client import BaseAPIClient

class UsersClient(BaseAPIClient):
    def create_user(self, user_data):
        return self.post("/users", json=user_data)
    
    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")
```

### 2. Request/Response Models

#### Using Pydantic Models

```python
from pydantic import BaseModel, validator

class UserRequest(BaseModel):
    name: str
    email: str
    age: int
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: str
```

**Benefits**:
- Automatic validation
- Type safety
- IDE autocomplete
- Clear data contracts

### 3. Validation Strategies

#### 1. Status Code Validation

```python
def test_create_user(client):
    response = client.create_user(user_data)
    assert response.status_code == 201
```

#### 2. Response Body Validation

```python
def test_user_response_structure(client):
    response = client.get_user("123")
    data = response.json()
    
    assert 'id' in data
    assert 'name' in data
    assert data['email'].endswith('@example.com')
```

#### 3. JSON Schema Validation

```python
from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["id", "name", "email"]
}

def test_schema_validation(client):
    response = client.get_user("123")
    validate(instance=response.json(), schema=user_schema)
```

#### 4. Pydantic Model Validation

```python
def test_pydantic_validation(client):
    response = client.get_user("123")
    user = UserResponse(**response.json())
    assert user.name == "John Doe"
```

#### 5. Response Time Validation

```python
def test_response_time(client):
    response = client.get_users()
    assert response.elapsed.total_seconds() < 2.0
```

### 4. Test Organization

#### CRUD Test Pattern

```python
@pytest.mark.api
@pytest.mark.crud
class TestUsersCRUD:
    
    def test_create_user(self, users_client):
        """POST /users - Create"""
        response = users_client.create_user(user_data)
        assert response.status_code == 201
    
    def test_get_user(self, users_client, test_user_id):
        """GET /users/{id} - Read"""
        response = users_client.get_user(test_user_id)
        assert response.status_code == 200
    
    def test_update_user(self, users_client, test_user_id):
        """PUT /users/{id} - Update"""
        response = users_client.update_user(test_user_id, updated_data)
        assert response.status_code == 200
    
    def test_delete_user(self, users_client, test_user_id):
        """DELETE /users/{id} - Delete"""
        response = users_client.delete_user(test_user_id)
        assert response.status_code == 204
```

#### Negative Test Pattern

```python
@pytest.mark.api
@pytest.mark.negative
class TestUsersNegative:
    
    def test_get_nonexistent_user(self, users_client):
        response = users_client.get_user("invalid_id")
        assert response.status_code == 404
    
    def test_create_user_invalid_email(self, users_client):
        invalid_data = {"name": "John", "email": "invalid"}
        response = users_client.create_user(invalid_data)
        assert response.status_code == 400
    
    def test_unauthorized_access(self, users_client):
        # Remove auth token
        response = users_client.get_user("123", headers={})
        assert response.status_code == 401
```

### 5. Data-Driven Testing

#### Using Parametrize

```python
@pytest.mark.parametrize("name,email,expected_status", [
    ("John Doe", "john@example.com", 201),
    ("Jane Smith", "jane@example.com", 201),
    ("", "test@example.com", 400),  # Empty name
    ("Test User", "invalid", 400),  # Invalid email
])
def test_create_user_variations(client, name, email, expected_status):
    data = {"name": name, "email": email}
    response = client.create_user(data)
    assert response.status_code == expected_status
```

#### Using Test Data Files

```python
import json

def load_test_data():
    with open('test_data/users.json') as f:
        return json.load(f)

@pytest.mark.parametrize("user_data", load_test_data())
def test_create_multiple_users(client, user_data):
    response = client.create_user(user_data)
    assert response.status_code == 201
```

### 6. Authentication Handling

#### Bearer Token

```python
class AuthenticatedClient(BaseAPIClient):
    def __init__(self, base_url, token):
        super().__init__(base_url)
        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
```

#### Basic Auth

```python
def test_with_basic_auth(base_url):
    response = requests.get(
        f"{base_url}/users",
        auth=("username", "password")
    )
    assert response.status_code == 200
```

#### API Key

```python
def test_with_api_key(base_url):
    headers = {"X-API-Key": "your_api_key"}
    response = requests.get(f"{base_url}/users", headers=headers)
    assert response.status_code == 200
```

### 7. Test Fixtures

#### Session-Scoped Fixtures

```python
@pytest.fixture(scope="session")
def api_config():
    return load_config("config.yml")

@pytest.fixture(scope="session")
def base_url(api_config):
    return api_config['api']['base_url']
```

#### Function-Scoped Fixtures

```python
@pytest.fixture(scope="function")
def test_user(users_client):
    # Setup: Create test user
    response = users_client.create_user(test_data)
    user_id = response.json()['id']
    
    yield user_id
    
    # Teardown: Delete test user
    users_client.delete_user(user_id)
```

### 8. Performance Testing

#### Response Time Assertions

```python
def test_api_performance(client):
    import time
    
    start = time.time()
    response = client.get_users()
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 2.0, f"Request took {duration}s"
```

#### Concurrent Requests

```python
import concurrent.futures

def test_concurrent_requests(client):
    def make_request():
        return client.get_users()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in futures]
    
    # All requests should succeed
    assert all(r.status_code == 200 for r in results)
```

### 9. Error Handling

#### Expected Errors

```python
def test_expected_error(client):
    response = client.get_user("nonexistent")
    
    assert response.status_code == 404
    assert "error" in response.json()
    assert "not found" in response.json()['error'].lower()
```

#### Retry Mechanism

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retry():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
```

### 10. Best Practices

#### ✅ Do's

1. **Use client abstraction**: Don't call requests directly in tests
2. **Validate multiple aspects**: Status, body, headers, time
3. **Test both positive and negative scenarios**
4. **Use appropriate fixtures**: Setup and cleanup test data
5. **Keep tests independent**: Each test should work standalone
6. **Use meaningful assertions**: Clear error messages
7. **Log requests/responses**: For debugging
8. **Parametrize similar tests**: Reduce duplication
9. **Handle authentication properly**: Use fixtures
10. **Version your APIs**: Test against specific versions

#### ❌ Don'ts

1. **Don't test third-party APIs directly**: Mock or use test environments
2. **Don't hardcode URLs**: Use configuration
3. **Don't skip cleanup**: Clean up test data
4. **Don't test UI through API**: Keep concerns separated
5. **Don't ignore response times**: Performance matters
6. **Don't use production data**: Use test data
7. **Don't share test data**: Tests should be independent
8. **Don't skip negative tests**: Test error handling
9. **Don't ignore status codes**: Always verify
10. **Don't skip schema validation**: Validate structure

### 11. Common Patterns

#### Chaining API Calls

```python
def test_user_workflow(users_client, posts_client):
    # Create user
    user_response = users_client.create_user(user_data)
    user_id = user_response.json()['id']
    
    # Create post for user
    post_data = {"user_id": user_id, "content": "Hello"}
    post_response = posts_client.create_post(post_data)
    
    # Verify
    assert post_response.status_code == 201
    assert post_response.json()['user_id'] == user_id
```

#### Polling for Status

```python
import time

def wait_for_job_completion(client, job_id, timeout=60):
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        response = client.get_job(job_id)
        status = response.json()['status']
        
        if status == 'completed':
            return True
        elif status == 'failed':
            return False
        
        time.sleep(2)
    
    raise TimeoutError(f"Job {job_id} did not complete")
```

### 12. Running Tests

```bash
# All API tests
pytest api_tests/tests/

# Specific test file
pytest api_tests/tests/test_objects_crud.py

# With markers
pytest -m "api and smoke"

# Parallel execution
pytest -n 4

# Generate report
pytest --html=reports/api-report.html

# Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### 13. Debugging Tips

1. **Print request/response**:
   ```python
   print(f"Request: {response.request.method} {response.request.url}")
   print(f"Response: {response.status_code} - {response.text}")
   ```

2. **Use pytest -s**: See print output

3. **Check response details**:
   ```python
   print(f"Headers: {response.headers}")
   print(f"Time: {response.elapsed.total_seconds()}s")
   ```

4. **Validate JSON manually**:
   ```python
   import json
   print(json.dumps(response.json(), indent=2))
   ```

5. **Use curl equivalent**:
   ```python
   from curlify import to_curl
   print(to_curl(response.request))
   ```

---

For more information, see the [Architecture Documentation](ARCHITECTURE.md).


