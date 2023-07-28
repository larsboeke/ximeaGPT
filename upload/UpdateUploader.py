import pymongo
import pinecone
import os
import openai
import mysql.connector
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
        """
        Creates an embedding for a chunk
        :param chunk:
        :return chunkEmbedding: created embedding
        """
        chunkText = chunk['content']
        chunkEmbedding = openai.Embedding.create(input=chunkText, model=self.EMBEDDING_MODEL)['data'][0]['embedding']

        return chunkEmbedding

    # Upload created chunks to MongoDB and Pinecone
    def uploadChunk(self, chunk, index, col):
        """
        Uploads a chunk to pinecone and mongodb
        :param chunk:
        :param index: pinecone_connection
        :param col: mongodb_connection
        :return:
        """
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

        if (chunk['metadata']['type'] == 'ticket'):
            index.upsert([(id, chunkEmbedding)], namespace='tickets')
        elif (chunk['metadata']['type'] == 'email'):
            index.upsert([(id, chunkEmbedding)], namespace='emails')
            # manuals get uploaded to manuals namespace
        elif (chunk['metadata']['type'] == 'manuals' or chunk['metadata']['type'] == 'text'):
            index.upsert([(id, chunkEmbedding)], namespace='manuals')

    def is_file_uploaded(self, source, file_type):
        """
        Checks if a file is already uploaded
        :param source:
        :param file_type:
        :return is_uploaded:
        """
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
        """
        Uploads a PDF from a given path
        :param path:
        """
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
        """
        Uploads a URL from a given URL
        :param url:
        """
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
            EmailDatabaseDeleter(pinecone_connection, mongodb_connection, sql_connection).delete_null_activities()
            EmailDatabaseDeleter(pinecone_connection, mongodb_connection, sql_connection).deleteCases(updated_cases)
            for case in updated_cases:
                emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
                one_case = Case(str(case[0]), emails_for_one_case)
                content = PlainTextFromCaseProvider().provide_full_content(one_case)
                chunks = Chunker().data_to_chunks(content, one_case.metadata)
                #print(chunks)
                SQLDatabaseUpdater(sql_connection).update_case(case[0])
                for chunk in chunks:
                    self.uploadChunk(chunk, pinecone_connection, mongodb_connection)

                SQLDatabaseUpdater(sql_connection).update_case(case[0])
                sql_connection[0].close()

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



    def uploadPDB(self):
        config = {
        'host':'ximeapdbdev.mysql.database.azure.com',
        'user':'ai_lean_dev',
        'password':'8CXhkZqU5FxyKT',
        'database':'products',
        'client_flags': [mysql.connector.ClientFlag.SSL],
        'ssl_ca': 'DigiCertGlobalRootG2.crt.pem'
        }

        try:
            source_connection = mysql.connector.connect(**config)
            source_cursor = source_connection.cursor()
            destination_connection, destination_cursor = SQLConnectionProvider().create_connection()
        except:
            print("connection error")


        create_table_sql = """
        CREATE TABLE [AI:Lean].[dbo].[product_database_staging] (
            name_of_camera VARCHAR(145) NULL,
            name_of_feature VARCHAR(45) NULL,
            value_of_feature VARCHAR(MAX),
            unit VARCHAR(45) NULL,
            description_of_feature VARCHAR(245) NULL
        );"""
        source_sql_command = """
        SELECT p.name, f.name, pfr.value_txt, f.gentl_unit, f.gentl_description
        FROM feat f
        INNER JOIN prodfeat pfr
        ON f.id = pfr.id_feat
        INNER JOIN prod p
        ON pfr.id_product = p.id;
        ;"""

        drop_table_command = """DROP TABLE [AI:Lean].[dbo].[product_database_staging];"""
        try:
            destination_cursor.execute(drop_table_command)
            destination_connection.commit()
            print('Delete old table')
            destination_cursor.execute(create_table_sql)
            print('Create new table')
            source_cursor.execute(source_sql_command)
            data_to_insert = source_cursor.fetchall()
            print("data_fetched")
            insert_query = "INSERT INTO [AI:Lean].[dbo].[product_database_staging] (name_of_camera, name_of_feature, value_of_feature, unit, description_of_feature) VALUES (%s, %s,%s,%s,%s)"
            destination_cursor.executemany(insert_query, data_to_insert)
            
            destination_connection.commit()
            print('data_transfered')
            destination_cursor.execute("""UPDATE [AI:Lean].[dbo].[product_database_staging]
            SET value_of_feature = NULL
            WHERE value_of_feature = 'used';""")
            destination_connection.commit()
            print("used = NULL")
            destination_cursor.execute("""UPDATE [AI:Lean].[dbo].[product_database_staging]
            SET name_of_feature = 'Camera Family'
            WHERE name_of_feature = 'Marketing Name';""")
            destination_connection.commit()


            print("Product Database Push finished")

        except Exception as e:
            print("Error occurred:", e)

        finally:
            # Close the connections
            source_cursor.close()
            source_connection.close()
        
