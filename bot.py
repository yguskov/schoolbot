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

from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import school

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

# def start(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )

LOGIN, PASSWORD, AUTHORIZE = range(3)

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
        'Привет! Сначала нужно авторизоваться в электронном дневнике?\nХотите это сделать?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Да?'
        ),
    )

    return LOGIN


def login(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("User %s say %s", user.first_name, update.message.text)

    if update.message.text != 'Да' :
        update.message.reply_text(
                'Ну и ладно',
                reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Укажите логин',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PASSWORD

def password(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Login for %s is %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ok, теперь пароль',
        reply_markup=ReplyKeyboardRemove(),
    )

    return AUTHORIZE

def authorize(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user

    authResult = school.auth("some_login", update.message.text)

    logger.info("Password for %s is %s and auth result is %s", user.first_name, update.message.text, authResult)

    update.message.reply_text(
        'Авторизация крайне успешна',
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.message.from_user
    logger.info("Help to User %s.", user.first_name)
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user = update.effective_user
    message = update.message.text
    update.message.reply_markdown_v2(
        f'Сам ты, {user.mention_markdown_v2()} не поэт\!\n У самого у тебя {message}',
    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("5040799832:AAF9F8KTQr6CuAKKz8ciWkBuKxQHuOBrTcI")
    updater = Updater("5043534943:AAGNjukWrf9a-u1f-33wN6sF09N9WPwzdl0")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", authorize))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOGIN: [MessageHandler(Filters.regex('^(Да|Нет)$'), login)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
            AUTHORIZE: [MessageHandler(Filters.text & ~Filters.command, authorize)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)


    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
