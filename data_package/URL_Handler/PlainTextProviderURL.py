from .URL import URL
import requests
import os
from bs4 import BeautifulSoup
from Chunk_Handler.Chunker import Chunker

class PlainTextProviderURL:

    def get_text(self, url:URL):
        response = requests.get(url.get_path())
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        text = os.linesep.join([s for s in text.splitlines() if s])
        return text

