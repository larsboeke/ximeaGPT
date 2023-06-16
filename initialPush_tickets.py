from process_manuals import manuals
import uploadData
from process_emails_old.get_cases_from_db import get_all_cases
from process_tickets.resolved_ids import ticket_ids

# Approx 42€ total costs

# Upload Tickets
# Approx costs 0,0004 * 0,4 * 3 * 4 904
iter=0
for id in ticket_ids:
    uploadData.uploadTicket(id)
    iter += 1
    print("Uploaded case ", iter, " / ", len(ticket_ids))