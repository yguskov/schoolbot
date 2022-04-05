import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import school

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    # update.message.reply_text(
    #     'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    # )

    return ConversationHandler.END

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


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.message.from_user
    logger.info("Help to User %s.", user.first_name)
    update.message.reply_text('Help!')


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOGIN: [MessageHandler(Filters.regex('^(Да|Нет)$'), login)],
        PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
        AUTHORIZE: [MessageHandler(Filters.text & ~Filters.command, authorize)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)







