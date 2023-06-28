import Functions
import openai
import os
import json
import backend.user_utils as usr
from datetime import datetime as dt

class AiResponse:


    def __init__(self, conversation_id, user_prompt, timestamp):
        
        self.conversation_id = conversation_id
        self.conversation_history = usr.retrieve_conversation(conversation_id)
        self.functions = Functions.tools
        self.user_prompt = user_prompt
        self.sources = []
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0
        self.start_timestamp = timestamp
    

 


    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        usr.add_message(self.conversation_id, role, content)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)
        usr.add_function(self.conversation_id, function_name, content)


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

    def chat_completion_request(self):
        usr.add_message(self.conversation_id, 'user', self.user_prompt)
        self.add_message("user", self.user_prompt)
        
        message = self.get_openai_response()
    
        check_function_call = message.get("function_call")

        if not check_function_call:
            self.add_message('assistant', message['content'])
           
        while check_function_call:

            json_str = message["function_call"]["arguments"]
            data = json.loads(json_str)

            function_name = message["function_call"]["name"]

            if function_name == "get_context_tool":
                print("Using get-context tool...")
                function_response, sources, tokens = Functions.getText(
                    query = data["query"],
                    namespace="pastConversations"
                )
                #append sources to sources attribute
                for source in sources:
                    self.sources.append(source)
                #app used tokens
                self.embeddings_tokens += tokens

            elif function_name == "query_manuals":
                print("Using query_manuals tool...")
                function_response, sources, tokens = Functions.getText(
                    query = data["query"],
                    namespace="manuals"
                )
                #append sources to sources attribute
                for source in sources:
                    self.sources.append(source)
                #app used tokens
                self.embeddings_tokens += tokens
                print(function_response)

            elif function_name == "get_last_message":
                pass

            elif function_name == "get_database_schema":
                print("Using get_database_schema tool...")
                function_response = Functions.get_database_schema()

            elif function_name == "query_product_database":
                pass

            self.add_function(function_name, str(function_response))
     
            additional_message = self.get_openai_response()
            check_function_call = additional_message.get("function_call")

            #add assistant messgae if no further function call is required
            if not check_function_call:
                assistant_message = additional_message['content']
                self.add_message('assistant', assistant_message)
                usr.add_message(self.conversation_id, 'assistant', assistant_message)
            
            
            self.add_message("assistant", str(additional_message["content"]))
            print(additional_message["content"])
            additional_message['timestamp'] = dt.now()

        
        
        usr.add_activity(self.embeddings_tokens, self.prompt_tokens, self.completion_tokens, self.start_timestamp, end_timestamp = dt.now())

        return additional_message, self.sources
    


