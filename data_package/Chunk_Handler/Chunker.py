from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from data_package.Chunk_Handler.Chunk import Chunk

class Chunker:
    
    def data_to_chunks(self, content, metadata):
        """
        Turn the data into chunks
        :param content:
        :param metadata:
        :return chunk_list: list of chunks
        :rtype: list
        """
        chunk_list = []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50,
            length_function= self.tiktoken_len,
            separators=['\n\n\n', '\n\n', '\n', '.', ' ', '']
        )
        chunks = text_splitter.split_text(content)

        metadata["order_id"] = 0
        for index, chunk in enumerate(chunks):
            metadata["order_id"] = index
            jsonChunk = {"content": chunk,
                        "metadata": metadata
                        }
            chunk_list.append(jsonChunk)


        #print("Email turned into chunks")
        return chunk_list


    def tiktoken_len(self, text):
        """
        Get the length of the text
        :param text:
        :return length: length of the text
        :rtype: int
        """
        # maybe woanders die varaible erstellen
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    #Currently not in use due to design decision
    def chunk_to_json(self, chunks):
        """
        Turn the chunks into json with content and metadata
        :param chunks:
        :return listOfJson: list of json
        :rtype: list
        """
        listOfJson = []

        for chunk in chunks:
            jsonChunk = {"content": chunk.content,
                        "metadata": chunk.metadata
                        }
            listOfJson.append(jsonChunk)

        return listOfJson



