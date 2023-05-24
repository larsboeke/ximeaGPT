import pymongo
import pinecone
import os
import openai
from process_manuals import pdfChunker
from dotenv import load_dotenv
from process_emails import email_chunker


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")



def createEmbedding(chunk):#JSON als Input
    chunkText = chunk['content']
    chunkEmbedding = openai.Embedding.create(input = chunkText, model=EMBEDDING_MODEL)['data'][0]['embedding']

    return chunkEmbedding


def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["test"]
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
    id_ = col.insert_one(chunk)
    id = str(id_.inserted_id)

        #Emails and Tickets get uploaded to pastConversations Namespace
    if (chunk['metadata']['type'] == 'email' or chunk['metadata']['type'] == 'ticket'):
        index.upsert([(id, chunkEmbedding)], namespace='pastConversations')

        #manuals get uploaded to manuals namespace
    elif (chunk['metadata']['type'] == 'manuals'):
        index.upsert([(id, chunkEmbedding)], namespace='maunals')
        

def uploadPDF(path):
    col = initMongo()
    index = initPinecone()
    chunks = pdfChunker.chunkPDF(path)

    for chunk in chunks:
        uploadChunk(chunk, index, col)

    print("uploaded " + path)


def uploadURL(url):
    col = initMongo()
    index = initPinecone()

    chunks = pdfChunker.chunkURL(url)

    for chunk in chunks:
        uploadChunk(chunk, index, col)

    print("uploaded " + url)

def uploadMail(case):
    col = initMongo()
    index = initPinecone()
    chunks = email_chunker.chunk_email(case)
    for chunk in chunks:
        uploadChunk(chunk, index, col)

    print("uploaded case: " + case)


