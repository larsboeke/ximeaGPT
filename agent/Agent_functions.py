#import pymongo
#import pinecone
import openai
import pymssql
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import tiktoken
from difflib import SequenceMatcher
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
import json

load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

get_context_tool = {
                "name": "query_past_conversations",
                "description": "Get Context from past conversations that already happend with real customers to.",
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

query_manuals = {
                "name": "query_manuals",
                "description": "Query technical manuals to get technical information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to gather technical information about",
                        },
                    },
                    "required": ["query"],
                },
            }
#Checken was Der als Query
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
            }
query_pdb ={
            "name": "query_pdb",
                "description": "Write an SQL Query and retrieve Informations from XIMEAs Product Database! Watch out! The Column value_of_feature is of Type Text. TABLE product_database COLUMNS id_product | id_feature | name_of_feature | name_of_product | value_of_feature | unit | description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL Query which can answer the question of the user! Only query what is neccesary!",
                        },
                    },
                    "required": ["query"],
                },
}

get_correct_features ={
            "name": "get_correct_features",
                "description": "In order to write an correct SQL Query you need to have the correct name_of_feature. Use this tool to get the correct names for the features you want to query! The second value is the simmilarity score.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features":{
                            "type": "array",
                             "description": "An array of strings to pass to the function for getting the corresponding Feature names back, e.g. ['Resolution', 'OffsetX'].",
                             "items": {
                                 "type": "string"
                             }

                        }
                    },
                    "required": ["features"],
                }
}
use_structured_data ={
            "name": "use_structured_data",
                "description": """
                This function can be used in three ways (1,2,3).
                1: Input = query -> Write an SQL Query and retrieve Informations from XIMEAs Product Database! TABLE product_database COLUMNS id_product | id_feature | name_of_feature | name_of_product | value_of_feature | unit | description
                2: Input = features -> When you give this function a list of features you will get a list with the most simmilar features back that exists in the product database. The second value is the simmilarity score.
                3: Input = features + query -> Runs the query only if all the names of features exists in the product database! Otherwise the return will be like the same as just the feature list as input!""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features":{
                            "type": "array",
                             "description": "An array of strings to pass to the function for getting the corresponding Feature names back, e.g. ['Resolution', 'OffsetX'].",
                             "items": {
                                 "type": "string"
                             }

                        },
                        "query": {
                            "type": "string",
                            "description": "SQL Query which can answer the question of the user! Only query what is neccesary!",
                        },
                    },
                    
                }
}                   
#TABLE product_database COLUMNS id_product | id_feature | name_of_feature | name_of_product | value_of_feature | unit | description
query_product_database_with2function_call ={
            "name": "use_product_database",
                "description": "This function can be used to write a SQL query with the correct feature names on the XIMEA SQL Database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features":{
                            "type": "array",
                             "description": "An array of strings to pass to the function for getting the corresponding Feature names back, e.g. ['Resolution', 'OffsetX'].If you don't want to look for any Features then give an empty list as a parameter e.g [] ",
                             "items": {
                                 "type": "string"
                             }

                        },
                        "user_question": {
                            "type": "string",
                            "description": "Place the question the user asked you right here!",
                        },
                    },
                    "required": ["features","user_question"],
                }
}                   
tools = [
    #use_structured_data,
    #query_all,
    query_product_database_with2function_call,
    #query_pdb,
    #get_correct_features,
    #query_feature_of_product_pdb,
    #query_data_of_feature_of_product_pdb,
    # query_data_of_category_feature_of_product_pdb,
]
def query_product_database_with2function_call(user_question, feature_list):
    if feature_list != []:
        feature_list = similar(feature_list)
    message = get_openai_response(user_question, feature_list)
    # json_str = message["function_call"]["arguments"]
    # data = json.loads(json_str)
    # function_name = message["function_call"]["name"]
    # if function_name == "query_pdb":
    #     print("Using query_pdb tool...")
            
    #     function_response, sources = query_pdb( 
    #         query=data.get("query")
    #     )
    #     print(function_response)
    print(str(message.get('content')))
    query = message.get('content')
    function_response, sources = query_pdb( query=query)
    print(str(function_response))
    return function_response, sources
    
def get_openai_response(user_question, feature_list):
    max_attempts = 5
    x = 0
    while x < max_attempts:

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please write an SQL query to answer this this: {user_question}. Use these feature names for the features mentioned in the question!: {str(feature_list)}. TABLE product_database COLUMNS id_product | id_feature | name_of_feature | name_of_product | value_of_feature | unit | description . ONLY WRITE THE SQL QUERY NOTHING ELSE!"}],
                #functions=[query_pdb],
                #function_call="None",#"""{"name":\ "query_pdb"}""",
                temperature = 0,  
)
            return response["choices"][0]["message"]

        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
    
def use_structured_data(query=None, feature_list=None):
    print("query")
    print(str(query))
    print("feature_list")
    print(str(feature_list))
    #print("1")

    if query != None and feature_list == None:
        #print("1.1")
        result, source = query_pdb(query)
        #print("2")
    elif query is None and feature_list is not None:
        result, source = get_correct_features(feature_list)
        #print("3")
    elif query is None and feature_list is None:
        result, source = None
        #print("4")
    elif query is not None and feature_list is not None:
        result, source = get_correct_features(feature_list)
        #print("5")
        lowest_value_1 = True
        for tup in result:
            lowest_value_1 = tup[1] == 1 and lowest_value_1 == True
            if lowest_value_1:
                result, source = query_pdb(query)

    return result, source
    
def get_correct_features(feature_list):
    combined_answers = similar(feature_list)
    sources = []
    return combined_answers, sources
    
def similar(OpenAIs_features):
    connection, cursor = SQLConnectionProvider().create_connection()
    cursor.execute("SELECT DISTINCT name_of_feature FROM product_database;")
    liste_of_all_features = cursor.fetchall()
    highest_score = 0
    highest_element = None
    actual_feautures = []
    score_list = []
    for feature in OpenAIs_features:
        score = 0
        highest_score= 0
        for l in liste_of_all_features:
            score = SequenceMatcher(None, l[0], feature).ratio()
            if score > highest_score:
                highest_score = score
                highest_element = l[0]
        actual_feautures.append(highest_element)
        score_list.append(highest_score)
    
    return list(zip(actual_feautures, score_list))

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

def query_pdb(query):
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except Exception as e:
        myresult = "The query you wrote produced an error message. First use get_correct_features if you were querying for features! If after checking the features you still get this message then ask the user for clarification!" + str(e)
    else:
        myresult = mycursor.fetchall()
    if myresult == []:
        myresult =  "The query you wrote didn't contain data. First use get_correct_features if you were querying for features! If after checking the features you still get this message then ask the user for clarification!"
    if num_tokens_from_string(str(myresult))>3000:
        myresult =  "The query you wrote contains too much data for you to handle. Rewrite the SQL Query so that less data is returned!"
    matches_sources = []

    source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    matches_sources.append(source)
    endresult = [query, myresult]
    return endresult, matches_sources
    

#     source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}


def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
     #Returns the number of tokens in a text string.
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

def getText(query, counter):
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
    
    namespaces = [("pastConversations", [0, 2, 4, 6]), ("manuals", [0, 1, 2, 3])]
    for namespace, borders in namespaces:

        pinecone_results = index.query([filtered_query_embedding], top_k=borders[counter], include_metadata=True, namespace=namespace)
        unique_pinecone_results = pinecone_results['matches'][borders[counter -1]:borders[counter]]
        
        print("")
        print(namespace)
        print("")
        print(unique_pinecone_results)
 

        
        #get matches from mongoDB for IDs

        print(pinecone_results)
        for id in unique_pinecone_results:
            idToFind = ObjectId(id['id'])
            match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun    
            print(match)
            # print(match['content'])
            matches_content.append(match['content'])
        
            source = {'id': str(match['_id']), 'content': match['content'], 'metadata': match['metadata']}
            matches_sources.append(source)


    return matches_content, matches_sources, used_tokens