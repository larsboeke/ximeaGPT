from upload.UpdateUploader import UpdateUploader
from data_package.resolved_ids import ticket_ids
import time


def updating_loop(time_interval):
    while True:
        # Upload new email cases and update existing email cases
        UpdateUploader().update_new_cases_and_updated_cases()
        print("All Emails uploaded!")

        # get new resolved tickets and save to resolved_ids.py
        # TODO: get new resolved tickets and save to resolved_ids.py

        # Upload new manuals and update existing manuals
        for id in ticket_ids:
            UpdateUploader().uploadNewTicket(id)

        # Manual are uploaded with Frontend
        time.sleep(time_interval)

# Update every 24 hours
updating_loop(86400)


