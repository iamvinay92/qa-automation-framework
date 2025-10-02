"""
Screenshot utility for capturing page screenshots.
"""
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from ui_tests.utils.logger import get_logger

logger = get_logger(__name__)


class ScreenshotHelper:
    """Helper class for taking and managing screenshots."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize ScreenshotHelper.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.screenshots_dir = Path(__file__).parent.parent / "reports" / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Capture and save a screenshot.
        
        Args:
            name: Base name for the screenshot file
            
        Returns:
            str: Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            raise
    
    def take_element_screenshot(self, element, name: str = "element") -> str:
        """
        Capture screenshot of a specific element.
        
        Args:
            element: WebElement to capture
            name: Base name for the screenshot file
            
        Returns:
            str: Path to the saved screenshot
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            
            element.screenshot(str(filepath))
            logger.info(f"Element screenshot saved: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {str(e)}")
            raise


