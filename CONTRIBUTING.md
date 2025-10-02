# Contributing to QA Automation Framework

Thank you for your interest in contributing to the QA Automation Framework! This document provides guidelines and best practices for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix
4. Make your changes
5. Run tests to ensure everything works
6. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone <your-fork-url>
cd qa-automation-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install black flake8 isort pylint
```

## Code Style Guidelines

### Python Style Guide
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where applicable
- Write docstrings for all functions and classes

### Example:

```python
def create_object(self, data: Dict[str, Any]) -> requests.Response:
    """
    Create a new object.
    
    Args:
        data: Object data as dictionary
        
    Returns:
        requests.Response: API response object
    """
    return self.post("/objects", json=data)
```

### Formatting Tools

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Static analysis with pylint
pylint ui_tests api_tests shared
```

## Writing Tests

### Test Structure
- Follow AAA pattern (Arrange, Act, Assert)
- One assertion per test (when possible)
- Clear and descriptive test names
- Add appropriate markers
- Include allure decorations

### Example:

```python
@pytest.mark.api
@pytest.mark.smoke
@allure.feature("Objects API")
@allure.story("CRUD Operations")
def test_create_object(self, objects_client, sample_data):
    """Test creating a new object with valid data."""
    # Arrange
    payload = sample_data
    
    # Act
    response = objects_client.create_object(payload)
    
    # Assert
    assert response.status_code == 200
    assert response.json()['name'] == payload['name']
```

### Test Naming Convention

- Test functions: `test_<action>_<expected_result>`
- Test classes: `Test<Feature><Action>`
- Test files: `test_<feature>.py`

Examples:
- `test_create_object_with_valid_data`
- `test_get_object_returns_404_when_not_found`
- `TestObjectsCRUD`
- `test_objects_crud.py`

## Adding New Features

### Adding UI Tests

1. Create page object in `ui_tests/pages/`
2. Extend `BasePage`
3. Define locators as class variables
4. Implement page methods
5. Create test file in `ui_tests/tests/`
6. Update README with test cases

### Adding API Tests

1. Create API client in `api_tests/api_clients/`
2. Extend `BaseAPIClient`
3. Create Pydantic models in `api_tests/models/`
4. Create test file in `api_tests/tests/`
5. Add test data in `api_tests/test_data/`
6. Update README with API documentation

## Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(api): Add user authentication tests

- Implement login/logout test cases
- Add token refresh validation
- Include negative scenarios

Closes #123
```

```
fix(ui): Fix stale element exception in search

- Add explicit wait before clicking
- Retry mechanism for stale elements
- Update locator strategy

Fixes #456
```

## Pull Request Process

1. **Update Documentation**: Ensure README and docs are updated
2. **Run Tests**: All tests must pass
3. **Code Review**: Request review from maintainers
4. **Address Feedback**: Make requested changes
5. **Merge**: Maintainer will merge when approved

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, browser)

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Proposed solution
- Alternative solutions considered

## Code Review Guidelines

### For Reviewers

- Be respectful and constructive
- Focus on code quality and best practices
- Provide specific feedback
- Approve when satisfied

### For Contributors

- Respond to feedback promptly
- Ask questions if unclear
- Make requested changes
- Update PR description if scope changes

## Testing Guidelines

### Before Submitting PR

```bash
# Run all tests
pytest

# Run specific test suite
pytest ui_tests/tests/
pytest api_tests/tests/

# Run with coverage
pytest --cov=. --cov-report=html

# Check code style
black --check .
flake8 .
```

### CI/CD

All PRs automatically trigger:
- Test execution on multiple Python versions
- Code style checks
- Test coverage report
- Security scanning

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Adding configuration options
- Updating dependencies

### Documentation Locations

- `README.md`: Project overview and quick start
- `docs/ARCHITECTURE.md`: Framework architecture
- `docs/UI_TESTING.md`: UI testing guide
- `docs/API_TESTING.md`: API testing guide
- Code docstrings: Function/class documentation

## Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the QA Automation Framework! 🎉


