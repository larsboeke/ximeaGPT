
import requests
import json
from bs4 import BeautifulSoup

class Ticket:
    
    def __init__(self, TicketID):
        self.TicketID = TicketID
        self.WholeTicket = []
        self.fullTicketText = ""
        self.metadata ={},
        self.ticketStartDate = None

    def set_metadata(self):
        self.metadata = {
            'ticketID': self.WholeTicket[0]['data'][0]['ticket'],
            'countMessages': self.WholeTicket[0]['meta']['pagination']['total'],
        }

    def set_fullTicketText(self):
        countmessage = 0
        for page in range(0, len(self.WholeTicket)):
            for message in range(0, len(self.WholeTicket[page]['data'])):
                countmessage += 1
                self.fullTicketText += ('\n' + f'This is Message {countmessage}'.center(70, '.') + '\n' +
                                        self.convert_html_to_text((self.WholeTicket)[page]['data'][message]['message']))

    def set_WholeTicket(self):
        """returns List containing Dictionaries. Each Dictionary contains content of one ticket page"""

        url = f'https://desk.ximea.com/api/v2/tickets/{self.TicketID}/messages'
        header = {'Accept': 'application/json',
                  'Authorization': 'key 5:9ZJG366BBM9WZ8YPSTBXKPPW3'}

        page = 1
        while True:
            response = requests.get(url, headers=header, params={"page": page})

            if not response:
                break
            ticket = json.loads(response.content)
            self.WholeTicket.append(ticket)
            page += 1

    def convert_html_to_text(self,data):
        if isinstance(data, str):
            # HTML-Tags in normalen Text umwandeln
            soup = BeautifulSoup(data, 'html.parser')
            text = soup.get_text(separator='\n')
            return text
        elif isinstance(data, list):
            # Rekursiv durch die Liste gehen und jedes Element umwandeln
            return [self.convert_html_to_text(item) for item in data]
        elif isinstance(data, dict):
            # Rekursiv durch das Dictionary gehen und jedes Element umwandeln
            return {key: self.convert_html_to_text(value) for key, value in data.items()}
        else:
            # Wenn der Wert weder ein String noch eine Liste noch ein Dictionary ist, ihn einfach zurückgeben
            return data

    def get_WholeTicket(self):
        return self.WholeTicket

    def get_metadata(self):
        return self.metadata

    def get_fullTicketText(self):
        return self.fullTicketText

    def get_TicketID(self):
        return self.TicketID
