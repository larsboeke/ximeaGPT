from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import os
import tiktoken
import uploadData

os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "d589266c-40d5-4a99-a813-8166f90f11a3"

def pdf_to_chunks(path):
    loader = PyPDFLoader(path)

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
    return chunks

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base') # maybe woanders die varaible erstellen
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)




#main
def chunkPDF(path):
    chunks = pdf_to_chunks(path)
#document = {"key": "mykey", "value": "myvalue"}
    for chunk in chunks:
        uploadData.uploadChunk(chunk)


