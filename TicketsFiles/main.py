import requests
import json
import csv
from langchain.text_splitter import TokenTextSplitter
from Chunk import Chunk
from Ticket import Ticket
from TicketChunker import TicketChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter


#from LoadOldTickets import LoadOldTickets

class main:

    def __init__(self):
       a = Ticket(53483)
       a.set_WholeTicket()
       a.set_metadata()
       a.set_fullTicketText()

       b = TicketChunker()
       d = b.chunkTicket(a)
       for i in d:
           print(i)
       
 
    def save_oldData(init):
        file_path = 'C:/Users/mimgh/OneDrive/Desktop/OneDrive/Main Page/PYTHON/Lists/APIs_Lernen/TestsAPI/XimeaTickets/output.csv'

        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            linecount=0
            max=100
            for line in reader:
                number = int(line[0])  # Assuming the number is in the first column
                if linecount<max:
                    # Use the extracted number for further processing
                    print(line)
                    linecount +=1
                else:
                    break

main()


#    def splittext(text):
#         text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=200)
#         return text_splitter.split_text(text)

