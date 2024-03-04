import os
from dotenv import load_dotenv
import logging
from chat_manager import ChatManager
from telegram_client import TelegramClient

'''
    # OpenAI API Python Library Reference: https://pypi.org/project/openai/
    
    # TODO:
    - Count tokens and track montly costs
    - Save conversation history
    - User interface

    # Using other completion models
        ## create a completion
        completion = openai.Completion.create(model="ada", prompt="Hello world")

        ## print the completion
        print(completion.choices[0].text)
'''

# # Generate logger
# logging.basicConfig(
#     format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]',
#     level=logging.INFO
# )


def main():
    # Load environment variables
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # Create a ChatManager instance
    chat_manager = ChatManager(OPENAI_API_KEY)

    # Create the TelegramApiClient and start the bot
    telegram_client = TelegramClient(TELEGRAM_BOT_TOKEN, chat_manager)
    telegram_client.run_bot()

if __name__ == "__main__":
    main()
