from data_package.PDF_Handler.PDF import PDF
from data_package.Chunk_Handler.Chunker import Chunker
import requests
import os
from langchain.document_loaders import PyPDFLoader
import re

class PlainTextProviderPDF:

    def get_text(self, pdf:PDF):

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


# path = manuals.pdf_list[0]
# pdf = PDF(path=path)
# plainString = PlainTextProviderPDF().get_text(pdf)
# chunks = Chunker().data_to_chunks(plainString, pdf.get_metadata())
# print(chunks)
# print(chunks[0])