from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores.pinecone import Pinecone
import pinecone
import openai
import os


os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "d589266c-40d5-4a99-a813-8166f90f11a3"

def pdf_to_chunks(path, file_name):
    loader = PyPDFLoader(path)

    #split into pages
    pages = loader.load_and_split()

    #initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
    #split pages into chunks
    chunks = text_splitter.split_documents(pages)
    print(chunks)
    print("Pdf turned into chunks")
    return pages, chunks 

#create Embeddings from chunks
def createEmbeddingsAndVectorstore(pages, chunks, file_name):
    #create Embeddings
    embeddings = OpenAIEmbeddings()
    
    # initialize pinecone
    pinecone.init(
        api_key="ddafaa1a-777c-4f6d-b61d-cc8f962ddf64",  
        environment="us-west4-gcp"  
    )
    index_name = "pdfreader"

    print(file_name)
   
    Pinecone.from_texts([file_name], embeddings, index_name=index_name, namespace="pdf_names")
    #Pinecone.from_documents(file_name, embeddings, index_name=index_name, namespace="pdf_names")
    Pinecone.from_documents(chunks, embeddings, index_name=index_name, namespace=file_name)
    print("pdf turned into embeddings & uploaded to pinecone")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


#main
def pdf_to_pinecone(path, file_name):
    pages, chunks = pdf_to_chunks(path, file_name)
    createEmbeddingsAndVectorstore(pages, chunks, file_name)
