import pymongo
import pinecone
import openai
import pymssql
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import tiktoken
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider
import html
import json


load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

query_all_sources = {
                "name": "query_all_sources",
                "description": "This tool is the most general tool you can use. It provides infomation form all data sources of the company, namely support tickets and emails, technical manuals and the product database. This tool is best to use if all of these data sources provide good information. Also use this tool if you are unsure which other tool to use!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "This is equal to the whole query of the user!",
                        },
                         "product" : {
                            "type": "string",
                            "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP.",
                        },
                        "feature" : {
                            "type": "string",
                            "description": "This is the feature of which we want to know specific information. Features in the database are for example: TriggerMode, LUTValue, xiAPI Loopback Trigger Support, xiapi_UsedFFSSize.",
                        },
                    },
                    "required": ["query"],
                },
            }

query_emails_and_tickets = {
                "name": "query_emails_and_tickets",
                "description": "This tool answers the users query only with information of from the support eamils and tickets of XIMEA. Therefore use cases for this tool are when the user asks for the email or ticket history for a case. This tool provides infomation about things that typically get negotiated in emails or tickets, like contract datails ... ONLY USE THIS TOOL IF emails and tickest are the best source for answering the user query. Keep in mind that data from technical manuals is not included!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to find similar contexts to. Stay close to the user query and do not shorten much!",
                        },
                    },
                    "required": ["query"],
                },
            }


query_manuals = {
                "name": "query_manuals",
                "description": "This tool answers the users query only with information of the technical manaul. Therefore it is good to use it when there are questions concerning the technical parts of a camera/ camera family of ximea! ONLY use this tool if the technical manual is the best source for answering the user's quer. Keep in mind that information from the support tickets and emails is not included!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to gather technical information about. Stay close to the user query and do not shorten much!",
                        },
                    },
                    "required": ["query"],
                },
            }
query_product_database_with2function_call ={
            "name": "use_product_database",
                "description": "This function can be used to write a SQL query with the correct feature names on the XIMEA SQL Database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features":{
                            "type": "array",
                             "description": "An array of strings to pass to the function for getting the corresponding Feature names back, e.g. ['Resolution', 'OffsetX']. Only use it when you are given a Feature!",
                             "items": {
                                 "type": "string"
                             }

                        },
                        "user_question": {
                            "type": "string",
                            "description": "Place the question the user asked you right here!",
                        },
                    },
                     "required": ["user_question"],
                }
}                   

"""
query_all = {
                "name": "query_unstructured_data",
                "description": "Query unstructed data to get context from past conversations with customers and technical manuals. The data store information about camera families and their specifications. This function should be used most often",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to find similar contexts to",
                        },
                    },
                    "required": ["query"],
                },
            }

# Fucntions for the PDB
query_feature_of_product_pdb = {
                "name": "query_feature_of_product_pdb",
                "description": "Query for the features of a specific product in XIMEA'S product database (PDB). Use this function if you want to check for features of a product or if you want to list features of a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                    },
                    "required": ["product"],
                },
            }

# query_data_of_category_feature_of_product_pdb = {
#                 "name": "query_data_of_category_feature_of_product_pdb",
#                 "description": "Query for the data of a category of a specific feature of a product in XIMEA'S product database",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "product" : {
#                             "type": "string",
#                             "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
#                         },
#                         "feature" : {
#                             "type": "string",
#                             "description": "This is the feature of which we want to know specific information. Features in the database are for example: TriggerMode, LUTValue, xiAPI Loopback Trigger Support, xiapi_UsedFFSSize",
#                         },
#                         "category" : {
#                             "type": "string",
#                             "description": "This is the catergory of information about the feature. The possible categories are: id_feature, name_of_feature, gentl_name, api_name, datatype, tooltip, description, display_name, access_mode, visibility_level, type_of_value, maximum_values, minimum_values, increment_values, length, port, signature, unit, namespace, command_value, default_value, gentl_pmax, gentl_pmin, streamable, register, generate_register, handler_function, available_sk, lock_while_acq, cal_en, cal_rtg, xp_en, xp_ext_en, app_def, polling_time, string_is_path, supported_file_format, web_link, flags, p_selected, value_description, invalidates_all_params, web_download_type",
#                         },
#                     },
#                     "required": ["product", "feature", "category"],
#                 },
#             }

query_data_of_feature_of_product_pdb = {
                "name": "query_data_of_feature_of_product_pdb",
                "description": "Query for specific information about a feature of a product in XIMEA'S product database (PDB).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                        "feature" : {
                            "type": "string",
                            "description": "This is the feature of which we want to know specific information. Features in the database are for example: TriggerMode, LUTValue, xiAPI Loopback Trigger Support, xiapi_UsedFFSSize.",
                        },
                    },
                    "required": ["product", "feature"],
                },
            }"""
