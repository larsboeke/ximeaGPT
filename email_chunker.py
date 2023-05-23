from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import tiktoken


# Input: Case history in String format
def email_to_chunks(case, metadata):

    # initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a tiny chunk size, just to show.
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n\n', '\n\n', '\n', ' ', '']
    )
    # split text into chunks
    chunks = text_splitter.split_text(case)

    print("Case split into chunks")
    return chunks, metadata

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base') # maybe woanders die varaible erstellen
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def email_chunk_to_json(chunks, metadata):
    listOfJson = []

    for chunk in chunks:
        jsonChunk = {"content": chunk,
                     "type": "EMail",
                     "source": metadata
                     }
        # {"content" : xxx, "metadaten" : "source" : xxx, "sourceID" : xxx,  "type": xxx, "page number"}
        listOfJson.append(jsonChunk)

    return listOfJson



#main
def chunk_email(case):
    chunks = email_to_chunks(case)
    jsonChunks = email_chunk_to_json(chunks)
    #document = {"key": "mykey", "value": "myvalue"}
    return jsonChunks


