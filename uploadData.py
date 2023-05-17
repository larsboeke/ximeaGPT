import pymongo
import pinecone
import os
import openai
import pdfChunker

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")



def createEmbedding(chunk):#JSON als Input
    chunkText = chunk['content']
    chunkEmbedding = openai.Embedding.create(input = chunkText, model=EMBEDDING_MODEL)['data'][0]['embedding']

    return chunkEmbedding


def initMonogo():
    client = pymongo.MongoClient("adress")
    db = client["mydatabase"]                   #Ändern
    col = db["collection"]
    return col
        
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

def uploadChunk(chunk, index, col):

    chunkEmbedding = createEmbedding(chunk)
    id = col.insert_one(chunk)
        #Emails and Tickets get uploaded to pastConversations Namespace
    if (chunk['metadata']['type'] == 'email' or 'ticket'):
        index.upsert([(id, chunkEmbedding)], namespace='pastConversations')

        #manuals get uploaded to manuals namespace
    elif (chunk['metadata']['type'] == 'manual'):
        index.upsert([(id, chunkEmbedding)], namespace='maunals')
        

def uploadPDF(path):
    chunks = pdfChunker.chunkPDF(path)
    col = initMonogo()
    index = initPinecone()

    for chunk in chunks:
        uploadChunk(chunk, index, col)
    

def uploadMail():
    #chunks = mailChunker.chunkMail(path)
    col = initMonogo()
    index = initPinecone()
    pass
