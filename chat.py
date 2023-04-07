import os
import openai

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

MODEL="gpt-3.5-turbo" # "gpt-4"
SYSTEM_PROMPT = "You are a helpful assistant focused on providing as much detail and context on topics as possible."

OPENAI_API_KEY_FILEPATH = "..\openai_api_key.txt"
OPENAI_API_KEY = ""

# Get API Key
with open(OPENAI_API_KEY_FILEPATH) as f:
    OPENAI_API_KEY = f.readlines()[0]
openai.api_key = OPENAI_API_KEY
# print(openai.Model.list()) # Display list of models

message_history = [
# On roles:
    # System messages set the initial assistant behavior. Default is "You are a helpful assistant." 
    # User Messages help instruct the assistent, and can be set by the developer as an instruction
    # Assistant messages store prior responses and can give examples of desired behavior
]

def submitCompletionMessage(role='', content=''):
    '''Submits current message history to the model after updating with provide message'''
    if role != '' and content != '':
        updateMessageHistory(role, content)
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages = message_history
    )
    return response

def updateMessageHistory(role, content): 
    '''Creates a new message object in the message_history list'''
    global message_history
    message_history += [{"role": role, "content": content}] 

def parseResponse(resp):
    '''Parses openai response for role and content, then appends that to the message history and passes those values as output'''
    role, content = resp['choices'][0]['message']['role'], resp['choices'][0]['message']['content']
    updateMessageHistory(role, content)
    return role, content

def showResponseContent(resp, showRaw=False):
    '''Shows response content with model label in chat format or as raw if showRaw is set to True'''
    role, content = parseResponse(resp)
    if showRaw == True:
        print(f"{MODEL} raw response:\n {resp}")
    else:
        print(f"{MODEL}:\n {content}")
    
def chat():  
    '''Chat loop'''

    # Populate initial prompt(s)
    updateMessageHistory("system", SYSTEM_PROMPT)
    # updateMessageHistory("user", "USER_PROMPT")
    # updateMessageHistory("assistant", ASSISTANT_PROMPT)

    # Submit initial message history
    showResponseContent(submitCompletionMessage())
    
    user_prompt = "\nEnter the word 'hist' to view history. Enter 'exit' to exit. Enter '?' if you want me to repeat myself." 
    print(user_prompt)
    while(True):
    # User input loop
        user_input = input("user: ")
        if user_input == "exit": break
        elif user_input == "hist": 
                for item in message_history:
                    print(f"role: {item['role']}\ncontent: {item['content']}")
        elif user_input == "help" or user_input == "?": print(user_prompt)
        else: 
            # Submit input to gpt
            showResponseContent(submitCompletionMessage("user", user_input))
        user_input=""

if __name__ == "__main__":
    chat()

