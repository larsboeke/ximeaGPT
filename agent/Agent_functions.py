import pymongo
import pinecone
import openai
import pymssql
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import tiktoken

load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

get_context_tool = {
                "name": "query_past_conversations",
                "description": "Get Context from past conversations that already happend with real customers to. ONLY USE THIS TOOL ONCE IN A QUERY",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to find similar contexts to",
                        },
                    },
                    "required": ["query"],
                },
            }

query_maunals = {
                "name": "query_manuals",
                "description": "Query technical manuals to get technical information. ONLY USE THIS TOOL ONCE IN A QUERY",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to gather technical information about",
                        },
                    },
                    "required": ["query"],
                },
            }

get_database_schema = {
            "name": "get_database_schema",
            "description": "Get the schema of the transact-SQL database of XIMEA. ",
            "parameters": {
                "type": "object",
                "properties": {
                    "empty_string": {
                        "type": "string",
                        "description": "empty_string e.g '' ",
                    },
                },
                "required": [],
            },
}

query_product_database = {
            "name": "query_product_database",
            "description": "Get the result back from a valid transact-SQL query on XIMEAs Product-database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlquery": {
                        "type": "string",
                        "description": "Valid transact-SQL syntax, e.g. SELECT TOP (10) [id_product], [name_of_product], [description] FROM [AI:Lean].[dbo].[product]",
                    },
                },
                "required": ["sqlquery"],
            },
        }

get_last_message = "pass"

 

tools = [get_context_tool, query_maunals]

database_schema = """ 
CREATE TABLE [dbo].[feature](
	[id_feature] [int] NULL,
	[name_of_feature] [nvarchar](45) NULL,
	[gentl_name] [nvarchar](145) NULL,
	[api_name] [nvarchar](145) NULL,
	[datatype] [nvarchar](45) NULL,
	[tooltip] [nvarchar](245) NULL,
	[description] [nvarchar](245) NULL,
	[display_name] [nvarchar](245) NULL,
	[access_mode] [nvarchar](45) NULL,
	[visibility_level] [nvarchar](45) NULL,
	[type_of_value] [nvarchar](45) NULL,
	[maximum_values] [nvarchar](245) NULL,
	[minimum_values] [nvarchar](245) NULL,
	[increment_values] [nvarchar](245) NULL,
	[length] [nvarchar](45) NULL,
	[port] [nvarchar](45) NULL,
	[signature] [nvarchar](45) NULL,
	[unit] [nvarchar](45) NULL,
	[namespace] [nvarchar](45) NULL,
	[command_value] [nvarchar](45) NULL,
	[default_value] [nvarchar](145) NULL,
	[gentl_pmax] [nvarchar](145) NULL,
	[gentl_pmin] [nvarchar](145) NULL,
	[streamable] [nvarchar](145) NULL,
	[register] [nvarchar](145) NULL,
	[generate_register] [nvarchar](145) NULL,
	[handler_function] [nvarchar](145) NULL,
	[available_sk] [nvarchar](145) NULL,
	[lock_while_acq] [nvarchar](145) NULL,
	[cal_en] [nvarchar](145) NULL,
	[cal_rtg] [nvarchar](145) NULL,
	[xp_en] [nvarchar](10) NULL,
	[xp_ext_en] [nvarchar](145) NULL,
	[app_def] [nvarchar](145) NULL,
	[polling_time] [nvarchar](145) NULL,
	[string_is_path] [nvarchar](145) NULL,
	[supported_file_format] [nvarchar](145) NULL,
	[web_link] [nvarchar](145) NULL,
	[flags] [nvarchar](145) NULL,
	[p_selected] [nvarchar](245) NULL,
	[value_description] [nvarchar](245) NULL,
	[invalidates_all_params] [nvarchar](145) NULL,
	[web_download_type] [int] NULL
) ON [PRIMARY]

CREATE TABLE [dbo].[product_feature_relationship](
	[id] [int] NULL,
	[id_product] [int] NULL,
	[id_feature] [int] NULL,
    FOREIGN KEY (id_product) REFERENCES [dbo].[product]([id_product]),
    FOREIGN KEY (id_feature) REFERENCES [dbo].[feature]([id_feature])
) ON [PRIMARY]

CREATE TABLE [dbo].[product](
	[id_product] [int] NULL,
	[name_of_product] [nvarchar](145) NULL,
	[description] [nvarchar](500) NULL
) ON [PRIMARY]
"""

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_database_schema(empty_string = ""):
    schema = {"database": database_schema}
    return schema 

def create_connection():
    server = '192.168.11.22'
    database = 'AI:Lean'
    username = 'AI:Lean'
    password = 'NbIxyuc5b!4'

    connection = pymssql.connect(server, username, password, database)
    cursor = connection.cursor()
    return connection, cursor
def query_product_database(sqlquery):
    print(str(sqlquery))
    connection, mycursor = create_connection()
    try:
        mycursor.execute(sqlquery)      #Excecute Query Check for Errors
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()
        print(str(myresult))
        print("Length from result!")
        print(str(len(myresult)))
        print("Length of tokens from result!")
        print(str(num_tokens_from_string(str(myresult))))
        if len(myresult)> 200:
            myresult = "The query you wrote returned too much data for you to handle. Please LIMIT the amount of data you get returned or rewrite the query!"
    query_info = {
        "sqlquery": sqlquery,
        "database_response": myresult
    }
    return query_info
    


def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype4"]
    return col, db


        
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
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype4"]
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    pinecone_results = index.query([filtered_query_embedding], top_k=3, include_metadata=True, namespace=namespace)
    #validIds = []
        # try:
    #     for id in ids:
    #         if id['score'] > float(0):  #parameter anpassen
    #             validIds.append(id)
    # except:
    #     print("Pinecone query failed")


    #get matches from mongoDB for IDs
    matches_content = []
    matches_sources = []
    print(pinecone_results)
    for id in pinecone_results['matches']:
        idToFind = ObjectId(id['id'])
        match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun    
        print(match)
        # print(match['content'])
        matches_content.append(match['content'])
    
        source = {'id': str(match['_id']), 'content': match['content'], 'metadata': match['metadata']}
        matches_sources.append(source)


    return matches_content, matches_sources, used_tokens
