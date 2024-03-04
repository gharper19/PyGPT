import openai

class OpenAIApiClient:
    def __init__(self, api_key, default_model="gpt-3.5-turbo", default_max_tokens=150):
        openai.api_key = api_key
        self.model = default_model
        self.max_tokens = default_max_tokens

    def set_model(self, model):
        self.model = model

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens

    def send_prompt(self, prompt_text):
        ''' Accepts conversation history as prompt '''
        response = openai.ChatCompletion.create(
            engine=self.model,
            prompt=prompt_text,
            max_tokens=self.max_tokens
        )
        return response