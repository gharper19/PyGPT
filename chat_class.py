import os
from datetime import datetime
import logging
import pprint

import openai
# import tiktoken


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
OPENAI_API_KEY_FILEPATH = "../openai_api_key.txt"

logging.basicConfig(
    format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]',
    level=logging.INFO
)

class ChatCompletionBot:
    def __init__(
            self, 
            OPENAI_API_KEY="",
            MODEL="gpt-3.5-turbo" #"gtp-4"
            SYSTEM_PROMPTS= [ # Set initial assistant behavior
            "You are a helpful assistant focused on providing as much detail and context on topics as possible."
            ],

            ):
        
        
        self.MODEL = MODEL
        self.SYSTEM_PROMPTS = SYSTEM_PROMPTS
        
        # Set API key
        if OPENAI_API_KEY == "":
            with open(OPENAI_API_KEY_FILEPATH) as f:
                OPENAI_API_KEY = f.readlines()[0]
            if OPENAI_API_KEY == "": raise ValueError(f"No value found for OpenAI API Key at: {OPENAI_API_KEY_FILEPATH}")
        openai.api_key = OPENAI_API_KEY

        self.message_history = [
            # System messages set the initial assistant behavior. Default is "You are a helpful assistant." 
            # User Messages help instruct the assistent, and can be set by the developer as an instruction
            # Assistant messages store prior responses and can give examples of desired behavior
        ]

        for msg in SYSTEM_PROMPTS:
            # Upate message history with initial system messages
            updateMessageHistory(role="system", content: msg)

    def updateMessageHistory(self, message_history=[], role="", content="", overwrite=False):
        '''Updates bot message history with provided list of {role, content} entries, appends by default. Adds additional entry on the end if role and content are provided. '''
        global message_history
        
        # Add or overwrite message history entries
        if len(message_history) > 0:
            if overwrite: self.message_history = message_history
            else: self.message_history += message_history
        
        # Append additional entry
        if role != "" and content != "": 
            self.message_history += [{"role": role, "content": content}] 

    def submitCompletionMessage(self, role='', content=''):
        '''Submits current message history for completion by gpt. Appends additional message if role is provided.'''
        # Update message history with new message
        if role != '':
            self.updateMessageHistory(role, content)
        
        # Request completion and return response
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=self.message_history
        )
        return response

    def parseCompletionResponse(self, resp):
        '''Parses openai response for role and content and returns as output'''
        # Parse role and content
        role, content = 
            resp['choices'][0]['message']['role'], 
            resp['choices'][0]['message']['content']
        return role, content

    def sendMessage(self, role, content, updateHistory=True, rawResponse=False):
        '''Submits new message along with current message history, parses api response for role and content and returns as output'''
        # Submit new message and get response
        response= self.submitCompletionMessage(role, content)
        role, content = self.parseCompletionResponse(response)

        # Update message history
        if updateHistory: self.updateMessageHistory(role, content)
        
        # Return response content
        if rawResponse: return response
        else: return role, content

    def getMessageHistory(self, format=False):
        if format: 
            return self.message_history
        else:
            return self.message_history

    def exportMessageHistory(self, filename="", filetype="txt", format=False, prependTimestamp="%Y-%m-%d_%H-%M-%S"):
        '''Exports current message history to file. Uses timestamp if no name is provided.'''
        # Set filename
        if filename == "": 
            filename=f"{datetime.now().strftime(prependTimestamp)}_{self.MODEL}_msg-log.{filetype}"
        else if prependTimestamp: 
            filename=f"{datetime.now().strftime(prependTimestamp)}_{filename}.{filetype}"
        else: filename=f"{filename}.{filetype}"

        # Write message history to file
        with open(filename, "r+") as exportFile: 
            try
                if format:
                    exportFile.writelines(getMessageHistory(format=True))
                else: 
                    exportFile.writelines(getMessageHistory)
                result= f"Successfully exported message history to {filename}"
                logging.INFO(result)
            catch(Exception e):
                result = f"Export to '{filename}' failed: {e}"
                logging.ERROR(result)
        return result

    def runChatLoop(self):
        # Submit initial message history
        self.showResponseContent(self.submitCompletionMessage())

        # Prompt user for input
        user_prompt = "\nEnter the word 'hist' to view history. Enter 'exit' to exit. Enter '?' for commands help."
        print(user_prompt)

        # Run chat loop
        while True:
            user_input = input("user: ")
            if user_input == "exit":
                break
            elif user_input == "hist":
                for item in self.message_history:
                    print(f"role: {item['role']}\ncontent: {item['content']}")
            elif user_input == "help" or user_input == "?":
                print(user_prompt)
            else:
                self.showResponseContent(self.submitCompletionMessage("user", user_input))
                user_input = ""

if __name__ == "__main__":
    bot = ChatCompletionBot()
    bot.runChatLoop()

