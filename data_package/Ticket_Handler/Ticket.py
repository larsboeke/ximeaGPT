"""
Ticket Klasse: Da die Metadaten der Tickets erst identifiziert werden können,
nachdem der Request bei der API erstellt wurde, geschieht dies bereits in dieser Klasse
"""
import requests
import json


class Ticket:
    def __init__(self, ticketID):
        self.TicketID = ticketID
        self.TicketContent = []
        self.metadata = {"type": "ticket",
                         "source_id": str(ticketID),
                         "ticket_start_date": None,
                         "number_of_messages": None}

        self.set_TicketContent()
        self.set_NumberOfMessages()
        self.set_ticketStartDate()



    def get_TicketID(self):
        return self.TicketID
    
    def get_metadata(self):
        return self.metadata

    def set_NumberOfMessages(self):
        self.metadata["number_of_messages"] = self.TicketContent[0]['meta']['pagination']['total']
    
    def set_ticketStartDate(self):
        self.metadata["ticket_start_date"] = self.TicketContent[0]['data'][0]['date_created']
    
    def set_TicketContent(self):
        """Methode gibt eine Liste zurück, die Dictionaries beinhaltet. 
        Jedes Dictionary beinhaltet den Inhalt einer Ticketseite """

        # Anfrage an die API
        url = f'https://desk.ximea.com/api/v2/tickets/{self.metadata["source_id"]}/messages'
        header = {'Accept': 'application/json',
                  'Authorization': 'key 5:9ZJG366BBM9WZ8YPSTBXKPPW3'}

        page = 1
        while True:
            response = requests.get(url, headers=header, params={"page": page})

            if not response:
                break
            ticket = json.loads(response.content)
            self.TicketContent.append(ticket)
            page += 1




