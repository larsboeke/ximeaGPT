from process_manuals import manuals
import uploadData
from process_emails.get_cases_from_db import get_all_cases
from process_tickets.resolved_ids import ticket_ids


# Upload Emails
iter=0
for case in get_all_cases():
    uploadData.uploadMail(case)
    iter += 1
    print("Uploaded case " + iter + " / " + len(get_all_cases()))

# Upload URLs
iter=0
for url in manuals.url_list:
    uploadData.uploadURL(url)
    iter += 1
    print("Uploaded case " + iter + " / " + len(manuals.url_list))

# Upload PDFs
iter=0
for pdf in manuals.pdf_list:
    uploadData.uploadPDF(pdf)
    iter += 1
    print("Uploaded case " + iter + " / " + len(manuals.pdf_list))

# Upload Tickets
iter=0
for id in ticket_ids:
    uploadData.uploadTicket(id)
    iter += 1
    print("Uploaded case " + iter + " / " + len(ticket_ids))