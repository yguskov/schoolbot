import logging
import math

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import school
import datetime

import telegramcalendar
import messages


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END


HOMEWORK, DATE, TOMORROW, GRADES = range(4)


def start_homework(update: Update, context: CallbackContext) -> int:
    """Verify that user is authorized."""
    if not school.is_auth_ok(update):
        update.message.reply_text(
            'Пожалуйста, авторизуйтесь, для этого запустите команду /start',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    reply_keyboard = [['Дз на завтра', 'Дз на определенное число']]

    update.message.reply_text(
        'Сделайте выбор',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Дз на завтра'
        ),
    )

    return HOMEWORK


def homework(update: Update, context: CallbackContext) -> int:

    if update.message.text != 'Дз на завтра':
        update.message.reply_text(text='Выберите дату',
                                  reply_markup=telegramcalendar.create_calendar())
        return ConversationHandler.END
    else:
        return tomorrow(update, context)

def inline_calendar_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        short_date = messages.calendar_response_message % (date.strftime("%d.%m"))
        today = datetime.datetime.now()
        monday1 = (date - datetime.timedelta(days=date.weekday()))
        monday2 = (today - datetime.timedelta(days=today.weekday()))
        result = school.read_homework(short_date, math.ceil((monday2 - monday1).days / 7))
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=result,
                                 reply_markup=ReplyKeyboardRemove())


def date(update: Update, context: CallbackContext) -> int:
    x = 'Дз на ' + update.message.text
    update.message.reply_text(x, reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


def tomorrow(update: Update, context: CallbackContext) -> int:
    logger.info("Tomorrow is %s", (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m'))
    short_day = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m')
    hometask = school.read_homework(short_day, 0)
    update.message.reply_text('Домашнее задание на '+hometask, reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


conv_handler_homework = ConversationHandler(
    entry_points=[CommandHandler('homework', start_homework)],
    states={
        HOMEWORK: [MessageHandler(Filters.regex('^(Дз на завтра|Дз на определенное число)$'), homework)],
        DATE: [MessageHandler(Filters.text, date)],
        TOMORROW: [MessageHandler(Filters.text & ~Filters.command, tomorrow)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

