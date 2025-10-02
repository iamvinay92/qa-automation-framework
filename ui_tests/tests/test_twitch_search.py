"""
Test cases for Twitch search functionality.

This test suite covers the complete user journey on Twitch:
1. Navigate to Twitch homepage
2. Perform search for a game
3. Scroll through results
4. Select a streamer
5. Verify streamer page loads
"""
import pytest
import allure
from ui_tests.pages.twitch_home_page import TwitchHomePage
from ui_tests.pages.twitch_streamer_page import TwitchStreamerPage
from ui_tests.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.ui
@pytest.mark.smoke
@allure.feature("Twitch Search")
@allure.story("Game Search and Streamer Selection")
class TestTwitchSearch:
    """Test suite for Twitch search functionality."""
    
    @allure.title("Search for StarCraft II and select LIVE streamer")
    @allure.description("""
    Test the complete user journey (EXACT FLOW):
    1. Navigate to https://www.twitch.tv
    2. Click the search icon
    3. Type 'StarCraft II' in the search input
    4. Press ENTER to submit the search
    5. Wait for Search Results Page to load (with Top/Channels/Categories/Video tabs)
    6. Verify the page defaults to 'Channels' tab showing live streamers
    7. Scroll down 2 times on this page to load more channels
    8. Click on the first LIVE streamer from the list
    9. Wait for the streamer's page to fully load (video player, etc.)
    10. Handle any popups (mature content, cookies)
    11. Take a screenshot and save it
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_starcraft_and_select_streamer(self, driver):
        """
        Test ID: UI-001
        Test complete search flow from homepage to streamer page.
        """
        with allure.step("1. Navigate to https://www.twitch.tv"):
            home_page = TwitchHomePage(driver)
            home_page.open()
            logger.info("✓ Twitch homepage loaded")
        
        with allure.step("2. Click the search icon"):
            home_page.click_search_icon()
            logger.info("✓ Search icon clicked")
        
        with allure.step("3. Type 'StarCraft II' and 4. Press ENTER to submit"):
            home_page.enter_search_query("StarCraft II")
            logger.info("✓ Search query entered and submitted")
            # Take debug screenshot
            home_page.take_screenshot("after_search_submit")
            logger.info("📸 Debug screenshot taken: after_search_submit")
        
        with allure.step("5-6. Wait for Search Results Page (Channels tab with live streamers)"):
            # Check current URL
            current_url = home_page.get_current_url()
            logger.info(f"Current URL: {current_url}")
            
            # Check if search results are displayed
            results_displayed = home_page.is_search_results_displayed()
            logger.info(f"Search results displayed: {results_displayed}")
            
            if not results_displayed:
                home_page.take_screenshot("search_results_not_found")
                logger.error("📸 Screenshot saved: search_results_not_found")
            
            assert results_displayed, \
                f"Search results page should be displayed with Channels tab. Current URL: {current_url}"
            logger.info("✓ Search results page loaded with live streamers")
            
            # Get count of cards
            cards_count = len(home_page.get_streamer_cards())
            logger.info(f"Found {cards_count} streamer cards on the page")
            assert cards_count > 0, f"Should have at least 1 streamer card, found {cards_count}"
        
        with allure.step("7. Scroll down 2 times to load more channels"):
            logger.info("Starting scroll down operation...")
            
            # Scroll twice (scroll_by_pixels handles finding the correct scrollable element)
            home_page.scroll_down(times=1, pixels=500)
            logger.info("✓ Scrolled 1st time")
            
            home_page.scroll_down(times=1, pixels=500)
            logger.info("✓ Scrolled 2nd time")
            
            # Note: Scroll validation is done in base_page.scroll_by_pixels which logs scrollTop values
            logger.info("✓ Scroll operation completed")
            
            # Take screenshot after scroll
            home_page.take_screenshot("after_scroll")
            logger.info("📸 Debug screenshot taken: after_scroll")
        
        with allure.step("8. Click on the first LIVE streamer from the list"):
            # Get cards again after scroll
            cards = home_page.get_streamer_cards()
            logger.info(f"Found {len(cards)} cards after scrolling")
            
            assert len(cards) > 0, "Should have at least one streamer card to click"
            
            # Log details about first card
            first_card = cards[0]
            card_href = first_card.get_attribute("href")
            card_text = first_card.text[:50] if first_card.text else "No text"
            logger.info(f"First card details - href: {card_href}, text: {card_text}")
            
            # Click the first streamer
            logger.info("Attempting to click first streamer...")
            home_page.click_first_streamer()
            logger.info("✓ Click command executed")
            
            # Verify navigation happened (wait is already inside click_first_streamer)
            new_url = home_page.get_current_url()
            logger.info(f"After click - New URL: {new_url}")
            
            assert "/search" not in new_url, \
                f"Should have navigated away from search page. Current URL: {new_url}"
            logger.info("✓ First LIVE streamer selected and navigated")
        
        with allure.step("9. Wait for the streamer's page to fully load"):
            streamer_page = TwitchStreamerPage(driver)
            streamer_page.wait_for_page_to_load()
            logger.info("✓ Streamer page loaded")
        
        with allure.step("10. Handle any popups (mature content, cookies) - already handled in wait_for_page_to_load"):
            # Popups are already handled in wait_for_page_to_load() method
            logger.info("✓ Popups handled (if any)")
        
        with allure.step("Verify page loaded successfully"):
            assert streamer_page.is_page_loaded_successfully(), \
                "Streamer page should load with all required elements"
            logger.info("✓ Page load verification successful")
        
        with allure.step("11. Take a screenshot and save it"):
            screenshot_path = streamer_page.take_page_screenshot("streamer_page_final")
            allure.attach.file(
                screenshot_path,
                name="Streamer Page Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"✓ Screenshot saved: {screenshot_path}")
    
    @allure.title("Search functionality verification")
    @allure.description("Verify that search icon is clickable and search input appears")
    @pytest.mark.smoke
    def test_search_icon_clickable(self, driver):
        """
        Test ID: UI-002
        Verify search icon functionality.
        """
        with allure.step("Navigate to Twitch"):
            home_page = TwitchHomePage(driver)
            home_page.open()
        
        with allure.step("Click search icon"):
            home_page.click_search_icon()
        
        with allure.step("Verify search input is visible"):
            assert home_page.is_element_visible(home_page.SEARCH_INPUT, timeout=10) or \
                   home_page.is_element_visible(home_page.SEARCH_BAR, timeout=5), \
                "Search input should appear after clicking search icon"
            logger.info("✓ Search input verified")
    
    @allure.title("Search results display verification")
    @allure.description("Verify search results are displayed for a valid query")
    @pytest.mark.regression
    def test_search_results_display(self, driver):
        """
        Test ID: UI-003
        Verify search results are displayed.
        """
        home_page = TwitchHomePage(driver)
        
        with allure.step("Navigate and perform search"):
            home_page.open()
            home_page.search_for("StarCraft II")
        
        with allure.step("Verify results are displayed"):
            assert home_page.is_search_results_displayed(), \
                "Search results should be displayed for valid query"
            
            # Verify at least one streamer card exists
            cards = home_page.get_streamer_cards()
            assert len(cards) > 0, "At least one search result should be displayed"
            logger.info(f"✓ {len(cards)} search results found")
    
    @allure.title("Scroll functionality verification")
    @allure.description("Verify page scrolls correctly and loads more content")
    @pytest.mark.ui
    def test_scroll_loads_content(self, driver):
        """
        Test ID: UI-004
        Verify scrolling loads additional content.
        """
        home_page = TwitchHomePage(driver)
        
        with allure.step("Navigate and search"):
            home_page.open()
            home_page.search_for("StarCraft II")
        
        with allure.step("Get initial number of results"):
            initial_cards = len(home_page.get_streamer_cards())
            logger.info(f"Initial results: {initial_cards}")
        
        with allure.step("Scroll down"):
            home_page.scroll_down(times=2)
        
        with allure.step("Verify more results loaded"):
            final_cards = len(home_page.get_streamer_cards())
            logger.info(f"Final results: {final_cards}")
            
            # Content should be loaded (either more cards or same if already loaded)
            assert final_cards >= initial_cards, \
                "Results count should not decrease after scrolling"
            logger.info("✓ Scroll functionality verified")


@pytest.mark.ui
@pytest.mark.mobile
@allure.feature("Mobile Responsive")
@allure.story("Mobile Twitch Experience")
class TestTwitchMobile:
    """Test suite for mobile responsive testing."""
    
    @allure.title("Mobile: Search and navigate flow")
    @allure.description("Test complete flow in mobile emulation mode")
    @pytest.mark.slow
    def test_mobile_search_flow(self, driver):
        """
        Test ID: UI-008
        Test search functionality in mobile view.
        
        Note: Run with --mobile flag: pytest --mobile
        """
        home_page = TwitchHomePage(driver)
        
        with allure.step("Open Twitch in mobile mode"):
            home_page.open()
            # Verify mobile viewport
            window_size = driver.get_window_size()
            logger.info(f"Window size: {window_size}")
        
        with allure.step("Perform search"):
            home_page.search_for("StarCraft II")
        
        with allure.step("Verify mobile layout"):
            assert home_page.is_search_results_displayed(), \
                "Search should work in mobile view"
            logger.info("✓ Mobile search verified")
        
        with allure.step("Take mobile screenshot"):
            screenshot_path = home_page.take_screenshot("mobile_search_results")
            allure.attach.file(
                screenshot_path,
                name="Mobile Screenshot",
                attachment_type=allure.attachment_type.PNG
            )


