# UI Testing Guide

## Overview

This document provides detailed information about the UI test automation framework, including implementation details, best practices, and troubleshooting guidelines.

## Framework Components

### 1. WebDriver Management

The framework uses `webdriver-manager` for automatic driver management:

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

**Benefits**:
- No manual driver downloads
- Automatic version matching
- Cross-platform compatibility

### 2. Page Object Model (POM)

#### BasePage

All page objects inherit from `BasePage`:

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
```

**Common Methods**:
- `find_element()`: Locate element with explicit wait
- `click()`: Click with wait for clickability
- `type_text()`: Type into input field
- `scroll_to_element()`: Scroll element into view
- `is_element_visible()`: Check element visibility

#### Creating New Page Objects

```python
from selenium.webdriver.common.by import By
from ui_tests.pages.base_page import BasePage

class NewPage(BasePage):
    # Locators
    LOGIN_BUTTON = (By.ID, "login-btn")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com"
    
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
```

### 3. Locator Strategies

**Priority Order** (Most to Least Reliable):

1. **ID**: `(By.ID, "element-id")`
2. **Data Attributes**: `(By.CSS_SELECTOR, "[data-testid='element']")`
3. **CSS Selector**: `(By.CSS_SELECTOR, ".class-name")`
4. **XPath**: `(By.XPATH, "//div[@class='example']")`

**Best Practices**:
```python
# ✅ Good - Specific and stable
SUBMIT_BUTTON = (By.ID, "submit-btn")
SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-testid='search']")

# ❌ Bad - Fragile and non-specific
BUTTON = (By.XPATH, "//body/div[1]/div[2]/button")
ELEMENT = (By.CSS_SELECTOR, "div > div > span")
```

### 4. Wait Strategies

#### Explicit Waits (Recommended)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for element to be clickable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "button"))
)

# Wait for visibility
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal"))
)
```

#### Common Expected Conditions:

- `presence_of_element_located`: Element exists in DOM
- `visibility_of_element_located`: Element is visible
- `element_to_be_clickable`: Element is clickable
- `text_to_be_present_in_element`: Specific text present
- `staleness_of`: Element is no longer in DOM

### 5. Browser Configuration

#### Chrome Options

```python
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# Mobile emulation
mobile_emulation = {"deviceName": "iPhone 12 Pro"}
options.add_experimental_option("mobileEmulation", mobile_emulation)
```

#### Cross-Browser Support

Run tests on different browsers:

```bash
# Chrome
pytest --browser=chrome

# Firefox
pytest --browser=firefox

# Edge
pytest --browser=edge
```

### 6. Test Organization

#### Test Structure

```python
@pytest.mark.ui
@pytest.mark.smoke
@allure.feature("Login")
@allure.story("User Authentication")
class TestLogin:
    
    @allure.title("Successful login with valid credentials")
    @allure.description("Verify user can login with valid username and password")
    def test_valid_login(self, driver):
        # Arrange
        login_page = LoginPage(driver)
        
        # Act
        login_page.open()
        login_page.login("user@example.com", "password123")
        
        # Assert
        assert login_page.is_login_successful()
```

#### Test Markers

```python
@pytest.mark.smoke      # Quick sanity tests
@pytest.mark.regression # Full regression suite
@pytest.mark.critical   # Critical path tests
@pytest.mark.slow       # Long-running tests
@pytest.mark.mobile     # Mobile-specific tests
```

### 7. Screenshot Management

Screenshots are automatically captured on test failures:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Captures screenshot on failure
    if report.failed and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        driver.save_screenshot(f"failure_{timestamp}.png")
```

Manual screenshots:

```python
page.take_screenshot("custom_screenshot_name")
```

### 8. Handling Dynamic Content

#### Waiting for AJAX

```python
def wait_for_ajax(driver, timeout=30):
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script("return jQuery.active == 0"))
```

#### Handling Modals/Popups

```python
def close_modal_if_present(self):
    try:
        close_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-close"))
        )
        close_button.click()
        return True
    except TimeoutException:
        return False
