import os
import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import school

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END


LOGIN, PASSWORD, AUTHORIZE = range(3)


def start(update: Update, context: CallbackContext) -> int:
    if school.is_auth_ok(update):
            update.message.reply_text(
                'Вы авторизованный пользователь',  
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END

    reply_keyboard = [['Да', 'Нет']]

    update.message.reply_text(
        'Привет! Для использования бота нужно авторизоваться в электронном дневнике?\nДля этого нужно знать логин и пароль к сайту school.nso.ru.\nПродолжить?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Да?'
        ),
    )

    return LOGIN


userLogin = ''
userPassword = ''


def login(update: Update, context: CallbackContext) -> int:
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
    global userLogin, userPassword, chat_id
    os.environ['chat_id'] = str(school.get_chat_id(update))
    logger.info("Chat Id = %s \n", os.environ['chat_id'])

    userPassword = update.message.text
    user = update.message.from_user
    logger.info("Login and password for %s is %s / ***", user.first_name, userLogin)

    auth_result = school.auth(userLogin, userPassword)
    if auth_result:
        message = 'Авторизация прошла успешно'
    else:
        message = 'Авторизация не удалась, попробуйте другой пароль и логин'

    logger.info("Auth result is %d", auth_result)

    update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.message.from_user
    logger.info("Help to User %s.", user.first_name)
    update.message.reply_text("""/homework - домашняя работа на завтра или определённое число
/grades - успеваемость
/cancel - остановить выполнение команды""")


def grades_command(update: Update, context: CallbackContext) -> None:
    if not school.is_auth_ok(update):
        update.message.reply_text(
            'Пожалуйста, авторизуйтесь, для этого запустите команду /start',
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text('Оценки в четверти\n'+school.read_grades())


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOGIN: [MessageHandler(Filters.regex('^(Да|Нет)$'), login)],
        PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
        AUTHORIZE: [MessageHandler(Filters.text & ~Filters.command, authorize)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)






