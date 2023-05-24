import tiktoken
from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

from Ticket import Ticket
from Chunk import Chunk




class TicketChunker:

    def ticket_to_chunks(self, ticket_object):
        chunkList = []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function=self.tiktoken_len,
            separators=['\n\n', '\n', ' ', '']
        )
        ticketText = ticket_object.get_fullTicketText()
        chunks = text_splitter.split_text([ticketText])

        for chunk in range(0, len(chunks)):
            chunkList.append(Chunk(Text=chunks[chunk], Ticket=ticket_object.get_TicketID(),
                                   Order=chunk+1))

        print("Ticket turned into chunks")
        return chunkList

    def tiktoken_len(self,text):
        # maybe woanders die varaible erstellen
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)

    def ticketChunkToJson(self,chunks):
        listOfJson = []
        for chunk in chunks:
            jsonChunk = {"content": str(chunk.get_Text()),
                         "metadata":{
                             "type": "Ticket", 
                             "TicketID": str(chunk.get_Ticket()),
                             "order in ticket: " : str(chunk.get_Order())}
                         }
            listOfJson.append(jsonChunk)
        return listOfJson

    def chunkTicket(self,ticket_object):
         chunks = self.ticket_to_chunks(ticket_object)
         jsonChunks = self.ticketChunkToJson(chunks)
         return jsonChunks
