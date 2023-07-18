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

database_schema = """ 
CREATE TABLE [dbo].[feature](
	[id_feature] [int] NULL,
	[name_of_feature] [nvarchar](45) NULL,
	
	[description] [nvarchar](245) NULL,
	[display_name] [nvarchar](245) NULL,
	
) ON [PRIMARY]


CREATE TABLE [dbo].[product_feature_relationship](
	[id] [int] NULL,
	[id_product] [int] NULL,
	[id_feature] [int] NULL,
    FOREIGN KEY (id_product) REFERENCES [dbo].[product]([id_product]),
    FOREIGN KEY (id_feature) REFERENCES [dbo].[feature]([id_feature])
) ON [PRIMARY]

3 rows from the product_feature_relationship table:
id	id_product	id_feature
18	1	8
407	2	8
409	4	8

CREATE TABLE [dbo].[product](
	[id_product] [int] NULL,
	[name_of_product] [nvarchar](145) NULL,
	[description] [nvarchar](500) NULL
) ON [PRIMARY]

3 rows from the product table:
id_product	name_of_product	description
1	MR274CU_BH	
2	MR16000MU	
3	MR282CC_BH	
"""

get_context_tool = {
                "name": "query_past_conversations",
                "description": "Get Context from past conversations that already happend with real customers to.",
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

query_manuals = {
                "name": "query_manuals",
                "description": "Query technical manuals to get technical information.",
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

query_all = {
                "name": "query_unstructured_data",
                "description": "Query unstructed data to get context from past conversations with customers and technical manuals.",
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

# Fucntions for the PDB
query_feature_of_product_pdb = {
                "name": "query_feature_of_product_pdb",
                "description": "Query for features of a specific product in XIMEA'S product database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                    },
                    "required": ["product"],
                },
            }

query_data_of_feature_of_product_pdb = {
                "name": "query_data_of_feature_of_product_pdb",
                "description": "Query for the data of a category of a specific feature of a product in XIMEA'S product database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the product of which we want to know more about a specific feature. Product in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                        "feature" : {
                            "type": "string",
                            "description": "This is the feature of which we want to know specific information. Features in the database are for example: TriggerMode, LUTValue, xiAPI Loopback Trigger Support, xiapi_UsedFFSSize",
                        },
                        "category" : {
                            "type": "string",
                            "description": "This is the catergory of information about the feature. The possible categories are: id_feature, name_of_feature, gentl_name, api_name, datatype, tooltip, description, display_name, access_mode, visibility_level, type_of_value, maximum_values, minimum_values, increment_values, length, port, signature, unit, namespace, command_value, default_value, gentl_pmax, gentl_pmin, streamable, register, generate_register, handler_function, available_sk, lock_while_acq, cal_en, cal_rtg, xp_en, xp_ext_en, app_def, polling_time, string_is_path, supported_file_format, web_link, flags, p_selected, value_description, invalidates_all_params, web_download_type",
                        },
                    },
                    "required": ["product", "feature", "category"],
                },
            }

get_last_message = "pass"




tools = [
    query_all,
    query_feature_of_product_pdb,
    query_data_of_feature_of_product_pdb,

]

def query_data_of_feature_of_product_pdb(product, feature, category):
    print(product)
    query = f"""
            SELECT f.[{category}]
            FROM [AI:Lean].[dbo].[feature] f 
            INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
            ON f.id_feature = pfr.id_feature 
            INNER JOIN [AI:Lean].[dbo].[product] p 
            ON pfr.id_product = p.id_product 
            WHERE p.name_of_product = '{product}' AND f.name_of_feature = '{feature}'
            """
    connection, mycursor = create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()
        print(str(myresult))
    matches_sources = []
    source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    matches_sources.append(source)
    return myresult, matches_sources


def query_feature_of_product_pdb(product):
    print(product)
    query = f"""
            SELECT f.name_of_feature
            FROM [AI:Lean].[dbo].[feature] f 
            INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
            ON f.id_feature = pfr.id_feature 
            INNER JOIN [AI:Lean].[dbo].[product] p 
            ON pfr.id_product = p.id_product 
            WHERE p.name_of_product = '{product}'
            """
    connection, mycursor = create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()
        print(str(myresult))

        # messages=[
        #     {"role": "user", "content": f"T-SQL query: {query}, Answer: {myresult}"},
        #     {"role": "system", "content": f"Your are a helpfull assistent who will turn a T-SQL query and it answer into a text."}
        # ]
    
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=messages,
        # )
        # myresult = response["choices"][0]["message"]
    matches_sources = []
    source = {'id': "1", 'content': query, 'metadata': {'type': "Product_Database"}}
    matches_sources.append(source)
    return myresult, matches_sources

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def create_connection():
    server = '192.168.11.22'
    database = 'AI:Lean'
    username = 'AI:Lean'
    password = 'NbIxyuc5b!4'

    connection = pymssql.connect(server, username, password, database)
    cursor = connection.cursor()
    return connection, cursor

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

def getText(query, counter):
    index = initPinecone() #
    #initialize mongoDB
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype4"]
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    #queries pinecone in namespace "manuals"
    
    matches_content = []
    matches_sources = []
    
    namespaces = [("pastConversations", [0, 2, 4, 6]), ("manuals", [0, 1, 2, 3])]
    for namespace, borders in namespaces:

        pinecone_results = index.query([filtered_query_embedding], top_k=borders[counter], include_metadata=True, namespace=namespace)
        unique_pinecone_results = pinecone_results['matches'][borders[counter -1]:borders[counter]]
        
        print("")
        print(namespace)
        print("")
        print(unique_pinecone_results)
 

        
        #get matches from mongoDB for IDs

        print(pinecone_results)
        for id in unique_pinecone_results:
            idToFind = ObjectId(id['id'])
            match = col.find_one({'_id' : idToFind}) #['content'] #Anpassen!!! und source retrun    
            print(match)
            # print(match['content'])
            matches_content.append(match['content'])
        
            source = {'id': str(match['_id']), 'content': match['content'], 'metadata': match['metadata']}
            matches_sources.append(source)


    return matches_content, matches_sources, used_tokens
