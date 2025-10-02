"""
Page Object Model for Twitch homepage.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui_tests.pages.base_page import BasePage
from ui_tests.utils.logger import get_logger
import time

logger = get_logger(__name__)


class TwitchHomePage(BasePage):
    """Page object for Twitch homepage."""
    
    # Locators for desktop Twitch
    SEARCH_ICON = (By.CSS_SELECTOR, "a[aria-label='Search']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_INPUT_ALT = (By.XPATH, "//input[@placeholder='Search' or @aria-label='Search Input']")
    
    # Search Results Page
    CHANNELS_TAB = (By.XPATH, "//a[contains(@href, '/search/channels')]")
    # More generic selectors for search results
    LIVE_CHANNELS = (By.XPATH, "//a[contains(@href, '/') and not(contains(@href, 'twitch.tv/p/'))]//h3")
    STREAMER_CARDS = (By.XPATH, "//a[contains(@class, 'tw-link') and contains(@href, '/')]")
    SEARCH_RESULT_LINKS = (By.CSS_SELECTOR, "a[class*='tw-link']")
    LIVE_INDICATOR = (By.XPATH, "//div[@data-a-target='animated-channel-viewers-count' or contains(@class, 'live-indicator')]")
    
    # Alternative selectors
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-label='Search']")
    SEARCH_BAR = (By.XPATH, "//input[@placeholder='Search' or @aria-label='Search Input']")
    
    def __init__(self, driver: WebDriver):
        """
        Initialize TwitchHomePage.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.url = "https://www.twitch.tv"
    
    def open(self) -> None:
        """Navigate to Twitch homepage."""
        logger.info("Opening Twitch homepage")
        self.navigate_to(self.url)
        self.wait_for_page_load()
        time.sleep(0.3)  # ⚡ AGGRESSIVE: Minimal wait for page to stabilize
        
        # Handle cookie consent banner if present
        self.handle_cookie_consent()
    
    def handle_cookie_consent(self) -> None:
        """Handle cookie consent banner if present."""
        try:
            # Try to find and click accept cookies button
            cookie_selectors = [
                (By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept']"),
                (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Consent')]"),
            ]
            
            for selector in cookie_selectors:
                try:
                    if self.is_element_visible(selector, timeout=1):  # ⚡ Reduced from 2s
                        self.click(selector)
                        logger.info("✓ Cookie consent handled")
                        time.sleep(0.2)  # ⚡ Reduced from 1s
                        return
                except Exception:
                    continue
        except Exception:
            logger.debug("No cookie consent banner")
    
    def click_search_icon(self) -> None:
        """Click on the search icon."""
        logger.info("Clicking search icon")
        try:
            # Try to find search button (may be hidden by overlays)
            search_element = None
            
            # Try CSS selector first
            if self.is_element_present(self.SEARCH_ICON):
                search_element = self.find_element(self.SEARCH_ICON)
            elif self.is_element_present(self.SEARCH_BUTTON):
                search_element = self.find_element(self.SEARCH_BUTTON)
            
            if search_element:
                # Try JavaScript click to bypass visibility issues
                self.driver.execute_script("arguments[0].click();", search_element)
                logger.info("✓ Search icon clicked (via JavaScript)")
            else:
                logger.error("Search icon not found")
                raise Exception("Search icon not present")
            
            time.sleep(0.2)  # ⚡ AGGRESSIVE: Minimal wait for search input
        except Exception as e:
            logger.error(f"Failed to click search icon: {str(e)}")
            raise
    
    def enter_search_query(self, query: str) -> None:
        """
        Enter a search query and press ENTER to submit.
        
        Args:
            query: Search query text
        """
        logger.info(f"Entering search query: {query}")
        try:
            # Wait for search input to be visible
            search_input = None
            if self.is_element_visible(self.SEARCH_INPUT, timeout=5):
                search_input = self.find_element(self.SEARCH_INPUT)
                logger.info("Found search input using SEARCH_INPUT selector")
            elif self.is_element_visible(self.SEARCH_INPUT_ALT, timeout=5):
                search_input = self.find_element(self.SEARCH_INPUT_ALT)
                logger.info("Found search input using SEARCH_INPUT_ALT selector")
            else:
                logger.error("Search input not found")
                raise Exception("Search input field not found")
            
            # Click on the search input
            search_input.click()
            logger.info("Clicked on search input")
            time.sleep(0.1)  # ⚡ AGGRESSIVE: Minimal wait
            
            # Clear any existing text
            search_input.clear()
            
            # Type the query
            search_input.send_keys(query)
            logger.info(f"✓ Entered query: {query}")
            
            time.sleep(0.2)  # ⚡ AGGRESSIVE: Brief pause before ENTER
            
            # Press ENTER to submit search
            from selenium.webdriver.common.keys import Keys
            search_input.send_keys(Keys.ENTER)
            logger.info("✓ Pressed ENTER to submit search")
            
            # Wait for navigation to complete using explicit wait
            logger.info("Waiting for search results page to load...")
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Wait for URL to change to search results
            WebDriverWait(self.driver, 5).until(  # ⚡ Reduced from 10s
                EC.url_contains("/search")
            )
            time.sleep(0.3)  # ⚡ AGGRESSIVE: Minimal wait for content
            
            # Verify we're on search page
            current_url = self.get_current_url()
            logger.info(f"After ENTER - Current URL: {current_url}")
            
        except Exception as e:
            logger.error(f"Failed to enter search query: {str(e)}")
            self.take_screenshot("search_query_error")
            raise
    
    def search_for(self, query: str) -> None:
        """
        Perform a complete search operation.
        
        Args:
            query: Search query text
        """
        logger.info(f"Searching for: {query}")
        self.click_search_icon()
        self.enter_search_query(query)
    
    def scroll_down(self, times: int = 1, pixels: int = 500) -> None:
        """
        Scroll down the page multiple times.
        
        Args:
            times: Number of times to scroll
            pixels: Pixels to scroll each time
        """
        logger.info(f"Scrolling down {times} times")
        for i in range(times):
            self.scroll_by_pixels(pixels)
            time.sleep(0.2)  # ⚡ AGGRESSIVE: Minimal wait for content
            logger.debug(f"Scroll {i+1}/{times} completed")
    
    def get_live_streamer_cards(self) -> list:
        """
        Get list of LIVE streamer cards from search results.
        
        Returns:
            list: List of WebElements representing live streamer cards
        """
        try:
            # Wait a bit for results to load
            time.sleep(0.3)  # ⚡ AGGRESSIVE: Minimal wait for results
            
            # Try multiple selectors for streamer links
            selectors_to_try = [
                self.LIVE_CHANNELS,
                self.STREAMER_CARDS,
                self.SEARCH_RESULT_LINKS,
                (By.XPATH, "//a[contains(@href, '/') and .//h3]"),  # Links with h3 tags (channel names)
                (By.CSS_SELECTOR, "a[href^='/']"),  # Any link starting with /
            ]
            
            cards = []
            for selector in selectors_to_try:
                cards = self.find_elements(selector)
                if cards:
                    # Filter out navigation links, keep only channel links
                    filtered_cards = [card for card in cards if self._is_channel_link(card)]
                    if filtered_cards:
                        logger.info(f"Found {len(filtered_cards)} live streamer cards")
                        return filtered_cards
            
            logger.warning(f"Found {len(cards)} cards but none appear to be channel links")
            return cards[:10] if cards else []  # Return first 10 if we can't filter
            
        except Exception as e:
            logger.error(f"Failed to get streamer cards: {str(e)}")
            return []
    
    def _is_channel_link(self, element) -> bool:
        """Check if element is a channel link (not navigation/footer link)."""
        try:
            href = element.get_attribute("href")
            if not href or "twitch.tv/" not in href:
                return False
            
            # Extract the path after twitch.tv/
            path = href.split("twitch.tv/")[-1].strip("/")
            
            # Empty path or just query params - not a channel
            if not path or path.startswith("?"):
                return False
            
            # Split path into segments
            path_segments = path.split("/")
            channel_name = path_segments[0]
            
            # Exclude common non-channel paths
            exclude_patterns = ['directory', 'search', 'prime', 'turbo', 'downloads', 'jobs', 'about', 'p', 'videos', 'clips', 'settings', 'subscriptions', 'inventory', 'wallet', 'drops', 'friends']
            
            # Valid channel link must:
            # 1. Have a channel name
            # 2. Not be in exclude list
            # 3. Be exactly /channelname (no additional segments like /videos)
            is_valid = (channel_name and 
                       channel_name not in exclude_patterns and 
                       len(channel_name) > 1 and  # At least 2 chars
                       len(path_segments) == 1)  # No sub-paths
            
            if is_valid:
                logger.debug(f"Valid channel link: {href}")
            
            return is_valid
        except Exception as e:
            logger.debug(f"Error checking channel link: {str(e)}")
            return False
    
    def get_streamer_cards(self) -> list:
        """Alias for get_live_streamer_cards for backward compatibility."""
        return self.get_live_streamer_cards()
    
    def click_first_live_streamer(self) -> None:
        """Click on the first LIVE streamer from search results."""
        logger.info("Clicking first LIVE streamer")
        try:
            cards = self.get_live_streamer_cards()
            logger.info(f"Retrieved {len(cards)} cards for clicking")
            
            if cards:
                # Log info about the first card
                first_card = cards[0]
                card_href = first_card.get_attribute("href")
                card_text = first_card.text[:100] if first_card.text else "No text"
                logger.info(f"First card - HREF: {card_href}")
                logger.info(f"First card - Text: {card_text}")
                
                # Scroll to the first card to make sure it's in view
                logger.info("Scrolling first card into view...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cards[0])
                time.sleep(0.2)  # ⚡ AGGRESSIVE: Brief wait after scroll
                
                # Highlight element for debugging (optional) - SKIP for speed
                # try:
                #     self.driver.execute_script("arguments[0].style.border='3px solid red'", cards[0])
                #     time.sleep(0.2)
                # except:
                #     pass
                
                # Click using JavaScript to avoid interception issues
                logger.info("Executing click via JavaScript...")
                self.driver.execute_script("arguments[0].click();", cards[0])
                logger.info("Click executed successfully")
                
                # Wait for navigation using explicit wait
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                WebDriverWait(self.driver, 5).until(  # ⚡ Reduced from 10s
                    lambda driver: "/search" not in driver.current_url
                )
                time.sleep(0.3)  # ⚡ AGGRESSIVE: Minimal wait after navigation
                logger.info("✓ Clicked first LIVE streamer successfully")
            else:
                logger.error("No live streamer cards found")
                self.take_screenshot("no_streamers_found")
                raise Exception("No LIVE streamers found in search results")
        except Exception as e:
            logger.error(f"Failed to click first streamer: {str(e)}")
            self.take_screenshot("click_streamer_error")
            raise
    
    def click_first_streamer(self) -> None:
        """Alias for click_first_live_streamer for backward compatibility."""
        self.click_first_live_streamer()
    
    def is_search_results_page_loaded(self) -> bool:
        """
        Check if search results page is loaded with Channels tab.
        
        Returns:
            bool: True if search results page is displayed
        """
        time.sleep(2)
        
        # Check if we're on the search results page
        current_url = self.get_current_url()
        is_search_page = "/search" in current_url
        
        # Check if we have live streamer cards
        cards = self.get_live_streamer_cards()
        has_cards = len(cards) > 0
        
        is_loaded = is_search_page and has_cards
        logger.info(f"Search results page loaded: {is_loaded} (URL contains '/search': {is_search_page}, {len(cards)} cards found)")
        return is_loaded
    
    def is_search_results_displayed(self) -> bool:
        """Alias for is_search_results_page_loaded for backward compatibility."""
        return self.is_search_results_page_loaded()


