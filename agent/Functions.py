import pymongo
import pinecone
import openai
import os
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

get_last_message = "pass"

query_product_databse = "pass"

tools = [get_context_tool, query_maunals]

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

def getText(query, namespace):
    index = initPinecone() #
    #initialize mongoDB
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype2"]
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
    matches_content = []
    matches_sources = []
    print(pinecone_results)
    for id in pinecone_results['matches']:
        idToFind = ObjectId(id['id'])
        match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun    
        print(match)
        # print(match['content'])
        matches_content.append(match['content'])
    
        source = {'id': str(match['_id']), 'content': match['content'], 'source': match['metadata']}
        matches_sources.append(source)


    return matches_content, matches_sources, used_tokens

