from agent import Agent_functions
import openai
import os
import json
import backend.user_utils as usr
from datetime import datetime as dt
from backend import activity_utils as act

class AiResponse:


    def __init__(self, conversation_id, user_prompt):
        
        self.conversation_id = conversation_id
        self.conversation_history = usr.retrieve_conversation(conversation_id)
        self.functions = Agent_functions.tools
        self.user_prompt = user_prompt
        self.sources = []
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0
        self.start_timestamp = dt.now()
    


    def add_user_message(self, content):
        message = {"role": 'user', "content": content}
        self.conversation_history.append(message)
        usr.add_message(self.conversation_id, 'user', content)

    def add_assistant_message(self, content, sources):
        message = {"role": 'assistant', 'content': content}
        self.conversation_history.append(message)
        usr.add_assistant_message(self.conversation_id, content, sources)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)
        usr.add_function(self.conversation_id, function_name, content)


    def get_openai_response(self, call_type):
        max_attempts = 5
        x = 0
        while x < max_attempts:

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages= self.conversation_history,
                    functions= self.functions,
                    function_call=call_type,
                    temperature = 0
                )
                promt_tokens = response["usage"]["prompt_tokens"]
                completion_tokens = response["usage"]["completion_tokens"]

                self.prompt_tokens += promt_tokens
                self.completion_tokens += completion_tokens

                return response["choices"][0]["message"]

            except Exception as e:
                print("Unable to generate ChatCompletion response")
                print(f"Exception: {e}")
                
        
        

    def chat_completion_request(self):
        
        self.add_user_message(self.user_prompt)
        
        message = self.get_openai_response("auto")
    
        check_function_call = message.get("function_call")
        message['timestamp'] = str(dt.now())

        assistant_message = message['content']
        if not check_function_call:
            self.add_assistant_message(message['content'], [])

        function_call_counter = 0
        function_call_limit = 1
        query_counter = 1

        while function_call_counter < function_call_limit and check_function_call:  
 
            json_str = message["function_call"]["arguments"]
            data = json.loads(json_str)
            function_name = message["function_call"]["name"]

            if function_name == "query_unstructured_data":
                print("Using query_unstructured_data tool...")
                function_response, sources, tokens = Agent_functions.getText(
                    query=data["query"],
                    counter = query_counter
                )
                # append sources to sources attribute
                for source in sources:
                    self.sources.append(source)
                # app used tokens
                self.embeddings_tokens += tokens
                query_counter += 1
                print(function_response)

            elif function_name == "query_feature_of_product_pdb":
                print("Using query_feature_of_product_pdb tool...")
                function_response, sources = Agent_functions.query_feature_of_product_pdb( # Eventually add sources!
                    product = data["product"]
                )
                for source in sources:
                    self.sources.append(source)
                print(function_response)
            elif function_name == "query_data_of_feature_of_product_pdb":
                print("Using query_data_of_feature_of_product_pdb tool...")
                function_response, sources = Agent_functions.query_data_of_feature_of_product_pdb( # Eventually add sources!
                    product=data["product"], feature=data["feature"], category=data["category"]
                )
                print(function_response)
                for source in sources:
                    self.sources.append(source)


            print(check_function_call)
            self.add_function(function_name, str(function_response))

            function_call_counter += 1

            #call response with functions if counter is lower than function call limit, otherwise force respose without functions
            if function_call_counter == function_call_limit:
                message_response_to_function = self.get_openai_response(call_type="none")
            
            elif function_call_counter < function_call_limit:
                message_response_to_function = self.get_openai_response(call_type="auto")
    
            
            assistant_message = message_response_to_function['content']
            self.add_assistant_message(assistant_message, self.sources)
      

        act.add_activity(self.embeddings_tokens, self.prompt_tokens, self.completion_tokens, self.start_timestamp, end_timestamp = dt.now())

        return assistant_message, self.sources
