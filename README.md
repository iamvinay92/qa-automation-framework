# 🚀 QA Automation Framework

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.4.2-green.svg)](https://pytest.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-orange.svg)](https://www.selenium.dev/)

Comprehensive test automation framework for UI and API testing using **Pytest** with Selenium WebDriver and Requests library. Optimized for speed, reliability, and maintainability.

## 🎥 Demo

![Test Execution Demo](demo.gif)

*UI test running locally - Complete Twitch search flow (67 seconds)*

## 📋 Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Reports](#test-reports)
- [Performance](#performance)

## ✨ Features

- ✅ **UI Automation** - Selenium WebDriver with Page Object Model
- ✅ **API Automation** - RESTful API testing with Requests
- ✅ **Pytest Framework** - Industry-standard test runner
- ✅ **Allure Reports** - Beautiful test reports with screenshots
- ✅ **Parallel Execution** - Fast test execution
- ✅ **CI/CD Ready** - GitHub Actions compatible
- ✅ **Optimized Performance** - 52% faster execution (140s → 67s)
- ✅ **Page Object Model** - Maintainable UI test architecture
- ✅ **Data-Driven Testing** - Parameterized tests
- ✅ **Comprehensive Logging** - Detailed test execution logs

## 🛠️ Technologies

| Category | Technology |
|----------|-----------|
| Language | Python 3.13 |
| Test Framework | Pytest 8.4.2 |
| UI Automation | Selenium WebDriver 4.x |
| API Testing | Requests 2.32.3 |
| Reports | Allure, HTML |
| Assertions | Pytest assertions |
| Data Validation | Pydantic |
| Browser Management | WebDriver Manager |

## 📁 Project Structure

```
qa-automation-framework/
│
├── api_tests/                      # API Testing Suite
│   ├── api_clients/                # API client implementations
│   │   ├── base_client.py          # Base HTTP client
│   │   ├── ipstack_client.py       # IPStack API client
│   │   └── objects_client.py       # Objects API client
│   ├── config/
│   │   └── config.yml              # API configuration
│   ├── models/                     # Pydantic data models
│   │   ├── ipstack_model.py
│   │   └── object_model.py
│   ├── tests/                      # API test cases
│   │   ├── test_ipstack_geolocation.py
│   │   └── test_objects_crud.py
│   ├── utils/                      # Helper utilities
│   │   ├── api_helper.py
│   │   └── logger.py
│   ├── conftest.py                 # Pytest fixtures
│   └── pytest.ini                  # Pytest configuration
│
├── ui_tests/                       # UI Testing Suite
│   ├── pages/                      # Page Object Model
│   │   ├── base_page.py            # Base page class
│   │   ├── twitch_home_page.py     # Twitch homepage
│   │   └── twitch_streamer_page.py # Streamer page
│   ├── config/
│   │   └── config.yml              # UI configuration
│   ├── tests/                      # UI test cases
│   │   └── test_twitch_search.py   # Twitch search tests
│   ├── utils/                      # Helper utilities
│   │   ├── logger.py
│   │   └── screenshot_helper.py
│   ├── conftest.py                 # Pytest fixtures
│   └── pytest.ini                  # Pytest configuration
│
├── shared/                         # Shared utilities
│   ├── config/
│   └── utils/
│       ├── common_logger.py
│       └── data_generator.py
│
├── reports/                        # Test reports
│   └── screenshots/                # Test screenshots
│
├── logs/                           # Execution logs
│
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Root pytest config
└── README.md                       # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.13+
- Chrome browser (for UI tests)
- pip (Python package manager)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/qa-automation-framework.git
cd qa-automation-framework
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run API Tests Only
```bash
pytest api_tests/ -v
```

### Run UI Tests Only
```bash
pytest ui_tests/ -v --browser=chrome
```

### Run Specific Test
```bash
pytest ui_tests/tests/test_twitch_search.py::TestTwitchSearch::test_search_starcraft_and_select_streamer -v
```

### Run Tests with Allure Report
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Run Tests in Parallel
```bash
pytest -n auto
```

### Run Smoke Tests Only
```bash
pytest -m smoke
```

## 📊 Test Reports

After test execution, reports are generated in multiple formats:

- **HTML Report:** `reports/test-report.html`
- **Allure Report:** `reports/allure-results/`
- **Screenshots:** `reports/screenshots/`
- **Logs:** `logs/pytest.log`

## ⚡ Performance

### Optimization Results:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| UI Test Execution | 140s | 67s | **52% faster** |
| Implicit Wait | 10s | 1s | **90% reduction** |
| Page Load Timeout | 30s | 8s | **73% reduction** |

### Key Optimizations:
- ✅ Aggressive timeout reduction
- ✅ 'eager' page load strategy
- ✅ Disabled image loading
- ✅ Optimized explicit waits
- ✅ Reduced sleep times
- ✅ Parallel execution support

## 🎯 Test Coverage

### UI Tests (Selenium)
- ✅ Search functionality
- ✅ Navigation flows
- ✅ Element interactions
- ✅ Screenshot capture
- ✅ Modal handling
- ✅ Dynamic content loading

### API Tests (Requests)
- ✅ CRUD operations
- ✅ Response validation
- ✅ Status code checks
- ✅ Performance testing
- ✅ Error handling
- ✅ Data model validation

## 📝 Test Examples

### UI Test Example
```python
def test_search_starcraft_and_select_streamer(self, driver):
    home_page = TwitchHomePage(driver)
    home_page.open()
    home_page.search_for("StarCraft II")
    home_page.scroll_down(times=2)
    home_page.click_first_streamer()
    
    streamer_page = TwitchStreamerPage(driver)
    streamer_page.wait_for_page_to_load()
    assert streamer_page.is_page_loaded_successfully()
```

### API Test Example
```python
def test_lookup_specific_ip(self, ipstack_client):
    response = ipstack_client.lookup_ip("134.201.250.155")
    assert response.status_code == 200
    assert response.json()['country_code'] == 'US'
```

## 🔧 Configuration

### API Configuration (`api_tests/config/config.yml`)
```yaml
api:
  base_url: "https://api.restful-api.dev"
  timeout: 30

ipstack:
  base_url: "https://api.ipstack.com"
  access_key: "YOUR_KEY"
```

### UI Configuration (`ui_tests/config/config.yml`)
```yaml
urls:
  twitch: "https://www.twitch.tv"

browser:
  default: chrome
  headless: false

timeouts:
  implicit_wait: 1
  page_load: 8
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Vinay Rathod

## 📧 Contact

For questions or feedback, please reach out via email or GitHub issues.

---

**Happy Testing! 🚀**
