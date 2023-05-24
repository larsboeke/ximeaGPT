from process_manuals import manuals
import uploadData
from process_emails.get_cases_from_db import get_all_cases

# Upload PDFs
for pdf in manuals.pdf_list:
    uploadData.uploadPDF(pdf)
    print(pdf + "uploaded")

# Upload URLs
for url in manuals.url_list:
    uploadData.uploadURL(url)
    print(url + "uploaded")

# Upload Emails
i = 0
anzahl_cases = len(get_all_cases())
for case in get_all_cases():
    i += 1
    print(i + "/" + anzahl_cases + "uploaded")
    uploadData.uploadMail(case)
    if i == 40:
        break