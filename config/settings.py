import os
import logging
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Config:
    """A class for storing the app configuration"""

    # Telegram settings
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
    CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')

    # Selenium settings
    CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "chromedriver-mac-x64", "chromedriver")

    @classmethod
    def validate_env_variables(cls):
        """Checks if all required environment variables are present"""
        missing_vars = []

        if not cls.BOT_TOKEN:
            missing_vars.append('BOT_TOKEN')
        if not cls.CHANNEL_ID:
            missing_vars.append('CHANNEL_ID')
        if not cls.ADMIN_USER_ID:
            missing_vars.append('ADMIN_USER_ID')
        if not cls.CHANNEL_USERNAME:
            missing_vars.append('CHANNEL_USERNAME')

        if missing_vars:
            logger.error(f"The required environment variables are missing from the .env file: {', '.join(missing_vars)}")
            return False

        logger.info(f"Env variables loaded: channel @{cls.CHANNEL_USERNAME}")
        return True


# Create a configuration instance for import
config = Config()