```

### 9. Mobile Testing

#### Mobile Emulation

```python
mobile_emulation = {
    "deviceName": "iPhone 12 Pro"
}
options.add_experimental_option("mobileEmulation", mobile_emulation)

# Or custom metrics
mobile_emulation = {
    "deviceMetrics": {
        "width": 390,
        "height": 844,
        "pixelRatio": 3.0
    }
}
```

#### Running Mobile Tests

```bash
pytest ui_tests/tests/ --mobile -v
```

### 10. Best Practices

#### ✅ Do's

1. **Use explicit waits**: Always prefer explicit waits over sleep()
2. **Create reusable page objects**: One page = one class
3. **Use meaningful names**: Clear test and method names
4. **Add appropriate assertions**: Test one thing at a time
5. **Handle dynamic content**: Wait for AJAX and animations
6. **Take screenshots on failures**: Automatic debugging aid
7. **Use proper locators**: ID > CSS > XPath
8. **Keep tests independent**: Each test should run standalone
9. **Add test documentation**: Use allure decorators
10. **Clean up after tests**: Fixtures handle teardown

#### ❌ Don'ts

1. **Don't use time.sleep()**: Use explicit waits instead
2. **Don't hardcode test data**: Use fixtures or data files
3. **Don't create test dependencies**: Tests should be independent
4. **Don't use brittle locators**: Avoid complex XPath
5. **Don't skip error handling**: Handle expected exceptions
6. **Don't test implementation**: Test user behavior
7. **Don't share state**: Each test should be isolated
8. **Don't ignore flaky tests**: Investigate and fix
9. **Don't skip logging**: Log important actions
10. **Don't mix test logic with page logic**: Maintain separation

### 11. Troubleshooting

#### Common Issues

**Element Not Clickable**
```python
# Solution 1: Wait for element to be clickable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(locator)
)

# Solution 2: Scroll into view
driver.execute_script("arguments[0].scrollIntoView();", element)

# Solution 3: Use JavaScript click
driver.execute_script("arguments[0].click();", element)
```

**Stale Element Reference**
```python
# Solution: Re-locate the element
def safe_click(driver, locator):
    for _ in range(3):
        try:
            element = driver.find_element(*locator)
            element.click()
            break
        except StaleElementReferenceException:
            time.sleep(0.5)
```

**TimeoutException**
```python
# Solution: Increase timeout or check locator
wait = WebDriverWait(driver, 30)  # Increase timeout
element = wait.until(EC.presence_of_element_located(locator))
```

### 12. Running Tests

```bash
# All UI tests
pytest ui_tests/tests/

# Specific test file
pytest ui_tests/tests/test_twitch_search.py

# Specific test
pytest ui_tests/tests/test_twitch_search.py::TestTwitchSearch::test_search_starcraft_and_select_streamer

# With markers
pytest -m smoke
pytest -m "smoke and not slow"

# Parallel execution
pytest -n 4

# Generate report
pytest --html=reports/ui-report.html --self-contained-html

# Headless mode
pytest --headless
```

### 13. Debugging Tips

1. **Use --pdb flag**: Drop into debugger on failure
   ```bash
   pytest --pdb
   ```

2. **Use -s flag**: See print statements
   ```bash
   pytest -s
   ```

3. **Increase logging**: Set log level to DEBUG
   ```python
   logger.setLevel(logging.DEBUG)
   ```

4. **Take screenshots**: Capture current state
   ```python
   driver.save_screenshot("debug.png")
   ```

5. **Check element state**: Verify element properties
   ```python
   print(f"Displayed: {element.is_displayed()}")
   print(f"Enabled: {element.is_enabled()}")
   print(f"Location: {element.location}")
   ```

---

For more information, see the [Architecture Documentation](ARCHITECTURE.md).


