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

class Uploader:

    def __init__(self):
        # Load environment and set variables
        
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")


    # Method to create embeddings using OpenAI API
    def createEmbedding(self, chunk):#JSON als Input
        chunkText = chunk['content']
        chunkEmbedding = openai.Embedding.create(input = chunkText, model=self.EMBEDDING_MODEL)['data'][0]['embedding']

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

            #Emails and Tickets get uploaded to pastConversations Namespace
        if (chunk['metadata']['type'] == 'email' or chunk['metadata']['type'] == 'ticket'):
            index.upsert([(id, chunkEmbedding)], namespace='pastConversations')

            #manuals get uploaded to manuals namespace
        elif (chunk['metadata']['type'] == 'manuals'):
            index.upsert([(id, chunkEmbedding)], namespace='manuals')


    def is_file_uploaded(self, source):
        col = MongoDBConnectionProvider().initMongoDB()


        is_uploaded = col.count_documents({"metadata.source_id" : source}) != 0


        return is_uploaded

    # Upload PDFs from given path
    def uploadPDF(self, path):
        if self.is_file_uploaded(path) == False:
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
        if self.is_file_uploaded(url) == False:
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


    def upload_cases_parallel(self, cases, pinecone_connection, mongodb_connection):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.uploadCase, case, pinecone_connection, mongodb_connection): case for case in cases}
            for future in as_completed(futures):
                case = futures[future]
                try:
                    future.result()  # This will raise an exception if the uploadCase method failed.
                    print(f"Case: {case} uploaded successfully!")
                except Exception as exc:
                    print(f"Case: {case} generated an exception: {exc}")


    def uploadCase(self, case, pinecone_connection, mongodb_connection):
        sql_connection = SQLConnectionProvider().create_connection()
        emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
        one_case = Case(str(case[0]), emails_for_one_case)
        content = PlainTextFromCaseProvider().provide_full_content(one_case)
        chunks = Chunker().data_to_chunks(content, one_case.metadata)
        
        for chunk in chunks:
            self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

        SQLDatabaseUpdater(sql_connection).update_case(case[0])
        sql_connection[0].close()

    # Upload mails from SQL database
    def uploadMails(self):
        """
        Example of a function that uploads all cases from the database and updates
        the database with the already uploaded cases
        """
        sql_connection = SQLConnectionProvider().create_connection()
        pinecone_connection = PineconeConnectionProvider().initPinecone()
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()

        updated_cases = CaseRepository(sql_connection).get_updated_cases()
        all_cases = CaseRepository(sql_connection).get_all_cases()
        print("Cases to be updated: ", len(updated_cases))
        if updated_cases != all_cases:
            EmailDatabaseDeleter(pinecone_connection, mongodb_connection).deleteCases(updated_cases)

        if updated_cases and updated_cases != []:
            for case in updated_cases:
                emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
                one_case = Case(str(case[0]), emails_for_one_case)
                content = PlainTextFromCaseProvider().provide_full_content(one_case)
                chunks = Chunker().data_to_chunks(content, one_case.metadata)
                SQLDatabaseUpdater(sql_connection).update_case(case[0])
                for chunk in chunks:
                    self.uploadChunk(chunk, pinecone_connection, mongodb_connection)
                print("Case: " , case[0], " uploaded!")

    def initialUploadMail(self):
        sql_connection = SQLConnectionProvider().create_connection()
        pinecone_connection = PineconeConnectionProvider().initPinecone()
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()
        all_cases = CaseRepository(sql_connection).get_all_cases()
        self.upload_cases_parallel(all_cases, pinecone_connection, mongodb_connection)


    # Upload tickets from Deskpro API
    def uploadTicket(self, TicketID):
        # remove is_file_uploaded after initial upload, not needed anymore then
        if self.is_file_uploaded(str(TicketID)) == False:
            mongodb_connection = MongoDBConnectionProvider().initMongoDB()
            pinecone_connection = PineconeConnectionProvider().initPinecone()

            ticket = Ticket(TicketID)
            plainTicket = PlainTextProviderTicket().getText(ticket)
            chunks = Chunker().data_to_chunks(plainTicket, ticket.metadata)

            for chunk in chunks:
                self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

            print("uploaded ticket: " + str(TicketID))
        else:
            print("File already uploaded")


