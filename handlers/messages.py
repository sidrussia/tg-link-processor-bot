import logging
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import config
from services.message_processor import MessageProcessor

logger = logging.getLogger(__name__)


class MessageHandlers:
    """Class for handling text messages"""

    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Text message handler"""
        # Check that the message is from admin
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You don't have permission to use this bot.")
            return

        try:
            # Get text and entities
            message_text = update.message.text
            entities = update.message.entities or []

            logger.info(f"Received message: '{message_text}'")

            # Process message with channel_username parameter
            processed_message = MessageProcessor.process_message(
                message_text,
                entities,
                config.CHANNEL_USERNAME
            )

            logger.info(f"Processing result: '{processed_message}'")

            # Check if there's an error (message starts with ❌)
            if processed_message.startswith("❌"):
                logger.info("Link not found, sending only to user")
                # If link not found, only notify user, DON'T post to channel
                await update.message.reply_text(processed_message)
                return

            logger.info("Link found, sending to channel")

            # Send to channel silently only if link found and processed
            await context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=processed_message,
                disable_notification=True
            )

            # Confirmation to user
            await update.message.reply_text("✅ Message successfully sent to channel!")

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(f"❌ An error occurred: {str(e)}")

    @staticmethod
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Error handler"""
        logger.error(f"Update {update} caused error {context.error}")
