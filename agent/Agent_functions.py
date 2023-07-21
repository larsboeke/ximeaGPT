import pymongo
import pinecone
import openai
import pymssql
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
import tiktoken
from difflib import SequenceMatcher
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider


load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
GPT_MODEL = os.environ.get("GPT_MODEL")

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
                "description": "Query unstructed data to get context from past conversations with customers and technical manuals. The data store information about camera families and their specifications. This function should be used most often",
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
                "description": "Query for the features of a camera in XIMEA'S product database (PDB). Use this function if you want to check features of a camera or if you want to list features of a camera",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the camera of which you want to query the features. Camera in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                    },
                    "required": ["product"],
                },
            }

query_data_of_feature_of_product_pdb = {
                "name": "query_data_of_feature_of_product_pdb",
                "description": "Query for specific information about a feature of a camera oduct in XIMEA'S product database (PDB). Use this function if you want to query data resulting of a combination of camera and feature",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product" : {
                            "type": "string",
                            "description": "This is the camera of which we want to know more about a specific feature. Camera in the database are for example: MR282CC_BH, MC050MG-SY-FLEX, ADPT-MX-X4G2-IPASSHOST-FL, XCX-2P-X4G3-MTP",
                        },
                        "feature" : {
                            "type": "string",
                            "description": "This is the feature of which we want to know specific information.",
                        },
                    },
                    "required": ["product", "feature"],
                },
            }

query_pdb ={
            "name": "query_pdb",
                "description": "Query for information about products in XIMEA'S product database (PDB).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query of the user, you want to transform into a SQL query",
                        },
                    },
                    "required": ["query"],
                },
}


tools = [
    query_all,
    # query_product_database,
    query_feature_of_product_pdb,
    query_data_of_feature_of_product_pdb,
    # query_data_of_category_feature_of_product_pdb,
    # query_pdb
]
database = """
            CREATE TABLE [dbo].[product](
                [id_product] [int] NULL,
                [name_of_product] [nvarchar](145) NULL,
                [description] [nvarchar](500) NULL
            ) ON [PRIMARY]

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
                [id_feature] [int] NULL
            ) ON [PRIMARY]
            """


def query_pdb(query, product, feature):

    connection, mycursor = SQLConnectionProvider().create_connection()
    
    addition = "" 

    if product:
        mycursor.execute(query)
        all_products = mycursor.fetchall()
        product, score = similar(product, all_products)
        addition += f"The correct name of the product is: {product}"
        if score < 0.4:
            return "Product is not in database"
    
    if feature:
        mycursor.execute(query)
        all_features = mycursor.fetchall()
        feature, score = similar(product, all_features)
        addition += f"The correct name of the product is: {product}"
        if score < 0.4:
            return "Feature is not in database"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"You are a helpful assistant designed to turn user queries into Transact-SQL Queries. Just answer with the T-SQL query. The structure of the database is the following : {database}."},
                #{"role": "user", "content": "What is the visibility level of the feature OffsetX oft he Camera MR274CU_BH?"},
                #{"role": "assistant", "content": "SELECT f.visibility_level FROM product AS p JOIN product_feature_relationship AS pfr ON p.id_product = pfr.id_product JOIN feature AS f ON pfr.id_feature = f.id_feature WHERE p.name_of_product = 'MR274CU_BH' AND f.name_of_feature = 'OffsetX'"},
                {"role": "user", "content": query + addition}
            ],
        temperature = 0
        )
    sql_query = response["choices"][0]["message"]["content"]

    return response["choices"][0]["message"]["content"]

# print(query_pdb("List products from the PDB with a resolution more than 40 MP"))

def query_product_pdb(feature, value):
    pass


