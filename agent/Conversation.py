import Functions
import openai
import os
import json

def get_past_conversation(conversation_id):
    return None

class Conversation:


    def __init__(self, conversation_id):
        
        self.conversation_id = conversation_id
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant, helping out the customer support in the Company XIMEA. Base your Answers as much as possible on information gathered by the functions."}]
        self.functions = Functions.tools
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0

        past_conversation = get_past_conversation(self.conversation_id)
        if not past_conversation == None:
        
            self.conversation_history.append(past_conversation)

        print(self.conversation_history)

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)

    def add_promt_tokens(self, tokens):
        self.prompt_tokens += tokens

    def add_completion_tokens(self, tokens):
        self.completion_tokens += tokens

    def add_embedding_tokens(self, tokens):
        self.embeddings_tokens += tokens

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

            self.add_promt_tokens += promt_tokens
            self.add_completion_tokens += completion_tokens

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
                function_response = Functions.getText(
                    query = data["query"],
                    namespace="pastConversations"
                )
                self.add_embedding_tokens(tokens)

            elif function_name == "query_manuals":
                print("Using query_manuals tool...")
                function_response, tokens = Functions.getText(
                    query = data["query"],
                    namespace="manuals"
                )
                self.add_embedding_tokens(tokens)
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

    


test = Conversation("1234")

while True:
    prompt = input("Ask a question...")
    test.chat_completion_request(prompt)
    print(test.conversation_history[-1]["content"])
