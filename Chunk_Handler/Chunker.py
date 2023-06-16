from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import OnlinePDFLoader
import tiktoken
from Chunk_Handler.Chunk import Chunk
from langchain.text_splitter import TokenTextSplitter
import requests
import os

class Chunker:
    
    def data_to_chunks(self, text, metadata):
        text_splitter = RecursiveCharacterTextSplitter(
        # encoding_name='cl100k_base',
        chunk_size=800,
        chunk_overlap=50,
        length_function=Chunker.tiktoken_len,
        separators=['\n\n\n', '\n\n', '\n', ' ', '']
    )
        # split pages into chunks
        chunks = text_splitter.split_text(text)

        json_list = []
        for chunk in chunks:
            json_chunk = {"content": chunk,
                        "metadata": metadata
                        }
            Chunk(json_chunk)
        json_list.append(json_chunk)

        return chunks

    def tiktoken_len(text):
        tokenizer = tiktoken.get_encoding('cl100k_base')  # maybe woanders die varaible erstellen
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)