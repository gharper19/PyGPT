import telebot
from telebot import util

TEXT_CHAR_LIMIT = 4096
HELP_MESSAGE = '''
    Commands:
        - /start - start new telegram bot
        - /new - start new GPT bot
        - /help - show help menu
        - /settings - ?
    '''

class TelegramClient:
    def __init__(self, telegram_bot_token, chat_manager):
        self.bot = telebot.TeleBot(telegram_bot_token)
        self.chat_manager = chat_manager

        # Register handlers
        self.bot.message_handler(commands=['ey mane', 'start', 'help'])(self.send_init_message)
        self.bot.message_handler(content_types=['text'])(self.handle_message)

    def send_init_message(self): 
        send_telegram_message(HELP_MESSAGE)

    def send_telegram_message(self, msg):
        if msg.length > TEXT_CHAR_LIMIT:
            # Split characters if needed
            texts = util.split_string(msg, 3000)
        else: texts = [msg]

        for text in texts:
            telegram_bot.send_message(chat_id, text)

    def handle_message(self, msg):
        print(msg) # Dev Support: View raw message
        user_text = msg.text
        bot_response = self.chat_manager.get_response(user_text)
        # self.bot.reply_to(msg, bot_response)
        self.send_telegram_message(bot_response) 

    def run_bot(self):
        self.bot.polling(none_stop=True)
        print("Telegram Client Running...") # Dev Support: View raw message