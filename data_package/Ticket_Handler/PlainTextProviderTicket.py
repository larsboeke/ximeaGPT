from bs4 import BeautifulSoup
from data_package.Ticket_Handler.Ticket import Ticket
import re

class PlainTextProviderTicket:

    def convert_html_to_text(self, data):
        """
        Converts HTML to text
        :param data: HTML data
        :return data: text data
        """
        if isinstance(data, str):
            # HTML-Tags in normalen Text umwandeln
            soup = BeautifulSoup(data, 'html.parser')
            text = soup.get_text(separator='\n')
            # Leere Zeilen entfernen
            text = '\n'.join(
                line for line in text.splitlines() if line.strip())
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


    def getText(self, ticket: Ticket):
        """
        Returns the text of a ticket
        :param ticket:
        :return text: text of the ticket
        """
        text = ""
        countmessage = 0
        for page in range(0, len(ticket.TicketContent)):
            for message in range(0, len(ticket.TicketContent[page]['data'])):
                countmessage += 1
                text += ('\n' + f'This is Message {countmessage}'.center(70, '.') + '\n' +
                         self.convert_html_to_text((ticket.TicketContent)[page]['data'][message]['message']))
        return text



