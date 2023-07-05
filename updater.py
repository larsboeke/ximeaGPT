import time
from upload.UpdateUploader import UpdateUploader
from data_package.Ticket_Handler.TicketRepository import TicketRepository

def updating_loop(time_interval):
    while True:
        # Upload new email cases and update existing email cases
        UpdateUploader().upload_new_cases_and_updated_cases()
        print("All Emails uploaded!")

        # get new resolved tickets and save to ticket_ids.py
        # TODO: check if working
        new_ticket_ids = TicketRepository().get_new_ids(pages=TicketRepository().count_pages())

        # Upload new manuals and update existing manuals
        if len(new_ticket_ids) > 0:
            for id in new_ticket_ids:
                UpdateUploader().uploadNewTicket(id)
            print("New Tickets uploaded!")
        else:
            print("No new Tickets found!")
        # Manual are uploaded with Frontend
        time.sleep(time_interval)

# Update every 24 hours
updating_loop(86400)


