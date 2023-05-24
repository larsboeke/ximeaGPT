from langchain.text_splitter import RecursiveCharacterTextSplitter
from .get_message import get_full_message_from_one_case
import tiktoken


# Input: Case history in String format
def email_to_chunks(case):

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

    #print("Case split into chunks")
    return chunks

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
                     "metadata": metadata
                     }
        # metadata example:
        # type": "email",
        # "case_id": str(act_desc_tuple[0][2]),
        # "activity_id": [str(t[0]) for t in act_desc_tuple],
        # "document_date": formatted_dates

        listOfJson.append(jsonChunk)

    return listOfJson



#main
def chunk_email(case):
    messages, metadata = get_full_message_from_one_case(case)
    chunks = email_to_chunks(messages)
    jsonChunks = email_chunk_to_json(chunks, metadata)
    #document = {"key": "mykey", "value": "myvalue"}
    return jsonChunks


