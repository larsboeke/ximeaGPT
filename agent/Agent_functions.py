import pymongo
import pinecone
import openai
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
                "description": "This function provides infomation form support tickets, emails and technical manuals. This tool is best to use if all of these data sources provide could provide the neccesary information. Also use this tool if you are unsure which other tool to use!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The question the User wants you to answer! e.g. 'What is the XIX camera Family?'",
                        },
                        "features":{
                            "type": "array",
                             "description": "An array of all feature names that you can identify within the user prompt, e.g. ['Resolution', 'Device Rest xiapi' , 'xiapi_DeviceLocPath' ,'OffsetX']. Only use it when you are given a Feature!",
                             "items": {
                                 "type": "string"
                             }

                        },
                    },
                    "required": ["query"],
                },
            }


query_emails_and_tickets = {
                "name": "query_emails_and_tickets",
                "description": "This function answers the users query only with information of from the support eamils and tickets of XIMEA. Therefore use cases for this tool are when the user asks for the email or ticket history for a case. This tool provides infomation about things that typically get negotiated in emails or tickets, like contract datails ... Keep in mind that data from technical manuals is not included!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The question the User wants you to answer! e.g. 'What is the XIX camera Family?'",
                        },
                    },
                    "required": ["query"],
                },
            }


query_manuals = {
                "name": "query_manuals",
                "description": "This function will give you informations from XIMEA's technical manuals. The manuals contain information about camera/camera families including hardware specification, system requirements, instalation of related software drivers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The question the User want you to answer! e.g. 'What is the XIX camera Family?' ",
                        },
                    },
                    "required": ["query"],
                },
            }


# Fucntions for the PDB
database_schema = "TABLE product_database COLUMNS name_of_feature | name_of_camera | value_of_feature | unit | description_of_feature "

query_product_database_with2function_call ={
            "name": "use_product_database",
                "description": f"This function can be used to query the SQL Product Database (pdb) of XIMEA. It is useful when you are asked for certain features of cameras.{database_schema}.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "features":{
                            "type": "array",
                             "description": "An array of all feature names that you can identify within the user prompt, e.g. ['Resolution', 'Device Rest xiapi' , 'xiapi_DeviceLocPath' ,'OffsetX']. Only use it when you are given a Feature!",
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


query_pdb = {
            "name": "query_pdb",
            "description": "Get the result from a query on the product_database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A correct Transact-SQL Query!",
                    }
                    
                },
                "required": ["query"],
            },
        }


local_functions = [ query_pdb,]

tools = [
    query_all_sources,
    query_manuals,
    query_emails_and_tickets,
    query_product_database_with2function_call,
]


def query_product_database_with2function_call(feature_list = None, message_history = None):

    if feature_list != None:
        feature_list = similar_embeddings(feature_list)

    message = get_openai_sql_response(feature_list, message_history)

    json_str = message["function_call"]["arguments"]
    data = json.loads(json_str)

    function_response, sources = query_pdb(query=data.get("query"))

    return function_response, sources


def get_openai_sql_response(feature_list, message_history):
    max_attempts = 5
    x = 0
    
    if feature_list == None:
        message_history.append(
        {"role": "function", "name": "use_product_database", "content": f"NOW ONLY WRITE ONE TRANSACT-SQL QUERY to answer the user question. Do not use a WHERE clause. Use this table {database_schema}"})
    else:
        message_history.append(
        {"role": "function", "name": "use_product_database", "content": f"NOW ONLY WRITE ONE TRANSACT-SQL QUERY to answer the user question. Pick the matching name_of_feature from this List of features from our database: {feature_list} . Use this table {database_schema}"})

    while x < max_attempts:
        x += 1
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message_history,
                functions=local_functions,
                function_call={"name": "query_pdb"},
                temperature = 0,
            ) 
            return response["choices"][0]["message"]

        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")


#Similarity Search for Featur_names given by LLM!
def similar_embeddings(OpenAIs_features):
    index = initPinecone()
    feature_possibility = []
    for feature in OpenAIs_features:
        feature_embedding = openai.Embedding.create(input=feature, engine="text-embedding-ada-002")['data'][0]['embedding']
        pinecone_results = index.query([feature_embedding], top_k=3, include_metadata=True, namespace='name_of_sql_features')["matches"]
        feature_possibility.append(pinecone_results[0]['id'])
        feature_possibility.append(pinecone_results[1]['id'])
        feature_possibility.append(pinecone_results[2]['id'])
    return feature_possibility


def query_pdb(query):

    connection, mycursor = SQLConnectionProvider().create_connection()

    try:
        mycursor.execute(query)
    except Exception as e:
        myresult = "The query you wrote produced an error message." + str(e)
    else:
        myresult = mycursor.fetchall()
    #Catch possible bad queries and tell the model it made a mistake!
    if myresult == []:
        myresult =  "The query you wrote didn't contain data. Either there is no data for that question or you wrote a bad query!"
    if num_tokens_from_string(str(myresult))>5000:
        myresult =  "The query you wrote contains too much data for you to handle. Rewrite the SQL Query so that less data is returned!"
    
    #TODO: Check if all possible returns can be handled
    source_answer = []
    matches_sources = []
    print("Geschaft3")
    #Reformat the answer of the query! Stop HTML bugs
    if isinstance(myresult, list) and len(myresult) > 0 and isinstance(myresult[0], tuple):
        
        for result_touple in myresult:
            touple_content = []

            for element in result_touple:
                if element is None:
                    touple_content.append("None")
                else:
                    touple_content.append(html.escape(str(element)))

            source_answer.append(touple_content)

    elif isinstance(myresult, str):
        source_answer.append(myresult)
      
    source = {'id': "1", 'content': {'query': query, 'result': str(source_answer)}, 'metadata': {'type': "Product_Database"}}

    matches_sources.append(source)
    endresult = [query, myresult]
    return endresult, matches_sources


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
        
        #get matches from mongoDB for IDs
        for id in unique_pinecone_results:
            idToFind = ObjectId(id['id'])
            match = col.find_one({'_id' : idToFind})
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
