# Setup Guide

## Quick Start

Follow these steps to set up and run the QA Automation Framework.

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (included with Python)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Google Chrome/Firefox**: For UI testing

### Verify Prerequisites

```bash
python --version  # Should be 3.9 or higher
pip --version
git --version
```

## Installation Steps

### 1. Clone/Download the Repository

```bash
cd /path/to/your/workspace
# If from Git
git clone <repository-url>
cd qa-automation-framework

# Or if downloaded, extract and cd into the directory
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages:
- Selenium & WebDriver Manager
- Pytest & Plugins
- Requests for API testing
- Pydantic for data validation
- And more...

### 4. Configure Environment (Optional)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred settings
# (Optional - defaults work fine)
```

### 5. Verify Installation

```bash
# Check pytest is installed
pytest --version

# Run a quick test
pytest --co  # Collect tests without running
```

## Running Tests

### UI Tests

```bash
# Run all UI tests
pytest ui_tests/tests/ -v

# Run specific test
pytest ui_tests/tests/test_twitch_search.py -v

# Run in headless mode
pytest ui_tests/tests/ --headless

# Run with mobile emulation
pytest ui_tests/tests/ --mobile

# Run with Firefox
pytest ui_tests/tests/ --browser=firefox
```

### API Tests

```bash
# Run all API tests
pytest api_tests/tests/ -v

# Run specific test
pytest api_tests/tests/test_objects_crud.py -v

# Run only smoke tests
pytest api_tests/tests/ -m smoke

# Run only critical tests
pytest api_tests/tests/ -m critical
```

### Run All Tests

```bash
# Run everything
pytest -v

# Run with HTML report
pytest --html=reports/test-report.html --self-contained-html

# Run in parallel (4 workers)
pytest -n 4
```

## Generate Reports

### HTML Report

```bash
pytest --html=reports/test-report.html --self-contained-html
# Open reports/test-report.html in browser
```

### Allure Report

```bash
# Install Allure (one-time setup)
# On macOS:
brew install allure

# On Windows:
scoop install allure

# On Linux:
# Download from https://github.com/allure-framework/allure2/releases

# Run tests with Allure
pytest --alluredir=reports/allure-results

# Generate and open report
allure serve reports/allure-results
```

## Troubleshooting

### Issue: WebDriver Not Found

**Solution**: The framework uses `webdriver-manager` which auto-downloads drivers. If issues persist:

```bash
# Clear webdriver cache
rm -rf ~/.wdm

# Run tests again - drivers will be re-downloaded
pytest ui_tests/tests/
```

### Issue: Import Errors

**Solution**: Ensure virtual environment is activated

```bash
# Reactivate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Browser Not Found

**Solution**: Install the browser

- **Chrome**: [Download](https://www.google.com/chrome/)
- **Firefox**: [Download](https://www.mozilla.org/firefox/)

Or run in headless mode:
```bash
pytest ui_tests/tests/ --headless
```

### Issue: Tests Timeout

**Solution**: Increase timeout in pytest.ini or use:

```bash
pytest --timeout=600  # 10 minutes
```

### Issue: Permission Denied (Screenshots)

**Solution**: Create directories manually

```bash
mkdir -p ui_tests/reports/screenshots
mkdir -p logs
mkdir -p reports
```

## IDE Setup

### VS Code

1. Install Python extension
2. Select Python interpreter: `Cmd+Shift+P` → "Python: Select Interpreter" → Choose venv
3. Install Pytest extension
4. Configure settings.json:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["-v"],
    "python.linting.enabled": true
}
```

### PyCharm

1. Open project in PyCharm
2. File → Settings → Project → Python Interpreter
3. Add interpreter → Existing environment → Select venv/bin/python
4. Run → Edit Configurations → Add pytest configuration
5. Enable pytest in Settings → Tools → Python Integrated Tools

## Next Steps

1. **Explore Tests**: Review existing test files in `ui_tests/tests/` and `api_tests/tests/`
2. **Read Documentation**: Check out docs in `docs/` folder
3. **Run Tests**: Execute tests and view reports
4. **Customize**: Modify `config.yml` files for your needs
5. **Add Tests**: Create new tests following the examples

## Useful Commands

```bash
# List all available markers
pytest --markers

# Run tests by marker
pytest -m smoke
pytest -m "api and critical"

# Verbose output
pytest -v -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run specific test method
pytest ui_tests/tests/test_twitch_search.py::TestTwitchSearch::test_search_starcraft_and_select_streamer
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Getting Help

- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review [docs/](docs/) folder for detailed guides
- Open an issue on GitHub for bugs/questions
- Review test examples in the framework

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

**You're all set! Start testing! 🚀**


