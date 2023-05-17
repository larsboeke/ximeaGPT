from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from bson.objectid import ObjectId
import openai
import pinecone
import pymongo
import os
import pyodbc

OPEN_API_KEY = os.getenv("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")

#query all conversational data Tool Class
class getContextTool(BaseTool):
    name = "get Context Tool"
    description = "Use this tool to query past conversations and find similar contexts to answer the question"

    def _run(self, query: str):
        #queries in namespace "pastConversations"
        context = getText(query, "pastConversations")

        return context
    
    def _arun(self, query: str):
        return NotImplementedError("This tool does not support async.")

class queryManuals(BaseTool):
    name = "query Manuals"
    description = "Use this tool if you want to query the product manuals."


    def _run(self, query: str):
        #queries in "manuals" namespace
        context = getText(query, "manuals")

        return context
    
    def _arun(self, query: str):
        return NotImplementedError("This tool does not support async.")
    
class queryPDB(BaseTool):
    name = "query Product Database"
    description = "Use this tool if you want to query the product database to recive structured. Use a SQL Query as an Input. The Database has the following structure: " #anpassen

    def _run(self, query: str):
        server='server name'
        database='database name'
        username='username'
        password='password'

        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server}'
            f'DATABASE={database}'
            f'UID={username}'
            f'PWD={password}'
        )

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

    def _arun(self, query: str):
        return NotImplementedError("This tool does not support async.")


#initialize LLM
llm = ChatOpenAI(
    openai_api_key=OPEN_API_KEY,
    temperature=0,
    model_name='gpt-3.5-turbo'
)

#initialize conversational momory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

#List of Tools
tools = [
    getContextTool(),
    queryManuals(),
    queryPDB(),
    ]

#initialize agent
agent = initialize_agent(
    agent='Chat Agent',
    tools=tools,
    llm=llm,
    verbose=True, #for testing purposes
    max_iterations = 3, #max steps of reasoning before stopping
    early_stopping_method='generate', #model should decide when to stop
    memory=conversational_memory
)

def getText(query, namespace):
    index = pinecone.Index("ailean")
    #initialize mongoDB
    client = pymongo.MongoClient("adress")
    db = client["mydatabase"]                   #Ändern
    col = db["collection"]

    query_embedding = openai.Embedding.create(input=query, engine='text-embedding-ada-002')['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    ids = index.query([query_embedding], top_k=3, include_metadata=True, namespace=namespace)
    validIds = []
    for id in ids:
        if id['score'] > 0:  #parameter anpassen
            validIds.append(id)

    #get matches from mongoDB for IDs
    matches = []
    for id in validIds:
        idToFind = ObjectId(id)
        match = col.find_one({'_id' : idToFind})
        if match:    
            matches.append(match)
        else:
            print("No match found for ID: " + id)

    return matches