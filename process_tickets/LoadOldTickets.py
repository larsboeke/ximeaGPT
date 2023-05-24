import requests
import json
import csv
class LoadOldTickets:
    # file_path = 'output.csv'
    # HEADER = {"Authorization": "key 5:9ZJG366BBM9WZ8YPSTBXKPPW3"}


    def __init__(self,file_path,header):
        self.file_path = file_path
        self.header=header
        self.ticket_handler_main()


    def ticket_handler_main(self):
        url = 'https://desk.ximea.com/api/v2/tickets'

        n_pages = self.get_pages(url =url)
        print(n_pages)
        #n_pages = 10
        ids = self.get_ids(url=url, pages=n_pages)


    def get_pages(self,url):
        #global header
        response = requests.get(url, headers=self.header).json()
        # Get the number of total_pages
        number_pages = int(response['meta']['pagination']['total_pages'])
        return number_pages


    def get_ids(self,url, pages):
        #global file_path
        with open(self.file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            id = []
            for i in range(1, pages+1):
                params = {"page": i}
                response = requests.get(
                    url=url, headers=self.header, params=params).json()
                print(str(i), "request done")
                number_elements = response['meta']['pagination']['count']

                for j in range(0, number_elements):
                    if response['data'][j]['status'] == 'resolved':
                        writer.writerow([response['data'][j]['id']])

LoadOldTickets(file_path='output.csv',header={"Authorization": "key 5:9ZJG366BBM9WZ8YPSTBXKPPW3"})