query_pdb = {
            "name": "query_pdb",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                    
                },
                "required": ["query"],
            },
        }
local_functions = [ query_pdb,
        # {
        #     "name": "query_pdb",
        #     "description": "Get the current weather in a given location",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "query": {
        #                 "type": "string",
        #                 "description": "The city and state, e.g. San Francisco, CA",
        #             }
                    
        #         },
        #         "required": ["query"],
        #     },
        # }, #query_product_database_with2function_call,
    ]

tools = [
    query_all_sources,
    query_manuals,
    query_emails_and_tickets,
    #query_feature_of_product_pdb,
    #query_data_of_feature_of_product_pdb,
    # query_data_of_category_feature_of_product_pdb,
    query_product_database_with2function_call,
]


def query_product_database_with2function_call(user_question= None, feature_list = None, message_history = None):
    print("In function")
    if feature_list != None:
        feature_list = similar_embeddings(feature_list)
    print("past if statement")
    message = get_openai_sql_response(user_question, feature_list, message_history)
    print(str(message))

    print("past SQL response")
    json_str = message["function_call"]["arguments"]
    data = json.loads(json_str)

    function_response, sources = query_pdb(query=data.get("query"))
                    
    #print(str(message.get('content')))
    #query = message.get('content')
    #function_response, sources = query_pdb( query=query)
    print(str(function_response))
    return function_response, sources


def get_openai_sql_response(user_question, feature_list, message_history):
    max_attempts = 5
    x = 0
    database_schema = "TABLE product_database COLUMNS name_of_feature | name_of_camera | value_of_feature | unit | description_of_feature "
    if feature_list == None:
        message_history.append(
        {"role": "function", "name": "use_product_database", "content": f"NOW ONLY WRITE ONE TRANSACT-SQL QUERY to answer the user question. Do not use a WHERE clause. Use this table {database_schema}"})
    else:
        message_history.append(
        {"role": "function", "name": "use_product_database", "content": f"NOW ONLY WRITE ONE TRANSACT-SQL QUERY to answer the user question. Pick the matching name_of_feature from this List of features from our database: {feature_list} . Use this table {database_schema}"})

    

    
    while x < max_attempts:
        x += 1

        try:
            print(str(x))
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message_history,
                functions= local_functions,
                function_call={"name": "query_pdb"},
                temperature = 0,
)
            
            return response["choices"][0]["message"]

        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")

def similar_embeddings(OpenAIs_features):
    index = initPinecone()
    multiple_feature_possibility = []
    for feature in OpenAIs_features:
        feature_possibility = []
        score = 0
        highest_score= 0
        feature_embedding = openai.Embedding.create(input=feature, engine="text-embedding-ada-002")['data'][0]['embedding']
        pinecone_results = index.query([feature_embedding], top_k=3, include_metadata=True, namespace='name_of_sql_features')["matches"]
        feature_possibility.append(pinecone_results[0]['id'])
        feature_possibility.append(pinecone_results[1]['id'])
        feature_possibility.append(pinecone_results[2]['id'])
        multiple_feature_possibility.append(feature_possibility)
    return multiple_feature_possibility

def query_pdb(query):
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except Exception as e:
        myresult = "The query you wrote produced an error message." + str(e)
    else:
        myresult = mycursor.fetchall()
    if myresult == []:
        myresult =  "The query you wrote didn't contain data. Either there is no data for that question or you wrote a bad query!"
    if num_tokens_from_string(str(myresult))>6000:
        myresult =  "The query you wrote contains too much data for you to handle. Rewrite the SQL Query so that less data is returned!"
    matches_sources = []
    print("inside_pdb")
    #source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    #TODO: answers not correct
    source_answer = []
    for result_touple in myresult:
        touple_content = []
        for element in result_touple:
            touple_content.append(html.escape(element))
        source_answer.append(touple_content)
    print("past_for_loop")                         
    source = {'id': "1", 'content': f"Query: {query}, Result from PDB: {str(source_answer)}", 'metadata': {'type': "Product_Database"}}

    matches_sources.append(source)
    endresult = [query, myresult]
    return endresult, matches_sources

# def query_product_database(product, feature):
#     if feature == None:
#         query = f"""
#             SELECT f.name_of_feature
#             FROM [AI:Lean].[dbo].[feature] f 
#             INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
#             ON f.id_feature = pfr.id_feature 
#             INNER JOIN [AI:Lean].[dbo].[product] p 
#             ON pfr.id_product = p.id_product 
#             WHERE p.name_of_product = '{product}'
#             """
#     else:
#         query = f"""
#             SELECT *
#             FROM [AI:Lean].[dbo].[feature] f 
#             INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
#             ON f.id_feature = pfr.id_feature 
#             INNER JOIN [AI:Lean].[dbo].[product] p 
#             ON pfr.id_product = p.id_product 
#             WHERE p.name_of_product = '{product}' AND f.name_of_feature = '{feature}'
#             """
#     connection, mycursor = SQLConnectionProvider().create_connection()
#     try:
#         mycursor.execute(query)
#     except:
#         myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
#     else:
#         myresult = mycursor.fetchall()

