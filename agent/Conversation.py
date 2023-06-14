import Functions
import openai
import os
import json

def get_past_conversation():
    pass

class Conversation:


    def __init__(self, conversation_id):
        
        self.conversation_id = conversation_id
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant, helping out the customer support in the Company XIMEA. Base your Answers as much as possible on information gathered by the functions."}]
        self.functions = Functions.tools
        self.completion_tokens = 0
        self.embeddings_tokens = 0

        past_conversation = get_past_conversation(self.conversation_id)
        self.conversation_history.append(past_conversation)

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)


    def chat_completion_request(self, prompt):
        self.add_message("user", prompt)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages= self.conversation_history,
                functions= self.functions,
                function_call="auto"
            )
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
        
        message = response["choices"][0]["message"]
    
        check_function_call = message.get("function_call")
           
        while check_function_call:
            function_name = message["function_call"]["name"]

            if function_name == "get_context_tool":
                function_response = Functions.getText(
                    query = message.get("query"),
                    namespace="pastConversations"
                )

            elif function_name == "query_manuals":
                function_response = Functions.getText(
                    query = message.get("query"),
                    namespace="manuals"
                )

            elif function_name == "get_last_message":
                pass

            elif function_name == "query_product_database":
                pass

            self.add_message("function", function_name, function_response)
     

            try:
                additional_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages= self.conversation_history,
                    functions= self.functions,
                    function_call="auto"
                )
            except Exception as e:
                print("Unable to generate ChatCompletion response")
                print(f"Exception: {e}")
                return e
        
            additional_message = additional_response["choices"][0]["message"]
    
            check_function_call = additional_message.get("function_call")

        