def query_data_of_feature_of_product_pdb(product, feature):

    query = f"""
            SELECT f.name_of_feature
            FROM [AI:Lean].[dbo].[feature] f 
            INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
            ON f.id_feature = pfr.id_feature 
            INNER JOIN [AI:Lean].[dbo].[product] p 
            ON pfr.id_product = p.id_product 
            WHERE p.name_of_product = '{product}'
            """
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()

        if myresult == []:
            myresult = "Product Existiert nicht in Product Datenbank"
        else:
            element, score = similar(feature, myresult)
            print(element, score)
            if score < 0.5:
                myresult = "Feature Existiert nicht in Product Datenbank"
            else:
                feature = element
    
                query = f"""
                        SELECT *
                        FROM [AI:Lean].[dbo].[feature] f 
                        INNER JOIN [AI:Lean].[dbo].[product_feature_relationship] pfr
                        ON f.id_feature = pfr.id_feature 
                        INNER JOIN [AI:Lean].[dbo].[product] p 
                        ON pfr.id_product = p.id_product 
                        WHERE p.name_of_product = '{product}' AND f.name_of_feature = '{feature}'
                        """
                
                connection, mycursor = SQLConnectionProvider().create_connection()
                try:
                    mycursor.execute(query)
                except:
                    myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
                else:
                    myresult = mycursor.fetchall()
                    
                    if myresult == []:
                        myresult = "No entry is found in the Product Data Base."
                    else:
                        categories = ("id_feature", "name_of_feature", "gentl_name", "api_name", "datatype", "tooltip", "description", "display_name", "access_mode", "visibility_level", "type_of_value", "maximum_values", "minimum_values", "increment_values", "length", "port", "signature", "unit", "namespace", "command_value", "default_value", "gentl_pmax", "gentl_pmin", "streamable", "register", "generate_register", "handler_function", "available_sk", "lock_while_acq", "cal_en", "cal_rtg", "xp_en", "xp_ext_en", "app_def", "polling_time", "string_is_path", "supported_file_format", "web_link", "flags", "p_selected", "value_description", "invalidates_all_params", "web_download_type", "id", "id_product", "id_feature", "id_product", "name_of_product", "description")
                        if len(categories) == len(myresult[0]):
                            myresult = {categories[i]: myresult[0][i] for i, _ in enumerate(myresult[0])}

    source = [{'id': "1", 'content': f'Query for: Product = {product}, Feature = {feature}', 'metadata': {'type': "Product_Database"}}]
    
    return myresult, source

def similar(a, liste):
    highest_score = 0
    highest_element = None

    for l in liste:
        score = SequenceMatcher(None, l[0], a).ratio()
        if score > highest_score:
            highest_score = score
            highest_element = l[0]

    return highest_element, highest_score

def similar2(a, liste):
    return max(liste, key=lambda l: SequenceMatcher(None, a, l).ratio())

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
    connection, mycursor = SQLConnectionProvider().create_connection()
    try:
        mycursor.execute(query)
    except:
        myresult = "The query you wrote produced an error message. Rewrite the query if possible or fix the mistake in this query!"
    else:
        myresult = mycursor.fetchall()

    source = [{'id': "1", 'content': f'Query for: Product = {product}', 'metadata': {'type': "Product_Database"}}]
    return myresult, source

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def initMongo():
    client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
    db = client["XIMEAGPT"]                   
    col = db["prototype"]
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
    col = db["prototype"]
    query_embedding = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    used_tokens = query_embedding["usage"]["total_tokens"]

    filtered_query_embedding = query_embedding['data'][0]['embedding']
    print("--------------------------")
    print(query_embedding)
    print("--------------------------")
    print(filtered_query_embedding)
    print("---------------------------")
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

# class SQLConnectionProvider:
#     def __init__(self):
#         self.server = os.getenv('SQL_SERVER')
#         self.database = os.getenv('SQL_DATABASE')
#         self.username = os.getenv('SQL_USERNAME')
#         self.password = os.getenv('SQL_PASSWORD')
        
#     # create connection to SQL Server database
#     def create_connection(self):
#         """
#         Create a connection to the SQL Server database
#         :return connection, cursor: connection and cursor objects
#         """
        
#         load_dotenv()
#         connection = pymssql.connect(self.server, self.username, self.password, self.database)
#         cursor = connection.cursor()
#         return connection, cursor

# query = """
# SELECT DISTINCT f.name_of_feature
# FROM [AI:Lean].[dbo].[feature] f
# """

# connection, mycursor = SQLConnectionProvider().create_connection()
# print("OK")
# mycursor.execute(query)
# myresult = mycursor.fetchall()

# similar('resolution', myresult)
# def run():
#     connection, mycursor = SQLConnectionProvider().create_connection()
#     mycursor.execute("SELECT DISTINCT f.name_of_feature FROM feature f")
#     myresult = mycursor.fetchall()

# run()
