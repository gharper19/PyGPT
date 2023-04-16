import telegram
from telegram.ext.updater import Updater
from telegram.update import Update  # will invoke every time a bot receives an update
from telegram.ext.callbackcontext import CallbackContext # required when adding the dispatcher
from telegram.ext.commandhandler import CommandHandler # used to handle any command sent by the user
from telegram.ext.messagehandler import MessageHandler 
from telegram.ext.filters import Filters

import logging

logging.basicConfig(
    format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]',
    level=logging.INFO
)

TELEGRAM_BOT_KEY_FILEPATH = "../telegram_bot_key.txt"
TELEGRAM_BOT_KEY = ""

# Get API Key
with open(TELEGRAM_BOT_KEY_FILEPATH) as f:
    TELEGRAM_BOT_KEY = f.readlines()[0]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="...")

def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_KEY).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()

if __name__ == '__main__': 
    run_bot()

'''
# ---- ---- 

# Define the function to handle incoming messages
def message_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="...But no one came...")

# Set up the bot using the API token
TOKEN = TELEGRAM_BOT_KEY
bot = telegram.Bot(token=TOKEN)

# Set up the updater and dispatcher
updater = Updater(bot)
dispatcher = updater.dispatcher

# Add the message handler to the dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

# Start the bot
updater.start_polling()
updater.idle()
'''