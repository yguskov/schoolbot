import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from authorization import conv_handler, help_command, grades_command
from homework import conv_handler_homework, inline_calendar_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    updater = Updater("5043534943:AAGNjukWrf9a-u1f-33wN6sF09N9WPwzdl0")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("grades", grades_command))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler_homework)
    dispatcher.add_handler(CallbackQueryHandler(inline_calendar_handler))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
