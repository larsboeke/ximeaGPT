from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
from bson.objectid import ObjectId
import openai
import pinecone
import pymongo
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

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
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model_name=GPT_MODEL
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
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True, #for testing purposes
    max_iterations = 3, #max steps of reasoning before stopping
    early_stopping_method='generate', #model should decide when to stop
    memory=conversational_memory
)

def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype"]
    return col
        
def initPinecone():
    #init pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
    index = pinecone.Index(PINECONE_INDEX_NAME)
    return index

def getText(query, namespace):
    index = initPinecone() #
    #initialize mongoDB
    col = initMongo()

    query_embedding = openai.Embedding.create(input=query, engine=EMBEDDING_MODEL)['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    ids = index.query([query_embedding], top_k=3, include_metadata=True, namespace=namespace)
    validIds = []
    print(ids)
    try:
        for id in ids:
            if id['score'] > 0:  #parameter anpassen
                validIds.append(id)
    except:
        print("Pinecone query failed")


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