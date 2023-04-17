import telebot
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

# Create bot
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

# Apply decorator 
@bot.message_handler(func=lambda message: True) # func param is applied to every incoming msg to determine whether msg handler should trigger
def echo_message(message):
    response = "...But no one came..."
    bot.reply_to(message, response)

def run_bot():
    bot.polling(none_stop=True)

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