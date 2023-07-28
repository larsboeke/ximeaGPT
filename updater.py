import time

from data_package.PDB_Handler.PDBSetup import PDBSetup
from upload.UpdateUploader import UpdateUploader
from data_package.Ticket_Handler.TicketRepository import TicketRepository
from upload.DatabaseCleaner import DatabaseCleaner
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider

def updating_loop(time_interval):
    """
    Loop to update the databases with new emails and tickets
    :param time_interval:
    """
    while True:
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()
        pinecone_connection = PineconeConnectionProvider().initPinecone()
        sql_connection = SQLConnectionProvider().create_connection()

        # show current time and date and say that update is starting
        print("Latest update started at: " + time.strftime("%H:%M:%S") + " on " + time.strftime("%d/%m/%Y"))

        # Upload new email cases and update existing email cases
        UpdateUploader().upload_new_cases_and_updated_cases()
        print("All Emails uploaded!")

        new_ticket_ids = TicketRepository().get_new_ids(pages=TicketRepository().count_pages())
        print("Tickets to be uploaded: ", new_ticket_ids)
        # Upload new manuals and update existing manuals
        if len(new_ticket_ids) > 0:
            for id in new_ticket_ids:
                UpdateUploader().uploadNewTicket(id)
            print("New Tickets uploaded!")
        else:
            print("No new Tickets found!")

        # Delete chunks that are too short, duplicates, substrings, table of contents, no spaces, trash
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).delete_short_chunks()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_duplicates_from_databases()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_substrings_from_database()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_table_of_contents_manuals()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_chunks_with_no_spaces()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_trash_chunks()

        print("Sleeping for " + str(time_interval/60/60) + " hours")

        UpdateUploader().fetchingStagingPDB()
        PDBSetup(sql_connection=sql_connection).settingUpPDB()
        PDBSetup(sql_connection=sql_connection).pushingNewFeaturesToPinecone()

        # Manual are uploaded with Frontend
        time.sleep(time_interval)

# Update every 24 hours
updating_loop(86400)


