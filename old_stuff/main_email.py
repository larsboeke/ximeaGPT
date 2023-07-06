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

sql_connection = SQLConnectionProvider().create_connection()

all_cases = CaseRepository(sql_connection).get_all_cases()

#Liste an Email-Objekten
print(all_cases[5][0])
emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(all_cases[5][0])

one_case = Case(all_cases[5][0], emails_for_one_case)
content = PlainTextFromCaseProvider().provide_full_content(one_case)

chunks = Chunker().data_to_chunks(content, one_case.metadata)
print(chunks)

SQLDatabaseUpdater(sql_connection).update_case(all_cases[5][0])

def upload_all_cases():
    """
    Example of a function that uploads all cases from the database and updates
    the database with the already uploaded cases
    """
    sql_connection = SQLConnectionProvider().create_connection()
    all_cases = CaseRepository(sql_connection).get_all_cases()
    if all_cases:
        for case in all_cases:
            emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
            one_case = Case(case[0], emails_for_one_case)
            content = PlainTextFromCaseProvider().provide_full_content(one_case)
            chunks = Chunker().data_to_chunks(content, one_case.metadata)
            print(chunks)
            SQLDatabaseUpdater(sql_connection).update_case(case[0])

def upload_new_cases_and_updated_cases():
    """
    Example of a function that uploads all cases from the database and updates
    the database with the already uploaded cases
    """
    sql_connection = SQLConnectionProvider().create_connection()
    pinecone_connection = PineconeConnectionProvider().initPinecone()
    mongodb_connection = MongoDBConnectionProvider().initMongoDB()

    updated_cases = CaseRepository(sql_connection).get_updated_cases()
    print("Cases to be updated: ", len(updated_cases))

    if updated_cases:
        EmailDatabaseDeleter(pinecone_connection, mongodb_connection, sql_connection).deleteCases(updated_cases)
        for case in updated_cases:
            emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(case[0])
            one_case = Case(case[0], emails_for_one_case)
            content = PlainTextFromCaseProvider().provide_full_content(one_case)
            chunks = Chunker().data_to_chunks(content, one_case.metadata)
            print(chunks)
            SQLDatabaseUpdater(sql_connection).update_case(case[0])





