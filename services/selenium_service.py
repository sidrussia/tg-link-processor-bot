import logging
import time
from config.settings import config

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    SELENIUM_AVAILABLE = True
except ImportError:
    # Stubs for when Selenium is unavailable
    webdriver = None
    Options = None
    Service = None
    By = None
    WebDriverWait = None
    expected_conditions = None
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium is not installed. Automatic JavaScript link redirection is unavailable.")

logger = logging.getLogger(__name__)


class SeleniumService:
    """Service for working with Selenium and handling JavaScript redirects"""

    @staticmethod
    def is_available():
        """Checks Selenium availability"""
        return SELENIUM_AVAILABLE

    @staticmethod
    def follow_redirects_with_selenium(url):
        """Uses Selenium to handle JavaScript redirects"""
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium unavailable, using regular requests")
            return url

        driver = None
        try:
            # Configure Chrome in headless mode with additional options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # Use local ChromeDriver
            service = Service(config.CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Set optimized timeouts
            driver.set_page_load_timeout(15)  # 15 seconds for page load
            driver.implicitly_wait(5)  # 5 seconds for element search

            logger.info(f"Selenium: navigating to URL {url}")

            # Try to load the page
            try:
                driver.get(url)
            except Exception as load_error:
                logger.warning(f"Page load error: {load_error}")
                # If page didn't load, try to get current URL
                try:
                    current_url = driver.current_url
                    if current_url != url and current_url != "data:,":
                        logger.info(f"Got partial redirect: {current_url}")
                        return current_url
                except:
                    pass

            # Wait additional time for JavaScript redirects
            # Check URL every 2 seconds for 10 seconds
            for i in range(5):  # 5 attempts of 2 seconds = 10 seconds
                time.sleep(2)
                try:
                    current_url = driver.current_url
                    if current_url != url:
                        logger.info(f"Selenium: redirect detected on iteration {i + 1}: {current_url}")
                        return current_url
                except Exception as e:
                    logger.warning(f"Error getting URL on iteration {i + 1}: {e}")
                    continue

            # If no redirect occurred, return current URL
            final_url = driver.current_url
            logger.info(f"Selenium: final URL after waiting: {final_url}")

            return final_url

        except Exception as e:
            logger.error(f"Selenium error: {e}")
            return url
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
