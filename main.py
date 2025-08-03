"""
Telegram bot for link processing and channel posting.
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import config
from handlers.commands import CommandHandlers
from handlers.messages import MessageHandlers

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variable to store Application object
application = None


def main():
    """Main bot startup function"""
    global application

    # Validate environment variables
    if not config.validate_env_variables():
        return

    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", CommandHandlers.start))
    application.add_handler(CommandHandler("test_selenium", CommandHandlers.test_selenium))
    application.add_handler(CommandHandler("stop", CommandHandlers.stop_bot))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, MessageHandlers.handle_message))

    # Add error handler
    application.add_error_handler(MessageHandlers.error_handler)

    # Start the bot
    logger.info("Bot started...")
    application.run_polling(
        timeout=60,
        read_timeout=65,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
