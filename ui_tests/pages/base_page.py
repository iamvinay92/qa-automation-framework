"""
Base page class with common methods for all page objects.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, List
from ui_tests.utils.logger import get_logger
from ui_tests.utils.screenshot_helper import ScreenshotHelper

logger = get_logger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize BasePage.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)  # ⚡ AGGRESSIVE: Reduced from 20s to 5s
        self.screenshot_helper = ScreenshotHelper(driver)
        self.actions = ActionChains(driver)
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Find an element.
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            WebElement: Found element
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            List[WebElement]: List of found elements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click an element.
        
        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to type
            clear_first: Whether to clear the field first
        """
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Typed text into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to type text into element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            str: Element text
        """
        try:
            element = self.find_element(locator)
            text = element.text
            logger.debug(f"Got text from element {locator}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 10) -> bool:
        """
        Check if an element is visible.
        
        Args:
            locator: Tuple of (By, value)
            timeout: Timeout in seconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element is not visible: {locator}")
            return False
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is present in DOM.
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Scroll to an element.
        
        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def scroll_by_pixels(self, pixels: int) -> None:
        """
        Scroll page by pixels.
        Attempts to scroll the appropriate container (for sites like Twitch) or window.
        
        Args:
            pixels: Number of pixels to scroll (positive for down, negative for up)
        """
        try:
            # Strategy: Use JavaScript to find ALL scrollable elements and scroll them
            scroll_script = f"""
            var scrolled = false;
            var pixels = {pixels};
            
            // Try to find scrollable element by checking overflow and scrollHeight
            function isScrollable(element) {{
                var style = window.getComputedStyle(element);
                var overflowY = style.overflowY;
                return (overflowY === 'scroll' || overflowY === 'auto') && 
                       element.scrollHeight > element.clientHeight;
            }}
            
            // Check specific selectors first
            var selectors = ['main[role="main"]', 'div[data-a-page-loaded="true"]', '#root', 'body', 'html'];
            for (var i = 0; i < selectors.length; i++) {{
                var elements = document.querySelectorAll(selectors[i]);
                for (var j = 0; j < elements.length; j++) {{
                    var el = elements[j];
                    if (isScrollable(el)) {{
                        el.scrollTop += pixels;
                        return {{scrolled: true, selector: selectors[i], scrollTop: el.scrollTop}};
                    }}
                }}
            }}
            
            // If no specific element found, try scrolling all scrollable elements
            var allElements = document.querySelectorAll('*');
            for (var k = 0; k < allElements.length; k++) {{
                var elem = allElements[k];
                if (isScrollable(elem) && elem.scrollHeight > elem.clientHeight + 100) {{
                    elem.scrollTop += pixels;
                    return {{scrolled: true, selector: elem.tagName, scrollTop: elem.scrollTop}};
                }}
            }}
            
            // Fallback: try window scroll
            window.scrollBy(0, pixels);
            return {{scrolled: true, selector: 'window', scrollTop: window.pageYOffset}};
            """
            
            result = self.driver.execute_script(scroll_script)
            if result and result.get('scrolled'):
                logger.info(f"Scrolled {result.get('selector')} by {pixels} pixels (scrollTop: {result.get('scrollTop')})")
            else:
                logger.warning("Scroll command executed but no scrollable element found")
                
        except Exception as e:
            logger.error(f"Failed to scroll: {str(e)}")
            raise
    
    def wait_for_page_load(self, timeout: int = 30) -> None:
        """
        Wait for page to load completely.
        
        Args:
            timeout: Timeout in seconds
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            logger.info("Page loaded completely")
        except TimeoutException:
            logger.warning("Page load timeout")
    
    def switch_to_frame(self, locator: Tuple[str, str]) -> None:
        """
        Switch to an iframe.
        
        Args:
            locator: Tuple of (By, value)
        """
        try:
            frame = self.find_element(locator)
            self.driver.switch_to.frame(frame)
            logger.info(f"Switched to frame: {locator}")
        except Exception as e:
            logger.error(f"Failed to switch to frame {locator}: {str(e)}")
            raise
    
    def switch_to_default_content(self) -> None:
        """Switch back to default content from iframe."""
        self.driver.switch_to.default_content()
        logger.info("Switched to default content")
    
    def get_current_url(self) -> str:
        """
        Get current URL.
        
        Returns:
            str: Current URL
        """
        url = self.driver.current_url
        logger.debug(f"Current URL: {url}")
        return url
    
    def get_page_title(self) -> str:
        """
        Get page title.
        
        Returns:
            str: Page title
        """
        title = self.driver.title
        logger.debug(f"Page title: {title}")
        return title
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take a screenshot.
        
        Args:
            name: Screenshot name
            
        Returns:
            str: Path to screenshot
        """
        return self.screenshot_helper.take_screenshot(name)
    
    def close_modal_if_present(self, close_button_locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Close modal/popup if present.
        
        Args:
            close_button_locator: Locator for close button
            timeout: Timeout to wait for modal
            
        Returns:
            bool: True if modal was closed, False if not present
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            close_button = wait.until(EC.element_to_be_clickable(close_button_locator))
            close_button.click()
            logger.info("Modal closed")
            return True
        except TimeoutException:
            logger.debug("No modal present")
            return False
    
    def hover_over_element(self, locator: Tuple[str, str]) -> None:
        """
        Hover over an element.
        
        Args:
            locator: Tuple of (By, value)
        """
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            logger.error(f"Failed to hover over element {locator}: {str(e)}")
            raise


