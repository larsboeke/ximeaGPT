from upload.Uploader import Uploader
from data_package import resolved_ids

iter = 0
for id in resolved_ids.ticket_ids:
    Uploader().uploadTicket(id)
    iter += 1
    print("Uploaded Ticket ", iter, " / ", len(resolved_ids.ticket_ids))

print("All Tickets uploaded!")