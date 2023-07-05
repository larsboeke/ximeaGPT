from upload.Uploader import Uploader
from data_package.PDF_Handler import manual_list

iter=0
for path in manual_list.pdf_list:
    Uploader().uploadPDF(path)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_list.pdf_list))

print("All Manuals uploaded!")