from upload.Uploader import Uploader
from data_package.URL_Handler import url_list

iter=0
for url in url_list.url_list:
    Uploader().uploadURL(url)
    iter += 1
    print("Uploaded case ", iter, " / ", len(url_list.url_list))

print("All URLs uploaded!")