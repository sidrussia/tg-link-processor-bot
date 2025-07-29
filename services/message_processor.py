import re
import logging
from services.url_processor import URLProcessor

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Service for processing messages and extracting hashtags"""

    # Dictionary of rules: key phrase -> hashtag
    HASHTAG_RULES = {
        "useful:": "#useful",
        "haha:": "#haha",
        "cure boredom:": "#cure",
        "that's interesting:": "#interesting",
        "that's cool:": "#cool",
        "game:": "#game",
        "chill out:": "#chill",
        "how to:": "#howto"
    }

    @classmethod
    def extract_hashtag_from_text(cls, text):
        """Extracts hashtag based on text content"""
        logger.info(f"Analyzing text for hashtag: '{text}'")

        # Normalize text: remove extra spaces, convert to lowercase,
        # replace all types of quotes and apostrophes with regular ones
        clean_text = ' '.join(text.split()).lower()

        # Replace smart quotes
        clean_text = clean_text.replace('"', '"').replace('"', '"')
        # Replace smart apostrophes (character 8217 and others)
        clean_text = clean_text.replace(''', "'").replace(''', "'").replace('`', "'")
        # Additionally replace character 8217 directly
        clean_text = clean_text.replace(chr(8217), "'")

        logger.info(f"Normalized text: '{clean_text}'")

        # Check each rule
        for phrase, hashtag in cls.HASHTAG_RULES.items():
            logger.info(f"Looking for phrase: '{phrase}'")
            if phrase in clean_text:
                logger.info(f"✅ Found phrase '{phrase}' -> {hashtag}")
                return hashtag
            else:
                logger.info(f"❌ Phrase '{phrase}' not found")

        # If nothing found, return empty string
        logger.info("Key phrases not found, hashtag not added")
        return ""

    @staticmethod
    def clean_text_from_urls(text):
        """Removes links from text for cleanliness"""
        # Remove markdown links [text](url)
        clean_text = re.sub(r'\[([^]]+)]\s*\([^)]+\)', r'\1', text)
        # Remove regular URLs
        clean_text = re.sub(r'https?://[^\s)]+', '', clean_text).strip()
        return clean_text

    @classmethod
    def process_message(cls, original_text, entities, channel_username):
        """Processes message according to requirements"""
        # 1. Extract URL from entities or text
        original_url = URLProcessor.extract_url_from_text_and_entities(original_text, entities)

        if not original_url:
            return "❌ No link found in message"

        logger.info(f"Found URL: {original_url}")

        # 2. Follow redirects (automatically chooses method)
        final_url = URLProcessor.follow_redirects(original_url)
        logger.info(f"URL after redirects: {final_url}")

        # 3. Clean URL
        clean_final_url = URLProcessor.clean_url(final_url)
        logger.info(f"Cleaned URL: {clean_final_url}")

        # 4. Extract hashtag based on content
        hashtag = cls.extract_hashtag_from_text(original_text)

        # 5. Remove links from original text for cleanliness
        clean_text = cls.clean_text_from_urls(original_text)

        # 6. Form final message with dynamic channel_username
        if hashtag:
            result_message = f"""{clean_text}

{clean_final_url}

@{channel_username}
{hashtag}"""
        else:
            result_message = f"""{clean_text}

{clean_final_url}

@{channel_username}"""

        return result_message
