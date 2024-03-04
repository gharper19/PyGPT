import telebot
from telebot import util
from ChatCompletion import GPTChatCompletion
from GPTChatCompletion import submitCompletionMessage, parseResponse
import logging

TELEGRAM_BOT_KEY_FILEPATH = "../telegram_bot_key.txt"
TELEGRAM_BOT_KEY = ""

TEXT_CHAR_LIMIT = 4096

HELP_MESSAGE = '''
    Commands:
        - /start - start new telegram bot
        - /new - start new GPT bot
        - /help - show help menu
        - /settings - ?
    '''


logging.basicConfig(
    format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]',
    level=logging.INFO
)

# Get API Key
with open(TELEGRAM_BOT_KEY_FILEPATH) as f:
    TELEGRAM_BOT_KEY = f.readlines()[0]
    if TELEGRAM_BOT_KEY == "": raise ValueError(f"No value found for Telegram API Key at: {TELEGRAM_BOT_KEY_FILEPATH}")

# Initiate telegram bot
telegram_bot = telebot.TeleBot(TELEGRAM_BOT_KEY)
chat_id = ''

# Initiate ChatCompletionBot
gpt;

@telegram_bot.message_handler(regexp="ey mane") 
@telegram_bot.message_handler(commands=['start'])
def handle_init_help_text(msg): 
    ''' Handles initializing telegram_bot from start commands and displaying help message
    if msg.'''
    send_help()

@telegram_bot.message_handler(commands=['help'])
def send_help(msg):
    send_telegram_message(HELP_MESSAGE)

@telegram_bot.message_handler(content_types=['text'])
def handle_message(msg): 
    ''' General message handlerGets user message text and submits content to GPT as a new user prompt '''
    # Extract the text content of the message.
    user_text = message.text

    # Send user's message to the submitCompletionMessage function and get the response.
    api_response = submitCompletionMessage('user', user_text)

    # Send the API response back to the user as a reply.
    telegram_bot.reply_to(message, api_response)

    # If you must send more than 4096 characters, use the split_string
    telegram_bot.send_message(chat_id, text)

def send_telegram_message(msg):
    if msg.length > TEXT_CHAR_LIMIT:
        # Split characters
        texts = util.split_string(msg, 3000)
    else:
        texts = [msg]

    for text in texts:
        telegram_bot.send_message(chat_id, text)

def initialize_GPT():
    global gpt
    try:
        # Initiate GPTChatCompletion bot
        gpt = GPTChatCompletion(
            #model="gpt-4"
            system_prompts=[
                "You are a helpful assistant focused on providing as much detail and context on topics as possible."
            ]
        )
    except Exception as e:
        send_telegram_message(e)

def echo_message(message):
    response = "...But no one came..."
    telegram_bot.reply_to(message, response)

def run_bot():
    telegram_bot.polling(none_stop=True)

if __name__ == '__main__': 
    run_bot()


# Edited Message handler
@telegram_bot.edited_message_handler(filters) # Handle edited messages 
def updated_edited_message(msg):
    pass