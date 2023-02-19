from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update


BOT_KEY = "6081728663:AAFap3-a7_eL9RV9NQNcm5ijxcWP5VUTQFQ"


def start(update: Update, context: CallbackContext):
    welcome_message = "Ласкаво просимо до легкої здачі сесії"
    update.message.reply_text(welcome_message, parse_mode="html")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(f"У випадку питань - пишіть на bobroliu@fit.cvut.cz")


def _add_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("Почати", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


if __name__ == "__main__":
    updater = Updater(BOT_KEY, use_context=True)
    _add_handlers(updater)
    print("starting to poll...")
    updater.start_polling()