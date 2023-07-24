import openai
import os
import pinecone
from dotenv import load_dotenv
import pandas as pd
import agent.Agent_functions as af
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index
index = initPinecone()
i = 0
all_feature, source = af.query_pdb(query= "SELECT DISTINCT name_of_feature FROM product_database;")
for feature in all_feature[1]:
    embedding_response = openai.Embedding.create(
    input=feature[0],
    model="text-embedding-ada-002"
    )
    i += 1
    print(str)
    embeddings = embedding_response['data'][0]['embedding']
    index.upsert(vectors=[(feature[0], embeddings)],
             namespace='name_of_sql_features')



#embeddings = response['data'][0]['embedding']



