from upload.Uploader import Uploader
from data_package import manual_url_list
from data_package import resolved_ids




Uploader().initialUploadMail()

print("All Emails uploaded!")

iter=0
for path in manual_url_list.pdf_list:
    Uploader().uploadPDF(path)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.pdf_list))

print("All Manuals uploaded!")


iter=0
for url in manual_url_list.url_list:
    Uploader().uploadURL(url)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.url_list))

print("All URLs uploaded!")

          
for id in resolved_ids.ticket_ids:
    Uploader().uploadTicket(id)
    iter += 1
    print("Uploaded Ticket ", iter, " / ", len(resolved_ids.ticket_ids))

print("All Tickets uploaded!")

