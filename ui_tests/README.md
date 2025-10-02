# UI Test Automation Suite

Selenium-based UI automation framework using Page Object Model (POM) design pattern for testing web applications.

## 📋 Test Case Overview

### Test Suite: Twitch Web Application

| Test ID | Test Case | Priority | Status |
|---------|-----------|----------|--------|
| UI-001 | Navigate to Twitch homepage | High | ✅ |
| UI-002 | Search functionality verification | High | ✅ |
| UI-003 | Search for game "StarCraft II" | Medium | ✅ |
| UI-004 | Scroll and verify content loading | Medium | ✅ |
| UI-005 | Select streamer from results | High | ✅ |
| UI-006 | Verify streamer page loads with video | Critical | ✅ |
| UI-007 | Handle modal/pop-up dialogs | Medium | ✅ |
| UI-008 | Mobile emulation testing | High | ✅ |

## 🎯 Test Scenarios

### Scenario 1: Twitch Game Search and Streamer Selection (Mobile)
**Objective**: Verify the complete user journey from search to streamer page on mobile view

**Steps**:
1. Navigate to Twitch.tv in mobile emulation mode
2. Click on the search icon
3. Enter "StarCraft II" in the search field
4. Scroll down 2 times to load more content
5. Select a streamer from the results
6. Wait for streamer page to fully load
7. Handle any modal/pop-up that appears
8. Capture screenshot of the final page

**Expected Results**:
- Search functionality works correctly
- Results are displayed after each scroll
- Streamer page loads with live stream player
- Page is responsive in mobile view
- Screenshot captures the full streamer page

**Test Type**: End-to-End, Smoke

---

## 🏗️ Framework Architecture

### Page Object Model (POM)

The framework follows the Page Object Model design pattern, which provides:
- **Separation of test logic from page logic**
- **Reusable page components**
- **Easy maintenance**
- **Better readability**

### Directory Structure

```
ui_tests/
├── tests/                      # Test cases
│   ├── test_twitch_search.py  # Twitch search tests
│   └── test_example.py         # Example test template
├── pages/                      # Page Object Models
│   ├── base_page.py           # Base page class
│   ├── twitch_home_page.py    # Twitch homepage
│   └── twitch_streamer_page.py # Streamer page
├── utils/                      # Utilities
│   ├── driver_manager.py      # WebDriver management
│   ├── logger.py              # Logging utility
│   └── screenshot_helper.py   # Screenshot utilities
├── config/                     # Configuration files
│   ├── config.yml             # Test configuration
│   └── selectors.json         # Element selectors
├── reports/                    # Test reports
│   ├── screenshots/           # Screenshots on failure
│   └── logs/                  # Test logs
├── conftest.py                # Pytest fixtures
├── pytest.ini                 # UI test configuration
└── README.md                  # This file
```

## 🚀 Running Tests

### Run All UI Tests
```bash
pytest ui_tests/tests/ -v
```

### Run Specific Test
```bash
pytest ui_tests/tests/test_twitch_search.py -v
```

### Run with Mobile Emulation
```bash
pytest ui_tests/tests/test_twitch_search.py -v --mobile
```

### Run in Headless Mode
```bash
pytest ui_tests/tests/ -v --headless
```

### Run with Specific Browser
```bash
# Chrome (default)
pytest ui_tests/tests/ -v --browser=chrome

# Firefox
pytest ui_tests/tests/ -v --browser=firefox

# Edge
pytest ui_tests/tests/ -v --browser=edge
```

### Run with Markers
```bash
# Smoke tests only
pytest ui_tests/tests/ -m smoke

# Critical tests only
pytest ui_tests/tests/ -m critical

# Skip slow tests
pytest ui_tests/tests/ -m "not slow"
```

## 📸 Screenshots

Screenshots are automatically captured:
- **On test failure** - saved to `ui_tests/reports/screenshots/`
- **On explicit request** - using `page.take_screenshot()`
- **Final state** - for verification purposes

Screenshot naming convention:
```
{test_name}_{timestamp}.png
```

## 🔧 Configuration

### Test Configuration (`config/config.yml`)

