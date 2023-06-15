from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from PlainTextFromCaseProvider import PlainTextFromCaseProvider
from Chunk import Chunk
from Case import Case

class EmailChunker:
    
    def chunk_data(self, content, metadata):
         chunks = self.data_to_chunks(content, metadata)
         #json_chunks = self.chunk_to_json(chunks)
         return chunks
    
    def data_to_chunks(self, content, metadata):
        chunk_list = []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=50,
            length_function= self.tiktoken_len,
            separators=['\n\n\n', '\n\n', '\n', ' ', '']
        )
        chunks = text_splitter.split_text(content)

        for chunk in chunks:
            jsonChunk = {"content": chunk,
                        "metadata": metadata
                        }
            chunk_list.append(jsonChunk)


        print("Email turned into chunks")
        return chunk_list


    def tiktoken_len(self, text):
        # maybe woanders die varaible erstellen
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    def chunk_to_json(self, chunks):
        listOfJson = []

        for chunk in chunks:
            jsonChunk = {"content": chunk.content,
                        "metadata": chunk.metadata
                        }
            listOfJson.append(jsonChunk)

        return listOfJson



