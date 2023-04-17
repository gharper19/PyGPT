import telebot
import chat
from chat import submitCompletionMessage, parseResponse
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

# Initiate telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

# Apply decorator 
@bot.message_handler(func=lambda message: True) # func param is applied to every incoming msg to determine whether msg handler should trigger

def handle_message(msg): 
    ''' Gets user message text and submits content to GPT as a new user prompt '''
    # Extract the text content of the message.
    user_text = message.text

    # Send user's message to the submitCompletionMessage function and get the response.
    api_response = submitCompletionMessage('user', user_text)

    # Send the API response back to the user as a reply.
    bot.reply_to(message, api_response)

def echo_message(message):
    response = "...But no one came..."
    bot.reply_to(message, response)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__': 
    run_bot()