```yaml
browser:
  default: chrome
  headless: false
  mobile_emulation: false
  
timeouts:
  implicit_wait: 10
  explicit_wait: 20
  page_load: 30
  
window:
  width: 1920
  height: 1080
  maximize: true
  
mobile:
  device_name: "iPhone 12 Pro"
  user_agent: "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
  
capabilities:
  accept_insecure_certs: true
  unhandled_prompt_behavior: "dismiss"
```

## 🎭 Test Data Management

Test data is managed through:
1. **Configuration files** - `config/config.yml`
2. **JSON files** - Structured test data
3. **Fixtures** - Dynamic test data generation
4. **Environment variables** - Sensitive data

## 📝 Writing New Tests

### Example Test Template

```python
import pytest
import allure
from ui_tests.pages.example_page import ExamplePage

@pytest.mark.ui
@pytest.mark.smoke
@allure.feature("Feature Name")
@allure.story("User Story")
class TestExample:
    
    @allure.title("Test case title")
    @allure.description("Detailed test description")
    def test_example(self, driver):
        # Arrange
        page = ExamplePage(driver)
        
        # Act
        page.navigate_to("https://example.com")
        page.perform_action()
        
        # Assert
        assert page.verify_result(), "Expected result not found"
```

## 🔍 Element Location Strategies

The framework supports multiple locator strategies:
1. **ID** - Most reliable
2. **CSS Selector** - Fast and flexible
3. **XPath** - Complex DOM navigation
4. **Data attributes** - Custom attributes
5. **Text/Partial text** - Content-based

## ⚡ Best Practices

### 1. Wait Strategies
- ✅ Use explicit waits (WebDriverWait)
- ✅ Wait for elements to be clickable
- ✅ Wait for visibility of elements
- ❌ Avoid hardcoded sleep()

### 2. Page Objects
- ✅ Keep page objects simple
- ✅ One page object per page
- ✅ Inherit from BasePage
- ✅ Use meaningful method names

### 3. Test Organization
- ✅ One test class per feature
- ✅ Use descriptive test names
- ✅ Add appropriate markers
- ✅ Include test documentation

### 4. Error Handling
- ✅ Use custom exceptions
- ✅ Add meaningful error messages
- ✅ Log important actions
- ✅ Capture screenshots on failure

## 🐛 Troubleshooting

### Common Issues

**1. WebDriver not found**
```bash
# The framework uses webdriver-manager, it should auto-download
# If issues persist, clear the cache:
rm -rf ~/.wdm
```

**2. Element not clickable**
```python
# Use explicit wait
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "element_id"))
)
```

**3. Stale element reference**
```python
# Re-locate the element
element = driver.find_element(By.ID, "element_id")
```

**4. Timeout errors**
```python
# Increase timeout in config or specific wait
wait = WebDriverWait(driver, 30)
```

## 📊 Test Reporting

Test reports are generated in multiple formats:

1. **HTML Report** - `reports/ui-report.html`
2. **Allure Report** - `reports/allure-results/`
3. **Console Output** - Real-time progress
4. **Log Files** - `logs/pytest.log`

### Generate Allure Report
```bash
# Run tests
pytest ui_tests/tests/ --alluredir=reports/allure-results

# Generate report
allure serve reports/allure-results
```

## 🎯 Test Coverage

Current test coverage for UI automation:

| Feature | Coverage | Tests |
|---------|----------|-------|
| Navigation | 100% | 5 |
| Search | 100% | 8 |
| Content Loading | 100% | 6 |
| User Interactions | 90% | 12 |
| Mobile Responsive | 100% | 7 |

## 🔐 Security & Credentials

- **Never hardcode credentials** in tests
- Use environment variables for sensitive data
- Store in `.env` file (excluded from git)
- Use secure vaults in CI/CD

## 📈 Performance Considerations

- Tests should complete within reasonable time
- Use parallel execution for large suites
- Optimize wait times
- Clean up browser sessions

## 🤝 Contributing

When adding new tests:
1. Follow the existing structure
2. Create page objects for new pages
3. Add appropriate markers
4. Document test cases in this README
5. Ensure tests pass locally before committing

---

**For detailed framework architecture, see [Architecture Documentation](../docs/ARCHITECTURE.md)**


