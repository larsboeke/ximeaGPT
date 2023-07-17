import pymongo
import pinecone
import openai
import pymssql
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import tiktoken

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

def run_conversation(user_prompt):
    messages= {"role": "user", "content": user_prompt},
    functions = [
        {
            "name": "query_product_database",
            "description": "Get the result back from a valid transact-SQL query on XIMEAs Product-database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlquery": {
                        "type": "string",
                        "description": "Valid transact-SQL syntax, e.g. SELECT TOP (10) [id_product], [name_of_product], [description] FROM [AI:Lean].[dbo].[product]",
                    },
                },
                "required": ["sqlquery"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    print(response_message)
    second_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "function", "name": response_message["function_call"]["name"], "content": response_message["function_call"]["arguments"]}
        ],
        functions=functions,
        )
    print(second_completion)
    response = second_completion.choices[0].message.content
    print("111111111111111111111")

    return response





query_product_database = {
            "name": "query_product_database",
            "description": "Get the result back from a valid transact-SQL query on XIMEAs Product-database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlquery": {
                        "type": "string",
                        "description": "Valid transact-SQL syntax, e.g. SELECT TOP (10) [id_product], [name_of_product], [description] FROM [AI:Lean].[dbo].[product]",
                    },
                },
                "required": ["sqlquery"],
            },
        }

def query_product_database(sqlquery):
    print("Funtion called")
    print(str(sqlquery))
    connection, mycursor = create_connection()
    #sqlquery = sqlquery.function_call.arguments
    print(sqlquery)
    print("!1111111111111111111!")
    try:
        mycursor.execute(sqlquery)      #Excecute Query Check for Errors
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
        print("Error")
    else:
        myresult = mycursor.fetchall()
        print(str(myresult))


# def query_product_database(sqlquery):
#     print(str(sqlquery))
#     connection, mycursor = create_connection()
#     try:
#         mycursor.execute(sqlquery)      #Excecute Query Check for Errors
#     except:
#         myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
#     else:
#         myresult = mycursor.fetchall()
#         print(str(myresult))
#         print("Length from result!")
#         print(str(len(myresult)))
#         print("Length of tokens from result!")
#         print(str(num_tokens_from_string(str(myresult))))
#         if len(myresult)> 200:
#             myresult = "The query you wrote returned too much data for you to handle. Please LIMIT the amount of data you get returned or rewrite the query!"
#     query_info = {
#         "sqlquery": sqlquery,
#         "database_response": myresult
#     }
#     return query_info


def create_connection():
    server = '192.168.11.22'
    database = 'AI:Lean'
    username = 'AI:Lean'
    password = 'NbIxyuc5b!4'

    connection = pymssql.connect(server, username, password, database)
    cursor = connection.cursor()
    return connection, cursor

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

messages="Does the Camera xix feature 2x2-Binding?"

# print(run_conversation(messages))

def get_sql_query(user_prompt):
    context = """
    Context:
        As a context here is the structure of the database:

        CREATE TABLE feat (
            id INTEGER NOT NULL AUTO_INCREMENT, 
            name VARCHAR(45), 
            type INTEGER DEFAULT '1', 
            list_id INTEGER DEFAULT '0', 
            sub_type INTEGER DEFAULT '0', 
            gentl_name VARCHAR(145), 
            xiapi_name VARCHAR(145), 
            gentl_inv_feat_list VARCHAR(245), 
            id_featcateg INTEGER DEFAULT '0', 
            gentl_type VARCHAR(45), 
            gentl_tooltip VARCHAR(245), 
            gentl_description VARCHAR(245), 
            gentl_display_name VARCHAR(245), 
            gentl_access_mode VARCHAR(45), 
            gentl_visibility VARCHAR(45), 
            gentl_value VARCHAR(45), 
            gentl_representation VARCHAR(45), 
            gentl_max VARCHAR(245), 
            gentl_min VARCHAR(245), 
            gentl_inc VARCHAR(245), 
            gentl_length VARCHAR(45), 
            gentl_port VARCHAR(45), 
            gentl_sign VARCHAR(45), 
            gentl_endianess VARCHAR(45), 
            gentl_unit VARCHAR(45), 
            gentl_swiss_knife VARCHAR(45), 
            gentl_namespace VARCHAR(45), 
            gentl_command_value VARCHAR(45), 
            gentl_display_prec VARCHAR(45), 
            gentl_value_default VARCHAR(145), 
            gentl_pvalue VARCHAR(145), 
            gentl_pmax VARCHAR(145), 
            gentl_pmin VARCHAR(145), 
            gentl_streamable VARCHAR(145), 
            gentl_has_register VARCHAR(145), 
            gentl_generate_register VARCHAR(145), 
            gentl_handler_function VARCHAR(145), 
            subtable_cols VARCHAR(145), 
            u3v_en VARCHAR(145), 
            gentl_en VARCHAR(145), 
            gentl_avail_sk VARCHAR(145), 
            lock_while_acq VARCHAR(145), 
            cal_en VARCHAR(145), 
            cal_rtg VARCHAR(145), 
            xp_en VARCHAR(10), 
            xp_ext_en VARCHAR(145), 
            `pIsLocked` VARCHAR(145), 
            gentl_locked_sk VARCHAR(145), 
            app_def VARCHAR(145), 
            polling_time VARCHAR(145), 
            string_is_path VARCHAR(145), 
            supported_file_format VARCHAR(145), 
            web_link VARCHAR(145), 
            flags VARCHAR(145), 
            `pSelected` VARCHAR(245), 
            value_descr VARCHAR(245), 
            invalidates_all_params VARCHAR(145), 
            web_download_type INTEGER DEFAULT '0', 
        PRIMARY KEY (id)
        )ENGINE=InnoDB DEFAULT CHARSET=latin1

        CREATE TABLE product_feature_relationship (
                id INTEGER NOT NULL AUTO_INCREMENT, 
                id_feat INTEGER, 
                id_product INTEGER, 
                PRIMARY KEY (id), 
                CONSTRAINT product_feature_relationship_ibfk_1 FOREIGN KEY(id_product) REFERENCES prod (id), 
                CONSTRAINT product_feature_relationship_ibfk_2 FOREIGN KEY(id_feat) REFERENCES feat (id)
        )ENGINE=InnoDB DEFAULT CHARSET=latin1

        CREATE TABLE prod (
            id INTEGER NOT NULL AUTO_INCREMENT, 
            name VARCHAR(145), 
            type INTEGER DEFAULT '1', 
            sub_type INTEGER NOT NULL DEFAULT '0', 
            description VARCHAR(500), 
            PRIMARY KEY (id)
        )ENGINE=InnoDB DEFAULT CHARSET=latin1
         """
    
    messages=[
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": f"Your are a helpfull assistent who will take a the user prompt and turn it into a transact-SQL query. Only give back the query there is no need to execute it. To help you here is the structure of my database: {context}. The output could for example look like this: SELECT TOP (10) [id_product], [name_of_product], [description] FROM [AI:Lean].[dbo].[product]"}
    ]
    
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )
    return response#["choices"][0]["message"]

query = "What features does the xiB-64 camera have?"
#print(get_sql_query(query))

query = "SELECT feat.* \nFROM feat \nJOIN product_feature_relationship ON feat.id = product_feature_relationship.id_feat \nJOIN prod ON product_feature_relationship.id_product = prod.id \nWHERE prod.name = 'xiB-64';"

query_product_database(query)