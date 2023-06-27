import pymongo
import pinecone
import openai
import os
import mysql.connector
import json
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

get_context_tool = {
                "name": "get_context_tool",
                "description": "Query past conversations based on embeddings to get similar contexts to answer the question",
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

query_maunals = {
                "name": "query_manuals",
                "description": "Query manuals based on embeddings to get technical information",
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

get_mysql = {
            "name": "get_mysql",
            "description": "Get the result back from a valid sql query on a database. Use it when you are asked about an mysql query!",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlquery": {
                        "type": "string",
                        "description": "Valid MySQL syntax, e.g. SELECT id FROM prod LIMIT 5;",
                    },
                },
                "required": ["sqlquery"],
            },
        }
get_last_message = "pass"

query_product_databse = "pass"

tools = [get_context_tool, query_maunals, get_mysql]

def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["test"]
    return col, db


        
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

def get_mysql(sqlquery):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="859760Si.",
    database="products3"
    )
    mycursor = mydb.cursor()

    mycursor.execute(sqlquery)
    myresult = mycursor.fetchall()

    query_info = {
        "sqlquery": sqlquery,
        "database_response": myresult
    }
    return json.dumps(query_info)

def getText(query, namespace):
    index = initPinecone() #
    #initialize mongoDB
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype"]
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    pinecone_results = index.query([filtered_query_embedding], top_k=3, include_metadata=True, namespace=namespace)
    #validIds = []
        # try:
    #     for id in ids:
    #         if id['score'] > float(0):  #parameter anpassen
    #             validIds.append(id)
    # except:
    #     print("Pinecone query failed")


    #get matches from mongoDB for IDs
    matches = []
    print(pinecone_results)
    for id in pinecone_results['matches']:
        idToFind = ObjectId(id['id'])
        match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun    
        matches.append(match)
       

    return matches, used_tokens