#         print(str(myresult))
#     matches_sources = []
#     source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
#     matches_sources.append(source)
#     return myresult, matches_sources
    
def query_data_of_feature_of_product_pdb(product, feature):
    print(product)
    
    query = f"""
            SELECT *
            FROM [AI:Lean].[dbo].[feature] f 
            INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
            ON f.id_feature = pfr.id_feature 
            INNER JOIN [AI:Lean].[dbo].[product] p 
            ON pfr.id_product = p.id_product 
            WHERE p.name_of_product = '{product}' AND f.name_of_feature = '{feature}'
            """
    
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()
        
        if myresult == []:
            myresult = "No entry is found in the Product Data Base."
        else:
            categories = ("id_feature", "name_of_feature", "gentl_name", "api_name", "datatype", "tooltip", "description", "display_name", "access_mode", "visibility_level", "type_of_value", "maximum_values", "minimum_values", "increment_values", "length", "port", "signature", "unit", "namespace", "command_value", "default_value", "gentl_pmax", "gentl_pmin", "streamable", "register", "generate_register", "handler_function", "available_sk", "lock_while_acq", "cal_en", "cal_rtg", "xp_en", "xp_ext_en", "app_def", "polling_time", "string_is_path", "supported_file_format", "web_link", "flags", "p_selected", "value_description", "invalidates_all_params", "web_download_type", "id", "id_product", "id_feature", "id_product", "name_of_product", "description")
            if len(categories) == len(myresult[0]):
                myresult = {categories[i]: myresult[0][i] for i, _ in enumerate(myresult[0])}
        
        print(str(myresult))
    matches_sources = []
    source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    matches_sources.append(source)
    return myresult, matches_sources

# def query_data_of_category_feature_of_product_pdb(product, feature, category):
    # print(product)
    # query = f"""
    #         SELECT f.[{category}]
    #         FROM [AI:Lean].[dbo].[feature] f 
    #         INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
    #         ON f.id_feature = pfr.id_feature 
    #         INNER JOIN [AI:Lean].[dbo].[product] p 
    #         ON pfr.id_product = p.id_product 
    #         WHERE p.name_of_product = '{product}' AND f.name_of_feature = '{feature}'
    #         """
    # connection, mycursor = create_connection()
    # try:
    #     mycursor.execute(query)
    # except:
    #     myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    # else:
    #     myresult = mycursor.fetchall()
    #     print(str(myresult))
    # matches_sources = []
    # source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    # matches_sources.append(source)
    # return myresult, matches_sources


def query_feature_of_product_pdb(product):
    print(product)
    query = f"""
            SELECT f.name_of_feature
            FROM [AI:Lean].[dbo].[feature] f 
            INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
            ON f.id_feature = pfr.id_feature 
            INNER JOIN [AI:Lean].[dbo].[product] p 
            ON pfr.id_product = p.id_product 
            WHERE p.name_of_product = '{product}'
            """
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()

    matches_sources = []
    source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    matches_sources.append(source)
    return myresult, matches_sources

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype"]
    return col, db
        
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

def get_sources(query, namespaces):
    index = initPinecone() #
    #initialize mongoDB
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype"]
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    
    matches_content = []
    matches_sources = []
    
    for namespace, num_sources in namespaces:

        pinecone_results = index.query([filtered_query_embedding], top_k=num_sources, include_metadata=True, namespace=namespace)
        unique_pinecone_results = pinecone_results['matches']
        
        print("")
        print(namespace)
        print("")
        print(unique_pinecone_results)
 

        
        #get matches from mongoDB for IDs
        for id in unique_pinecone_results:
            idToFind = ObjectId(id['id'])
            match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun
            #DONT PRINT MATCHES, IT CAUSES ENCODING BUGS
            #print(match)
            # print(match['content'])
            matches_content.append(match['content'])
        
            source = {'id': str(match['_id']), 'content': match['content'], 'metadata': match['metadata']}
            matches_sources.append(source)


    return matches_content, matches_sources, used_tokens

def get_extra_sources(source):
    result = []
    if source["metadata"]["type"] == 'email' or source["metadata"]["type"] == 'ticket':
        mongodb_connection = initMongo()[0]
        source_id = source["metadata"]["source_id"]
        order_id = source["metadata"]["order_id"]
        query = {
            "metadata.source_id": source_id,
            "metadata.order_id": order_id + 1
        }
        source_extra = mongodb_connection.find(query)
        result = list(source_extra)
        if result:
            result = result[0]
            result["id"] = result.pop("_id")
            result["id"] = str(result["id"])
    return result
