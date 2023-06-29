from Uploader import Uploader
from data_package import manual_url_list

#Uploader().uploadMails()

"""iter=0
for path in manual_url_list.pdf_list:
    Uploader().uploadPDF(path)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.pdf_list))"""

iter=0
for url in manual_url_list.url_list:
    Uploader().uploadURL(url)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.url_list))
