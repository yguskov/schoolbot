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


HOMEWORK, DATE, TOMORROW, GRADES = range(4)


def start_homework(update: Update, context: CallbackContext) -> int:
    """Verify that user is authorized."""
    if not school.is_auth_ok(update):
        update.message.reply_text(
            'Пожалуйста, авторизуйтесь, для этого запустите команду /start',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    """Starts the conversation and asks the user about their gender."""
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
        update.message.reply_text(
                'На какое число?',
                reply_markup=ReplyKeyboardRemove(),
        )
        return DATE
    else:
        return tomorrow(update, context)


def date(update: Update, context: CallbackContext) -> int:
    x = 'Дз на ' + update.message.text
    update.message.reply_text(x, reply_markup=ReplyKeyboardRemove(),)
    return ConversationHandler.END


def tomorrow(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s say %s", user.first_name, update.message.text)

    update.message.reply_text('Вот вам дз на завтра', reply_markup=ReplyKeyboardRemove(),)
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

