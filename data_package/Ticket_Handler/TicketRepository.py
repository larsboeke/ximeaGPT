import requests
import csv

class TicketRepository:

    def __init__(self):
        self.file_path_old_ids = 'data_package/Ticket_Handler/old_ids.csv'
        self.url = 'https://desk.ximea.com/api/v2/tickets'
        self.header = {'Accept': 'application/json',
                       "Authorization": "key 5:9ZJG366BBM9WZ8YPSTBXKPPW3"}

    def count_pages(self):
        """
        Method that counts the number of pages of the API
        :return number_pages: number of pages
        """
        response = requests.get(self.url, headers=self.header).json()
        # Get the number of total_pages
        number_pages = int(response['meta']['pagination']['total_pages'])
        return number_pages

    def fetch_all_ids(self, pages):
        """
        Method that saves all the resolved Ticket ID's in specified csv file
        """
        all_ids = []

        for i in range(1, pages + 1):
            params = {"page": i}
            response = requests.get(
                url=self.url, headers=self.header, params=params).json()
            print(str(i), "request done")
            number_elements = response['meta']['pagination']['count']

            for j in range(0, number_elements):
                if response['data'][j]['status'] == 'resolved':
                    all_ids.append(response['data'][j]['id'])

        # schreibe all_ids mit komma getrennt in csv datei
        with open(self.file_path_old_ids, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(all_ids)

        return all_ids

    def get_new_ids(self, pages):
        """
        Method that compares the old csv file with the new csv file and returns the new ids
        :param pages:
        :return new_ids:
        """

        with open(self.file_path_old_ids, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # Convert each item in the row to an integer and save it to the list.
                old_ids = [int(item) for item in row]

        print("old_ids: ", old_ids)
        new_plus_old_ids = self.fetch_all_ids(pages=pages)
        print("new_plus_old_ids: ", new_plus_old_ids)
        # Finden Sie die Elemente in der Liste, die nicht in der CSV-Datei vorkommen
        new_ids = [id for id in new_plus_old_ids if id not in old_ids]
        print("new_ids: ", new_ids)

        return new_ids