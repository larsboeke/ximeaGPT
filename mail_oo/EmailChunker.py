from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from PlainTextFromCaseProvider import PlainTextFromCaseProvider
from Chunk import Chunk
from Case import Case

class EmailChunker:
    
    def chunk_case(self,case_object):
         chunks = self.case_to_chunks(case_object)
         #jsonChunks = self.ticketChunkToJson(chunks)
         return chunks
    
    def case_to_chunks(self, case_object):
        chunkList = []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=50,
            length_function= self.tiktoken_len,
            separators=['\n\n\n', '\n\n', '\n', ' ', '']
        )
        content = PlainTextFromCaseProvider.provide_full_content(case_object)
        chunks = text_splitter.split_text(content)

        for chunk in chunks:
            chunkList.append(Chunk(chunk, case_object.metadata))

        print("Email turned into chunks")
        return chunkList


    def tiktoken_len(self, text):
        # maybe woanders die varaible erstellen
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    def email_chunk_to_json(self, chunks, metadata):
        listOfJson = []

        for chunk in chunks:
            jsonChunk = {"content": chunk,
                        "metadata": metadata
                        }
            listOfJson.append(jsonChunk)

        return listOfJson



