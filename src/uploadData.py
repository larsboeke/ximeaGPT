import pymongo
import pinecone
import os
import openai

os.environ["PINECONE_API_KEY"] = "d589266c-40d5-4a99-a813-8166f90f11a3"


def createEmbedding(chunk):#JSON als Input
    chunkText = chunk['text']
    chunkEmbedding = openai.Embedding.create(input = chunkText, model='text-embedding-ada-002')['data'][0]['embedding']

    return chunkEmbedding

def uploadToMongo(chunk):
    client = pymongo.MongoClient("adress")
    db = client["mydatabase"]                   #Ändern
    col = db["collection"]

    #insert_one retruns ID
    id = col.insert_one(chunk)
    return id

def uploadToPinecone(id, embedding, namespace):
    pinecone.init(
        api_key="64dd442b-648a-4350-984e-60607443d969",
        environment="us-west1-gcp"
    )
    index = pinecone.Index("ailean")
    index.upsert([(id, embedding)], namespace=namespace)


def uploadChunk(chunk):

    chunkEmbedding = createEmbedding(chunk)
    id = uploadToMongo(chunk)
        #Emails and Tickets get uploaded to pastConversations Namespace
    if (chunk['metadata']['type'] == 'email' or 'ticket'):
        uploadToPinecone(id, chunkEmbedding, 'pastConversations')

        #manuals get uploaded to manuals namespace
    elif (chunk['metadata']['type'] == 'manual'):
        uploadToPinecone(id, chunkEmbedding, 'manuals')
        



