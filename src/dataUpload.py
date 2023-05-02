from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores.pinecone import Pinecone
import pinecone
import openai
import os
import sqlOperations
from uuid import uuid4


class dataUpload:

    def __init__(self, data, isPdf):
        self.data = data
        self.isPdf = isPdf
    
        
    

    #generate Chunks from Data
    def generateChunks(self):
        #initialize text slpitter
        textSplitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len,
        )
        #checks if data is pdf
        if self.getIsPdf():
            loader = PyPDFLoader(self.getData())

            #split into pages
            pages = loader.load_and_split()

          
            #split pages into chunks and save in attribute
            self.setChunks(textSplitter.split_documents(pages))

        else:
            #for not pdf texts
            self.setChunks(textSplitter.split_text(self.getData))
            


    def generateEmbeddings(self):

        embeddings = []
        #generating embeddings for each chunk and store in embeddings list
        for chunk in self.getChunks():
            embedding = openai.Embedding.create(input=chunk, engine='text-embedding-ada-002')['data'][0]['embedding']
            embeddings.append(embedding)
            


    def generateIDs(self):
        IDs = []
        for embedding in self.getEmbeddings():
            IDs.append(uuid4())
        self.setIDs(IDs)

    def generatePineconeData(self):
        dataset = []
        i = 0
        for embedding in self.getEmbeddings():
            data = (self.getIDs()[i], self.getEmbeddings()[i])
            dataset.append(data)
            i += 1

        self.setPineconeData(dataset)


    def uploadData(self):
        #upload embeddings
        index = pinecone.Index("ailean")
        index.upsert(self.getPineconeData())
        

        #sqlupload



    #getter & setter
    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data
    
    def setChunks(self, chunks):
        self.chunks = chunks

    def getChunks(self):
        return self.chunks
    
    def setEmbeddings(self, embeddings):
        self.embeddings = embeddings

    def getEmbeddings(self):
        return self.embeddings
    
    def setIndexes(self, indexes):
        self.indexes = indexes

    def getIndexes(self):
        return self.indexes
    
    def setIsPdf(self, isPdf):
        self.isPdf = isPdf

    def getIsPdf(self):
        return self.isPdf
    
    def setIDs(self):
        self.id = id

    def getIDs(self):
        return self.id
    
    def setPineconeData(self, dataset):
        self.pineconeData = dataset

    def getPineconeData(self):
        return self.pineconeData
    

    class Chunk:
        def __init__(self, content, date, communicationPartner, source):
            self.id = uuid4()
            self.content = content
            self.date = date
            self.communicationPartner = communicationPartner
            self.source = source

     