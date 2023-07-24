from agent import Agent_functions
import openai
import os
import json
#import backend.user_utils as usr
from datetime import datetime as dt
#from backend import activity_utils as act
import tiktoken

class AiResponse_test:


    def __init__(self, conversation_id, user_prompt):

        self.conversation_id = conversation_id
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant to the customer support in the Company XIMEA. Base your Answers as much as possible on information gathered by the functions."}] 
        self.functions = Agent_functions.tools
        self.user_prompt = user_prompt
        self.sources = []
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0
        self.conversation_history_token = 0
        self.start_timestamp = dt.now()

    
    def add_user_prompt(self, content):
        self.user_prompt = content

    def add_user_message(self, content):
        message = {"role": 'user', "content": content}
        self.conversation_history.append(message)
        #usr.add_message(self.conversation_id, 'user', content)

    def add_assistant_message(self, content, sources):
        message = {"role": 'assistant', 'content': content}
        self.conversation_history.append(message)
        #usr.add_assistant_message(self.conversation_id, content, sources)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)
        #usr.add_function(self.conversation_id, function_name, content)


    def get_openai_response(self, call_type):
        #print("conversation history")
        #print(str(self.conversation_history))
        #print("history ende")
        max_attempts = 5
        x = 0
        while x < max_attempts:

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
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
                
        
    def handlefunctions(self,data,function_name):
        if function_name == "query_unstructured_data":
            print("Using query_unstructured_data tool...")
            print("this is the query CHatGPT used for Embedding search!")
            print(str(data["query"]))
            function_response, sources, tokens = Agent_functions.getText(
                query=data["query"],
                counter = 0
            )
            # append sources to sources attribute
            for source in sources:
                self.sources.append(source)
            # app used tokens
            self.embeddings_tokens += tokens
            #query_counter += 1
            print(function_response)
        elif function_name == "use_product_database":
            print("Using use_product_database tool...")
            function_response, sources = Agent_functions.query_product_database_with2function_call( 
                user_question= data.get("user_question"),
                feature_list= data.get("features"),
                message_history=self.conversation_history
            )
            for source in sources:
                self.sources.append(source)
            print(function_response)            
        elif function_name == "query_feature_of_product_pdb":
            print("Using query_feature_of_product_pdb tool...")
            function_response, sources = Agent_functions.query_feature_of_product_pdb( 
                product = data["product"]
            )
            for source in sources:
                self.sources.append(source)
            print(function_response)

        elif function_name == "use_structured_data":
            print("Using use_structured_data tool...")
            function_response, sources = Agent_functions.use_structured_data( 
                query = data.get("query"),
                feature_list= data.get("features")
            )
            for source in sources:
                self.sources.append(source)
            print(function_response)
        
        elif function_name == "query_data_of_feature_of_product_pdb":
            print("Using query_data_of_feature_of_product_pdb tool...")
            function_response, sources = Agent_functions.query_data_of_feature_of_product_pdb( 
                product=data["product"], feature=data["feature"]
            )
            print(function_response)
            for source in sources:
                self.sources.append(source)

        elif function_name == "query_pdb":
            print("Using query_pdb tool...")
            
            function_response, sources = Agent_functions.query_pdb( 
                query=data.get("query")
            )
            print(function_response)
            for source in sources:
                self.sources.append(source)

        elif function_name == "get_correct_features":
            print("Using get_correct_features tool...")
            print(str(data.get("features")))
            function_response, sources = Agent_functions.get_correct_features( 
                feature_list=data.get("features")
            )
            print(function_response)
            #for source in sources:
            #    self.sources.append(source)
        return function_response

    def chat_completion_request(self):
        # try:
        
        self.add_user_message(self.user_prompt)
        
        message = self.get_openai_response("auto")
        print(str(message))
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

            function_response= self.handlefunctions(data,function_name)

            #print(check_function_call)
            self.add_function(function_name, str(function_response))

            function_call_counter += 1

            #call response with functions if counter is lower than function call limit, otherwise force respose without functions
            if function_call_counter == function_call_limit:
                message_response_to_function = self.get_openai_response(call_type="none")
            
            elif function_call_counter < function_call_limit:
                message_response_to_function = self.get_openai_response(call_type="auto")
    
            check_function_call = message_response_to_function.get("function_call")
            if check_function_call == None:
                assistant_message = message_response_to_function['content']
                self.add_assistant_message(assistant_message, self.sources)
            else:
                message = message_response_to_function
            
            
            

        return assistant_message, self.sources
        # except Exception as e:
        #     print(e)
        #     return "An Error occured, try again", self.sources

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens