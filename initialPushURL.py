from upload.Uploader import Uploader
from data_package import manual_url_list


iter=0
for url in manual_url_list.url_list:
    Uploader().uploadURL(url)
    iter += 1
    print("Uploaded case ", iter, " / ", len(manual_url_list.url_list))

print("All URLs uploaded!")