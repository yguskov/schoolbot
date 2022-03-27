import logging
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


HOMEWORK, DATE, TOMORROW = range(3)

def start(update: Update, context: CallbackContext) -> int:
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

def grades(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Оценки в четверти')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5040799832:AAF9F8KTQr6CuAKKz8ciWkBuKxQHuOBrTcI")
    # updater = Updater("5043534943:AAGNjukWrf9a-u1f-33wN6sF09N9WPwzdl0")


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("homework", homework))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HOMEWORK: [MessageHandler(Filters.regex('^(Дз на завтра|Дз на определенное число)$'), homework)],
            DATE: [MessageHandler(Filters.text, date)],
            TOMORROW: [MessageHandler(Filters.text & ~Filters.command, tomorrow)],
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

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.message.from_user
    # logger.info("Help to User %s.", user.first_name)
    update.message.reply_text('Help!')

if __name__ == '__main__':
    main()
