from data_package.URL_Handler.URL import URL
import requests
import os
from bs4 import BeautifulSoup


class PlainTextProviderURL:

    def get_text(self, url:URL):
        """
        Returns the plain text of a given url
        :param url:
        :return text:
        """
        response = requests.get(url.get_path())
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        text = os.linesep.join([s for s in text.splitlines() if s])
        return text

