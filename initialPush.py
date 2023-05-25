from process_manuals import manuals
import uploadData
from process_emails.get_cases_from_db import get_all_cases
from process_tickets.resolved_ids import ticket_ids


# Upload Emails
anzahl_cases = len(get_all_cases())
for case in get_all_cases():
    uploadData.uploadMail(case)

# Upload URLs
for url in manuals.url_list:
    uploadData.uploadURL(url)

# Upload PDFs
for pdf in manuals.pdf_list:
    uploadData.uploadPDF(pdf)

# Upload Tickets
for id in ticket_ids:
    uploadData.uploadTicket(id)

