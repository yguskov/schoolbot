#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from authorization import conv_handler, help_command, grades_command
from homework import conv_handler_homework, inline_calendar_handler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("5040799832:AAF9F8KTQr6CuAKKz8ciWkBuKxQHuOBrTcI")  # py_guskov_bot
    updater = Updater("5043534943:AAGNjukWrf9a-u1f-33wN6sF09N9WPwzdl0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("grades", grades_command))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler_homework)
    dispatcher.add_handler(CallbackQueryHandler(inline_calendar_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
