import re
import logging
import requests
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)


class URLProcessor:
    """Service for URL processing: extraction, redirects, cleaning"""

    @staticmethod
    def extract_url_from_text_and_entities(message_text, entities):
        """Extracts URL from message entities or from text"""
        # First try to find in entities
        for entity in entities:
            if entity.type == 'text_link':
                return entity.url
            elif entity.type == 'url':
                # Extract URL from text by offset and length
                offset_start = entity.offset
                offset_end = entity.offset + entity.length
                return message_text[offset_start:offset_end]

        # If not found in entities, search in text with regex
        url_pattern = r'https?://[^\s\)]+(?=\s|\)|$)'
        urls = re.findall(url_pattern, message_text)
        if urls:
            return urls[0]

        return None

    @staticmethod
    def follow_redirects(url):
        """Follows redirects and returns final URL. First tries requests, then falls back to Selenium"""
        logger.info(f"Starting redirect processing for: {url}")

        # First attempt: Use regular HTTP requests
        try:
            logger.info("Attempting redirect with HTTP requests...")
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            response = session.get(url, allow_redirects=True, timeout=15)

            # Check if redirect occurred
            if response.url != url:
                logger.info(f"HTTP redirect successful: {url} -> {response.url}")
                return response.url

            # Check if this is a tracking/shortened URL that likely needs JavaScript

            tracking_domains = ['bit.ly', 'tinyurl.com', 't.co', 'media.hubspot.com', 'short.link', 'goo.gl', 'ow.ly']
            is_tracking_url = any(domain in url.lower() for domain in tracking_domains)

            # If it's a tracking URL or long tracking-style URL, try Selenium even if HTTP worked
            if is_tracking_url or len(url) > 200:
                logger.info(
                    f"Detected tracking/long URL ({len(url)} chars), trying Selenium even though HTTP returned {response.status_code}")
                raise requests.RequestException("Tracking URL detected, forcing Selenium")

            # Check if page loaded successfully (status code 200-299)
            if 200 <= response.status_code < 300:
                logger.info(f"HTTP request successful, no redirect found, returning original URL")
                return url
            else:
                logger.warning(f"HTTP request returned status {response.status_code}, trying Selenium fallback")
                raise requests.RequestException(f"HTTP {response.status_code}")

        except Exception as e:
            logger.warning(f"HTTP request failed or tracking URL detected: {e}. Falling back to Selenium...")

            # Second attempt: Use Selenium as fallback
            try:
                # Import here to avoid circular imports
                from services.selenium_service import SeleniumService

                if SeleniumService.is_available():
                    logger.info("Using Selenium fallback for redirect processing")
                    selenium_result = SeleniumService.follow_redirects_with_selenium(url)
                    logger.info(f"Selenium fallback result: {selenium_result}")
                    return selenium_result
                else:
                    logger.warning("Selenium not available, returning original URL")
                    return url

            except Exception as selenium_error:
                logger.error(f"Selenium fallback also failed: {selenium_error}")
                return url

    @staticmethod
    def clean_url(url):
        """Cleans URL from parameters"""
        try:
            parsed = urlparse(url)
            # Remove query parameters and fragment
            clean_parsed = parsed._replace(query='', fragment='')
            return urlunparse(clean_parsed)
        except Exception as e:
            logger.error(f"Error cleaning URL: {e}")
            return url
