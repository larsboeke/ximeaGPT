import pymongo
import pinecone
import os
import openai
from dotenv import load_dotenv
from time import sleep
from data_package.SQL_Connection_Provider import SQLConnectionProvider
from data_package.Mail_Handler.CaseRepository import CaseRepository
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
from data_package.Mail_Handler.EmailRepository import EmailRepository
from data_package.Mail_Handler.Case import Case
from data_package.Mail_Handler.PlainTextFromCaseProvider import PlainTextFromCaseProvider
from data_package.Chunk_Handler.Chunker import Chunker
from data_package.Mail_Handler.SQLDatabaseUpdater import SQLDatabaseUpdater
from data_package.Mail_Handler.EmailDatabaseDeleter import EmailDatabaseDeleter
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider
from data_package.PDF_Handler.PDF import PDF
from data_package.PDF_Handler.PlainTextProviderPDF import PlainTextProviderPDF
from data_package.URL_Handler.URL import URL
from data_package.URL_Handler.PlainTextProviderURL import PlainTextProviderURL
from data_package.Ticket_Handler.Ticket import Ticket
from data_package.Ticket_Handler.PlainTextProviderTicket import PlainTextProviderTicket
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()


class UpdateUploader:

    def __init__(self):
        # Load environment and set variables

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")

    # Method to create embeddings using OpenAI API
    def createEmbedding(self, chunk):  # JSON als Input
        chunkText = chunk['content']
        chunkEmbedding = openai.Embedding.create(input=chunkText, model=self.EMBEDDING_MODEL)['data'][0]['embedding']

        return chunkEmbedding

    # Upload created chunks to MongoDB and Pinecone
    def uploadChunk(self, chunk, index, col):
        # Try Create embedding x times (due to APIERROR)
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                chunkEmbedding = self.createEmbedding(chunk)
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

        # Emails and Tickets get uploaded to pastConversations Namespace
        if (chunk['metadata']['type'] == 'email' or chunk['metadata']['type'] == 'ticket'):
            index.upsert([(id, chunkEmbedding)], namespace='pastConversations')

            # manuals get uploaded to manuals namespace
        elif (chunk['metadata']['type'] == 'manuals'):
            index.upsert([(id, chunkEmbedding)], namespace='manuals')

    def is_file_uploaded(self, source, file_type):
        col = MongoDBConnectionProvider().initMongoDB()
        type_to_key_map = {
            'ticket': 'TicketID',
            'manuals': 'source'
        }

        key = type_to_key_map.get(file_type)
        if key is not None:
            is_uploaded = col.count_documents({"metadata." + key: source}) != 0
        else:
            is_uploaded = False

        return is_uploaded

    # Upload PDFs from given path
    def uploadPDF(self, path):
        file_type = 'manuals'
        if self.is_file_uploaded(path, file_type) == False:
            mongodb_connection = MongoDBConnectionProvider().initMongoDB()
            pinecone_connection = PineconeConnectionProvider().initPinecone()
            pdf = PDF(path=path)
            plainString = PlainTextProviderPDF().get_text(pdf)
            chunks = Chunker().data_to_chunks(plainString, pdf.get_metadata())

            for chunk in chunks:
                self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

            print("uploaded " + path)
        else:
            print("File already uploaded")

    # Upload Pagecontent from given URLs
    def uploadURL(self, url):
        file_type = 'manuals'
        if self.is_file_uploaded(url, file_type) == False:
            mongodb_connection = MongoDBConnectionProvider().initMongoDB()
            pinecone_connection = PineconeConnectionProvider().initPinecone()

            url1 = URL(url)
            plainURL = PlainTextProviderURL().get_text(url1)
            chunks = Chunker().data_to_chunks(plainURL, url1.get_metadata())

            for chunk in chunks:
                self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

            print("uploaded " + url)
        else:
            print("File already uploaded")

    # Upload mails from SQL database
    def upload_new_cases_and_updated_cases(self):
        """
        A function that uploads all new cases from the database and updates
        the database with the already uploaded cases
        """
        sql_connection = SQLConnectionProvider().create_connection()
        pinecone_connection = PineconeConnectionProvider().initPinecone()
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()

        updated_cases = CaseRepository(sql_connection).get_updated_cases()
        print("Cases to be updated: ", len(updated_cases))

        if updated_cases:
            EmailDatabaseDeleter(pinecone_connection, mongodb_connection).deleteCases(updated_cases)
            for case in updated_cases:
                emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
                one_case = Case(case[0], emails_for_one_case)
                content = PlainTextFromCaseProvider().provide_full_content(one_case)
                chunks = Chunker().data_to_chunks(content, one_case.metadata)
                print(chunks)
                SQLDatabaseUpdater(sql_connection).update_case(case[0])

    # Upload tickets from Deskpro API
    def uploadNewTicket(self, TicketID):
        """
        A function that uploads a new resolved ticket from the Deskpro API
        :param TicketID: The ID of the ticket to be uploaded
        """
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()
        pinecone_connection = PineconeConnectionProvider().initPinecone()

        ticket = Ticket(TicketID)
        plainTicket = PlainTextProviderTicket().getText(ticket)
        chunks = Chunker().data_to_chunks(plainTicket, ticket.metadata)

        for chunk in chunks:
            self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

        print("uploaded ticket: " + str(TicketID))



