from upload.Uploader import Uploader
from data_package import manual_url_list



iter=0
for path in manual_url_list.pdf_list:
    Uploader().uploadPDF(path)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.pdf_list))

print("All Manuals uploaded!")