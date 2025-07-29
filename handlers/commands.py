import os
import signal
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import config
from services.selenium_service import SeleniumService

logger = logging.getLogger(__name__)


class CommandHandlers:
    """Class for processing bot commands"""

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /start command"""
        _ = context  # Suppress the warning about an unused parameter
        await update.message.reply_text(
            "Hi! Send me a message with the link and I'll process it for the channel.\n\n"
            "Commands:\n"
            "/test_selenium - test Selenium\n"
            "/stop - stop the bot (admin only)"
        )

    @staticmethod
    async def test_selenium(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test Selenium"""
        _ = context
        if update.effective_user.id != config.ADMIN_USER_ID:
            return

        test_url = "https://www.google.com"
        try:
            result = SeleniumService.follow_redirects_with_selenium(test_url)
            await update.message.reply_text(
                f"✅ Selenium works!\n"
                f"Test URL: {test_url}\n"
                f"Result: {result}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Selenium error: {str(e)}")

    @staticmethod
    async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stops the bot (admin only)"""
        _ = context  # Suppress the warning about an unused parameter

        # Checking for administrator permissions
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You don't have permission to stop the bot.")
            return

        try:
            # Send confirmation message
            await update.message.reply_text("🛑 Stopping the bot... Goodbye!")
            logger.info("Received bot stop command from administrator")

            # Simulate Ctrl+C - send SIGINT signal to itself
            logger.info("Sending a SIGINT signal for correct termination...")
            os.kill(os.getpid(), signal.SIGINT)

        except Exception as e:
            logger.error(f"Error when stopping bot: {e}")
            await update.message.reply_text(f"❌ Error on stopping: {str(e)}")
            # If an error occurs, we also try to terminate the process
            os.kill(os.getpid(), signal.SIGINT)
