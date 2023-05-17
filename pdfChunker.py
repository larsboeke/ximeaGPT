from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import tiktoken


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

def pdfChunkToJson(chunks):
    listOfJson = []

    for chunk in chunks:
        jsonChunk = {"content": chunk.page_content,
                     "type": "PDF",
                     "source": chunk.metadata["source"] + " page number: " + str(chunk.metadata["page"])}
        # {"content" : xxx, "metadaten" : "source" : xxx, "sourceID" : xxx,  "type": xxx, "page number"}
        listOfJson.append(jsonChunk)

    return listOfJson



#main
def chunkPDF(path):
    chunks = pdf_to_chunks(path)
    jsonChunks = pdfChunkToJson(chunks)
#document = {"key": "mykey", "value": "myvalue"}
    return jsonChunks


