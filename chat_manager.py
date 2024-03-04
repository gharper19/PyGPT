import os
from datetime import datetime
from openai_api_client import OpenAIApiClient
# import tiktoken


class ChatManager:
    def __init__(self, api_key):
        self.conversation_history = []
        self.openai_api_client = OpenAIApiClient(api_key)

    def add_message(self, role, content):
        ''' Adds message to conversation history. User can be system, assistant, or user '''
        self.conversation_history.append({"role": role, "content": content})

    def get_prompt(self):
        ''' Collects conversation history into prompt text '''
        prompt = ""
        for user, message in self.conversation_history:
            prompt += f"{user}: {message}\n"
        return prompt

    def get_response(self, user_message, raw_response=False):
        self.add_message("user", user_message)
        response = self.openai_api_client.send_prompt(self.conversation_history)
    
        if raw_response: 
            self.add_message("assistant", response.choices[0].text)
            return response
        else: response = response.choices[0].text
        self.add_message("assistant", response)
        return response

    def export_conversation(self, format='txt'):
        # Implement the logic to export the conversation in the desired format
        pass

    def set_model(self, model):
        self.openai_api_client.set_model(model)

    def set_max_tokens(self, max_tokens):
        self.openai_api_client.set_max_tokens(max_tokens)
