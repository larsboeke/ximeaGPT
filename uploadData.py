import pymongo
import pinecone
import os
import openai
from process_manuals import pdfChunker
from dotenv import load_dotenv
from process_emails import email_chunker
from time import sleep
from process_tickets.TicketChunker import TicketChunker
from process_tickets.Ticket import Ticket

# Load environment and set variables
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")


# Method to create embeddings using OpenAI API
def createEmbedding(chunk):#JSON als Input
    chunkText = chunk['content']
    chunkEmbedding = openai.Embedding.create(input = chunkText, model=EMBEDDING_MODEL)['data'][0]['embedding']

    return chunkEmbedding

def initMongo():
    # Initialise the non structured database MongoDB
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]
    col = db["test"]
    return col

# Initiialise Pinecone to upload embeddings
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

# Upload created chunks to MongoDB and Pinecone
def uploadChunk(chunk, index, col):
    # Try Create embedding x times (due to APIERROR)
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            chunkEmbedding = createEmbedding(chunk)
            # If the function is successful, we end the loop
            break
        except Exception as e:
            print(type(e).__name__)
            print("Could not create embedding, waiting 5 seconds")
            sleep(5)
            if attempt == max_attempts - 1:
                # If it was the last try, we throw the exception again
                raise e

    id_ = col.insert_one(chunk)
    id = str(id_.inserted_id)

        #Emails and Tickets get uploaded to pastConversations Namespace
    if (chunk['metadata']['type'] == 'email' or chunk['metadata']['type'] == 'ticket'):
        index.upsert([(id, chunkEmbedding)], namespace='pastConversations')

        #manuals get uploaded to manuals namespace
    elif (chunk['metadata']['type'] == 'manuals'):
        index.upsert([(id, chunkEmbedding)], namespace='maunals')


def is_file_uploaded(source, file_type):
    col = initMongo()
    type_to_key_map = {
        'email': 'case_id',
        # TODO: ticketID moeglicherweise falsch, vlt abändern zu TicketID
        'ticket': 'ticketID',
        'manuals': 'source'
    }

    key = type_to_key_map.get(file_type)
    if key is not None:
        is_uploaded = col.count_documents({"metadata." + key: source}) != 0
    else:
        is_uploaded = False

    return is_uploaded

# Upload PDFs from given path
def uploadPDF(path):
    file_type = 'manuals'
    if is_file_uploaded(path, file_type) == False:
        col = initMongo()
        index = initPinecone()
        chunks = pdfChunker.chunkPDF(path)

        for chunk in chunks:
            uploadChunk(chunk, index, col)

        print("uploaded " + path)
    else:
        print("File already uploaded")

# Upload Pagecontent from given URLs
def uploadURL(url):
    file_type = 'manuals'
    if is_file_uploaded(url, file_type) == False:
        col = initMongo()
        index = initPinecone()

        chunks = pdfChunker.chunkURL(url)

        for chunk in chunks:
            uploadChunk(chunk, index, col)

        print("uploaded " + url)
    else:
        print("File already uploaded")

# Upload mails from SQL database
def uploadMail(case):
    file_type = 'email'
    if is_file_uploaded(case, file_type) == False:
        col = initMongo()
        index = initPinecone()
        chunks = email_chunker.chunk_email(case)
        for chunk in chunks:
            uploadChunk(chunk, index, col)

        print("uploaded case: " + str(case))
    else:
        print("File already uploaded")

# Upload tickets from Deskpro API
def uploadTicket(TicketID):
    file_type = 'ticket'
    if is_file_uploaded(TicketID, file_type) == False:
        ticket = Ticket(TicketID)
        ticket.set_WholeTicket()
        ticket.set_metadata()
        ticket.set_fullTicketText()
        chunker = TicketChunker()
        chunks = chunker.chunkTicket(ticket)
        col = initMongo()
        index = initPinecone()

        for chunk in chunks:
            uploadChunk(chunk, index, col)

        print("uploaded ticket: " + str(TicketID))
    else:
        print("File already uploaded")
