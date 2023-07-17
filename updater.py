import time
from upload.UpdateUploader import UpdateUploader
from data_package.Ticket_Handler.TicketRepository import TicketRepository
from upload.DatabaseCleaner import DatabaseCleaner
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider

def updating_loop(time_interval):
    """
    Loop to update the databases with new emails and tickets
    :param time_interval:
    """
    while True:
        mongodb_connection = MongoDBConnectionProvider().initMongoDB()
        pinecone_connection = PineconeConnectionProvider().initPinecone()

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

        # Delete short chunks and remove duplicates from databases
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).delete_short_chunks()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_duplicates_from_databases()
        DatabaseCleaner(mongodb_connection=mongodb_connection, pinecone_connection=pinecone_connection).remove_substrings_from_database()

        print("Sleeping for " + str(time_interval/60/60) + " hours")
        # Manual are uploaded with Frontend
        time.sleep(time_interval)

# Update every 24 hours
updating_loop(86400)


