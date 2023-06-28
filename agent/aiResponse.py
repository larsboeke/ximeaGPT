import Functions
import openai
import os
import json
import backend.user_utils as usr
from datetime import datetime as dt

class Conversation:


    def __init__(self, conversation_id, user_prompt):
        
        self.conversation_id = conversation_id
        self.conversation_history = usr.get_past_messages(conversation_id)
        self.functions = Functions.tools
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0
        self.start_timestamp = dt.now()
    

        usr.add_message(conversation_id, 'user', user_prompt)


    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)


    def get_openai_response(self):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages= self.conversation_history,
                functions= self.functions,
                function_call="auto"
            )
            promt_tokens = response["usage"]["prompt_tokens"]
            completion_tokens = response["usage"]["completion_tokens"]

            self.prompt_tokens += promt_tokens
            self.completion_tokens += completion_tokens

        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
        
        return response["choices"][0]["message"]

    def chat_completion_request(self, prompt):
        self.add_message("user", prompt)
        
        message = self.get_openai_response()
    
        check_function_call = message.get("function_call")
           
        while check_function_call:

            json_str = message["function_call"]["arguments"]
            data = json.loads(json_str)

            function_name = message["function_call"]["name"]

            if function_name == "get_context_tool":
                print("Using get-context tool...")
                function_response, tokens = Functions.getText(
                    query = data["query"],
                    namespace="pastConversations"
                )
                self.embeddings_tokens += tokens

            elif function_name == "query_manuals":
                print("Using query_manuals tool...")
                function_response, tokens = Functions.getText(
                    query = data["query"],
                    namespace="manuals"
                )
                self.embeddings_tokens += tokens
                print(function_response)

            elif function_name == "get_last_message":
                pass

            elif function_name == "query_product_database":
                pass

            self.add_function(function_name, str(function_response))
     
            additional_response = self.get_openai_response()
        
            additional_message = additional_response["choices"][0]["message"]
            print(additional_message["content"])
            self.add_message("assistant", str(additional_message["content"]))

            check_function_call = additional_message.get("function_call")
        
        
        usr.add_activity(self.embeddings_tokens, self.prompt_tokens, self.completion_tokens, self.start_timestamp, end_timestamp = dt.now())

    


test = Conversation("1234")

while True:
    prompt = input("Ask a question...")
    test.chat_completion_request(prompt)
    print(test.conversation_history[-1]["content"])
