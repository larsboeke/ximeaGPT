from upload.DatabaseCleaner import DatabaseCleaner
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider
from bson.objectid import ObjectId

mongodb_connection = MongoDBConnectionProvider().initMongoDB()
pinecone_connection = PineconeConnectionProvider().initPinecone()



"""DatabaseCleaner(mongodb_connection=mongodb_connection,
                pinecone_connection=pinecone_connection).delete_chunk("64b539ff759784636018534c")
"""

# get content from _id 64b79bdc27af13bd1fff72f0 from mongodb
#chunk = mongodb_connection.find_one({"_id": ObjectId("64b7188c250c1ee3e4ce1e84")})
#print(chunk)

"""pinecone_vector = pinecone_connection.fetch(ids = ["64b709fa250c1ee3e4cd3392"], namespace = "pastConversations")

pinecone_connection.delete(ids = ["64b709fa250c1ee3e4cd3392"], namespace = "pastConversations")
print(pinecone_vector)"""
# find all chunks from mongodb where content contains "͟͟͟͟͟͟͟͟͟͟͟͟"
"""chunks = mongodb_connection.find({"content": {"$regex":"͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟͟"}})
chunks_c = []
for chunk in chunks:
    chunks_c.append(chunk["content"])
print(len(chunks_c))
print(chunks_c)"""

"""chunks = mongodb_connection.find({ "content": { "$not": { "$regex": " " } } })
chunks_c = []
for chunk in chunks:
#    print(chunk["_id"])
    chunks_c.append(chunk["_id"])
print(len(chunks_c))"""
#print(chunk["content"])
#print(len(chunk["content"]))

"""DatabaseCleaner(mongodb_connection=mongodb_connection,
                pinecone_connection=pinecone_connection).remove_table_of_contents_manuals()"""


pinecone_connection.delete(delete_all = True, namespace = "name_of_sql_features_modified_sql_db")