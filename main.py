import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Khmer Welcome Message
WELCOME_TEXT = (
    "សូមស្វាគមន៍មកវេបសាយធំបំផុត ងាយស្រួលលេង📲 និងគួរឱ្យទុកចិត្តបំផុតនៅកម្ពុជា🔥"
    "សេវាកម្ម២៤ម៉ោង: https://t.me/Sdrservice24h"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Inline button linking directly to your Telegram service
    keyboard = [
        [
            InlineKeyboardButton(
                "💬 សេវាកម្ម២៤ម៉ោង (Contact Support)", 
                url="https://t.me/Sdrservice24h"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=False
    )

def main() -> None:
    # Get Bot Token from Render Environment Variable
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("No BOT_TOKEN provided in Environment Variables!")

    # Build Application
    application = Application.builder().token(token).build()

    # Register /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start Polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
