"""
Pytest configuration and fixtures for UI tests.
OPTIMIZED for faster test execution.
"""
import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ui_tests.utils.logger import get_logger

logger = get_logger(__name__)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--mobile",
        action="store_true",
        default=False,
        help="Run tests in mobile emulation mode"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Initialize and return WebDriver instance.
    
    OPTIMIZED for faster test execution:
    - Reduced implicit wait from 10s to 3s
    - Reduced page load timeout from 30s to 10s
    - Added 'eager' page load strategy
    - Disabled image loading for speed
    - Added performance optimizations
    
    Args:
        request: Pytest request object containing config options
        
    Yields:
        WebDriver: Configured WebDriver instance
    """
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    mobile = request.config.getoption("--mobile")
    
    # Get from environment if set (useful for CI/CD)
    browser = os.getenv("BROWSER", browser)
    headless = os.getenv("HEADLESS", str(headless)).lower() == "true"
    
    logger.info(f"Initializing {browser} driver (headless={headless}, mobile={mobile})")
    
    driver = None
    
    try:
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            
            if headless:
                options.add_argument("--headless=new")
            
            # Basic stability options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-notifications")
            
            # 🚀 PERFORMANCE OPTIMIZATIONS 🚀
            
            # 1. Page Load Strategy - DON'T wait for all resources
            options.page_load_strategy = 'eager'  # ✅ CRITICAL: Loads DOM without waiting for images/CSS
            logger.info("✅ Page load strategy set to 'eager' for faster loading")
            
            # 2. Disable image loading - Huge speed boost for media-heavy sites like Twitch
            prefs = {
                "profile.managed_default_content_settings.images": 2,  # Disable images
                "profile.default_content_setting_values.notifications": 2,  # Disable notifications
                "profile.default_content_setting_values.media_stream": 2,  # Disable media stream
            }
            options.add_experimental_option("prefs", prefs)
            logger.info("✅ Image loading disabled for faster page loads")
            
            # 3. Additional performance flags
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # 4. Mobile emulation (if requested)
            if mobile:
                mobile_emulation = {
                    "deviceName": "iPhone 12 Pro"
                }
                options.add_experimental_option("mobileEmulation", mobile_emulation)
                logger.info("Mobile emulation enabled: iPhone 12 Pro")
            else:
                options.add_argument("--start-maximized")
            
            # 5. Exclude automation flags
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Initialize driver
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            
            if headless:
                options.add_argument("--headless")
            
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            # Firefox performance optimizations
            options.set_preference("permissions.default.image", 2)  # Disable images
            options.page_load_strategy = 'eager'
            
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            
        elif browser == "edge":
            options = webdriver.EdgeOptions()
            
            if headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Edge performance optimizations
            options.page_load_strategy = 'eager'
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # 🚀 AGGRESSIVE OPTIMIZATIONS 🚀
        # Reduced to 1s - Minimum viable wait for element detection
        driver.implicitly_wait(1)  # ✅ SUPER OPTIMIZED: Reduced from 10s → 3s → 1s
        logger.info("✅ Implicit wait set to 1 second (AGGRESSIVE)")
        
        # Reduced to 8s - With 'eager' strategy, most pages load within 5s
        driver.set_page_load_timeout(8)  # ✅ SUPER OPTIMIZED: Reduced from 30s → 10s → 8s
        logger.info("✅ Page load timeout set to 8 seconds (AGGRESSIVE)")
        
        # Script timeout for JavaScript execution
        driver.set_script_timeout(5)  # ✅ Prevent scripts from hanging
        logger.info("✅ Script timeout set to 5 seconds")
        
        # Maximize window if not in mobile mode
        if not mobile:
            driver.maximize_window()
        
        logger.info(f"WebDriver initialized successfully: {browser}")
        logger.info("🚀 AGGRESSIVE Performance optimizations applied:")
        logger.info("   - Page load strategy: eager")
        logger.info("   - Images disabled")
        logger.info("   - Implicit wait: 1s (was 10s) ⚡")
        logger.info("   - Page load timeout: 8s (was 30s) ⚡")
        
        yield driver
        
    except Exception as e:
        logger.error(f"Error initializing WebDriver: {str(e)}")
        raise
    finally:
        if driver:
            logger.info("Closing WebDriver")
            driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    
    Args:
        item: Test item
        call: Test call info
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = None
        
        # Get driver from fixture if available
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
        
        if driver:
            try:
                # Create screenshots directory if not exists
                screenshots_dir = os.path.join(
                    os.path.dirname(__file__),
                    "reports",
                    "screenshots"
                )
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.nodeid.replace("::", "_").replace("/", "_")
                filename = f"{test_name}_{timestamp}.png"
                filepath = os.path.join(screenshots_dir, filename)
                
                # Take screenshot
                driver.save_screenshot(filepath)
                logger.info(f"Screenshot saved: {filepath}")
                
                # Attach to allure report if available
                try:
                    import allure
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"failure_{timestamp}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass
                    
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")


@pytest.fixture(scope="session")
def screenshots_dir():
    """Create and return screenshots directory path."""
    screenshots_path = os.path.join(
        os.path.dirname(__file__),
        "reports",
        "screenshots"
    )
    os.makedirs(screenshots_path, exist_ok=True)
    return screenshots_path


@pytest.fixture(scope="session")
def test_data_dir():
    """Return test data directory path."""
    return os.path.join(os.path.dirname(__file__), "test_data")


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
