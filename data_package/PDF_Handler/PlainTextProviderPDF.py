from data_package.PDF_Handler.PDF import PDF
from data_package.Chunk_Handler.Chunker import Chunker
import requests
import os
from langchain.document_loaders import PyPDFLoader
import re

class PlainTextProviderPDF:

    def get_text(self, pdf:PDF):
        """
        Returns the plain text of the PDF
        :param pdf:
        :return text:
        """
        path = pdf.get_path()
        # Download the PDF file
        response = requests.get(path)
        response.raise_for_status()

        # Create a temporary file to save the downloaded PDF
        with open('temp.pdf', 'wb') as file:
            file.write(response.content)

        loader = PyPDFLoader('temp.pdf')

        # split into pages
        pages = loader.load_and_split()
        
        os.remove('temp.pdf')

        text= ""
        for page in pages:
            text += page.page_content
            text += "\n"

        return text

    def get_text_local(self, pdf: PDF):
        """get the text of a local stored pdf or one that was uploaded by a user"""

        path = pdf.get_path()
        loader = PyPDFLoader(path)
        # split into pages
        pages = loader.load_and_split()
        text = ""
        for page in pages:
            text += page.page_content
            text += "/n"

        return text