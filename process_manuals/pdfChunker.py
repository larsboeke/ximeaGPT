from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import OnlinePDFLoader
import tiktoken
import requests
import os
from bs4 import BeautifulSoup


def pdf_to_chunks(path):
    # Download the PDF file
    response = requests.get(path)
    response.raise_for_status()

    # Create a temporary file to save the downloaded PDF
    with open('temp.pdf', 'wb') as file:
        file.write(response.content)

    loader = PyPDFLoader('temp.pdf')

    # split into pages
    pages = loader.load_and_split()

    # initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a tiny chunk size, just to show.
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )
    # split pages into chunks
    chunks = text_splitter.split_documents(pages)
    # for page in pages:
    # chunk = text_splitter.split_text(page.page_content)
    # chunks.append(chunk)

    print("Pdf turned into chunks")
    os.remove('temp.pdf')
    return chunks


def url_to_chunks(url):
    # Download the PDF file
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text = text.replace("\n\n", " ")

    # initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a tiny chunk size, just to show.
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )
    # split pages into chunks
    chunks = text_splitter.split_text(text)
    # for page in pages:
    # chunk = text_splitter.split_text(page.page_content)
    # chunks.append(chunk)

    #print("Pdf turned into chunks")
    return chunks


def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')  # maybe woanders die varaible erstellen
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)


def pdf_chunk_to_json(chunks, path):
    listOfJson = []

    for chunk in chunks:
        jsonChunk = {"content": chunk.page_content,
                     "metadata": {
                         "type": "manuals",
                         "source": path,
                         "page number": chunk.metadata["page"]
                     }
                     }

        listOfJson.append(jsonChunk)

    return listOfJson


def url_chunk_to_json(chunks, url):
    listOfJson = []

    for chunk in chunks:
        jsonChunk = {"content": chunks,
                     "metadata": {
                         "source": url,
                         "type": "manuals",
                     }
                     }
        # {"content" : xxx, "metadaten" : "source" : xxx, "sourceID" : xxx,  "type": xxx, "page number"}
        listOfJson.append(jsonChunk)

    return listOfJson

# main
def chunkPDF(path):
    chunks = pdf_to_chunks(path)
    jsonChunks = pdf_chunk_to_json(chunks, path)

    return jsonChunks


def chunkURL(url):
    chunks = url_to_chunks(url)
    jsonChunks = url_chunk_to_json(chunks, url)

    return jsonChunks
