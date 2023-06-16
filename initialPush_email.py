from .URL_Handler import manuals
import uploadData
from process_emails_old.get_cases_from_db import get_all_cases
from process_tickets.resolved_ids import ticket_ids

# Approx 42€ total costs

# Upload Emails
# Approx costs 0,0004 * 0,4 * 8 * 29 750
iter=0
for case in get_all_cases():
    uploadData.uploadMail(case)
    iter += 1
    print("Uploaded case ", iter, " / ", len(get_all_cases()))