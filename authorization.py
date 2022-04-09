import os, json
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
    session_file_name = 'data/' + get_chat_id(update) + '.json'
    if os.path.exists(session_file_name):
        with open(session_file_name) as json_file:
            school.session_data = json.load(json_file)
            logger.info("Session id %s ", school.session_data['session_id'])

            update.message.reply_text(
                'Вы авторизованный пользователь',  # FIXME parse and say to user real name of account
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END

    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
        'Привет! Сначала нужно авторизоваться в электронном дневнике?\nХотите это сделать?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Да?'
        ),
    )

    return LOGIN


userLogin = ''
userPassword = ''

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
    global userLogin
    userLogin = update.message.text
    user = update.message.from_user
    logger.info("Login for %s is %s", user.first_name, userLogin)
    update.message.reply_text(
        'Ok, теперь пароль',
        reply_markup=ReplyKeyboardRemove(),
    )
    return AUTHORIZE

def authorize(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    global userLogin, userPassword, chat_id

    os.environ['chat_id'] = str(get_chat_id(update))
    logger.info("Chat Id = %s \n", os.environ['chat_id'])

    userPassword = update.message.text
    user = update.message.from_user
    logger.info("Login and password for %s is %s / %s", user.first_name, userLogin, userPassword)

    auth_result = school.auth(userLogin, userPassword)

    logger.info("Password for %s is %s and auth result is %s", user.first_name, update.message.text, auth_result)

    update.message.reply_text(
        'Авторизация крайне успешна',  # FIXME parse and say to user real name of account
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


# method to get chat id
def get_chat_id(update):
    chat_id = None
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.channel_post is not None:
        chat_id = update.channel_post.chat.id
    return str(chat_id)





