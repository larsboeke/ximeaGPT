from agent.Agent_functions import AgentFunctions
import openai
import json
import backend.user_utils as usr
from datetime import datetime as dt
from backend import activity_utils as act
from data_package.Token_Counter.TokenCounter import TokenCounter


class AiResponse:
    def __init__(self, conversation_id, user_prompt):
        self.AgentFunction = AgentFunctions()
        self.conversation_id = conversation_id
        self.conversation_history = usr.retrieve_conversation(conversation_id)
        self.functions = self.AgentFunction.get_tools()
        self.user_prompt = user_prompt
        self.sources = []
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.embeddings_tokens = 0
        self.start_timestamp = dt.now()

    def add_user_message(self, content):
        message = {"role": "user", "content": content}
        self.conversation_history.append(message)
        usr.add_message(self.conversation_id, "user", content)

    def add_assistant_message(self, content, sources):
        message = {"role": "assistant", "content": content}
        self.conversation_history.append(message)
        usr.add_assistant_message(self.conversation_id, content, sources)

    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": content}
        self.conversation_history.append(message)
        usr.add_function(self.conversation_id, function_name, content)

    def drop_message(self):
        # self.conversation_history.pop(1)
        usr.drop_message(self.conversation_id)  # is just null not really deleted

    def get_openai_response(self, call_type):
        max_attempts = 5
        x = 0
        while x < max_attempts:
            x += 1
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=self.conversation_history,
                    functions=self.functions,
                    function_call=call_type,
                    temperature=0.3,
                )
                prompt_tokens = response["usage"]["prompt_tokens"]
                completion_tokens = response["usage"]["completion_tokens"]

                self.prompt_tokens += prompt_tokens
                self.completion_tokens += completion_tokens

                return response["choices"][0]["message"]

            except Exception as e:
                print("Unable to generate ChatCompletion response")
                print(f"Exception: {e}")

    def check_history_length(self):
        conv_his_token = TokenCounter().num_tokens_from_string(
            str(self.conversation_history), "cl100k_base"
        )
        while conv_his_token > 6000:
            self.conversation_history.pop(1)
            self.conversation_history.pop(1)
            self.drop_message()
            conv_his_token = TokenCounter().num_tokens_from_string(
                str(self.conversation_history), "cl100k_base"
            )
            print("Dropped two")

    def chat_completion_request(self):
        try:
            self.check_history_length()

            self.add_user_message(self.user_prompt)

            message = self.get_openai_response("auto")

            check_function_call = message.get("function_call")
            message["timestamp"] = str(dt.now())

            assistant_message = message["content"]
            if not check_function_call:
                self.add_assistant_message(message["content"], [])

            if check_function_call:
                json_str = message["function_call"]["arguments"]
                data = json.loads(json_str)
                print("Data aus Function call:", data)
                function_name = message["function_call"]["name"]

                response_dictionary = {}

                if function_name == "query_all_sources":
                    print("Using new superior tool ...")
                    print("User promt: ", self.user_prompt)
                    if "query" in data:
                        print("First getting the Unstructured data!")
                        namespaces = [("manuals", 2), ("tickets", 1), ("emails", 1)]
                        function_response, sources, tokens = self.AgentFunction.get_sources(
                            query=data["query"],
                            namespaces=namespaces,
                        )
                        print("Then the Structured data!")
                        function_response_sql, sources_sql, prompt_tokens, completion_tokens = self.AgentFunction.use_product_database(
                            feature_list=data.get("features"),
                            message_history=self.conversation_history,
                        )

                        function_response.append(function_response_sql)

                        for source in sources:
                            self.sources.append(source)
                            extra_source = self.AgentFunction.get_extra_sources(source)
                            if extra_source:
                                self.sources.append(extra_source)

                        self.sources.append(sources_sql[0])

                        # app used tokens
                        self.embeddings_tokens += tokens
                        self.prompt_tokens += prompt_tokens
                        self.completion_tokens += completion_tokens

                        response_dictionary["unstructured_data_response"] = function_response

                if function_name == "query_emails_and_tickets":
                    if "query" in data:
                        print("Getting email and ticket sources!")
                        namespaces = [("tickets", 2), ("emails", 2)]
                        function_response, sources, tokens = self.AgentFunction.get_sources(
                            query=data["query"], 
                            namespaces=namespaces
                        )
                        for source in sources:
                            self.sources.append(source)
                            extra_source = self.AgentFunction.get_extra_sources(source)
                            if extra_source:
                                self.sources.append(extra_source)
                        # app used tokens
                        self.embeddings_tokens += tokens
                        response_dictionary["ticket_email_data_response"] = function_response

                if function_name == "query_manuals":
                    if "query" in data:
                        print("Getting manual sources!")
                        namespaces = [("manuals", 4)]
                        function_response, sources, tokens = self.AgentFunction.get_sources(
                            query=data["query"], 
                            namespaces=namespaces,
                        )

                        for source in sources:
                            self.sources.append(source)
                        # app used tokens
                        self.embeddings_tokens += tokens
                        response_dictionary["manual_data_response"] = function_response

                if function_name == "use_product_database":
                    print("Using use_product_database tool...")
                    function_response, sources, prompt_tokens, completion_tokens = self.AgentFunction.use_product_database(
                        feature_list=data.get("features"),
                        message_history=self.conversation_history,
                        prompt_tokens=self.prompt_tokens,
                        completion_tokens=self.completion_tokens,
                        )
                    
                    self.prompt_tokens += prompt_tokens
                    self.completion_tokens += completion_tokens
                    for source in sources:
                        self.sources.append(source)

                    response_dictionary["sql_data_response"] = function_response

                # Add the Sources to the History
                response_dictionary_str = json.dumps(response_dictionary)
                self.add_function(function_name, response_dictionary_str)

                message_response_to_function = self.get_openai_response(call_type="none")

                assistant_message = message_response_to_function["content"]
                self.add_assistant_message(assistant_message, self.sources)

            print(f"Conversation History ------------------------------------------------ \n {self.conversation_history}")
            print(f"prompt_tokens {self.prompt_tokens} , completion_tokens {self.completion_tokens} , embeddings_tokens {self.embeddings_tokens}")
            print(f"his_tokens {TokenCounter().num_tokens_from_string(str(self.conversation_history), 'cl100k_base')}")

            act.add_activity(
                self.embeddings_tokens,
                self.prompt_tokens,
                self.completion_tokens,
                self.start_timestamp,
                end_timestamp=dt.now(),
            )

            return assistant_message, self.sources

        except Exception as e:
            print(e)
            return "An Error occured, try again", self.sources
