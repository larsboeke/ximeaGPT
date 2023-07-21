from bson.objectid import ObjectId
import time

class DatabaseCleaner:
    def __init__(self, mongodb_connection, pinecone_connection):
        self.mongodb_connection = mongodb_connection
        self.pinecone_connection = pinecone_connection
    def delete_chunk(self, chunk_id):
        """
        Deletes a chunk from Pinecone and MongoDB
        :param chunk_id:
        """
        # Delete from MongoDB
        self.mongodb_connection.delete_one({"_id": ObjectId(chunk_id)})
        # Delete from Pinecone
        self.pinecone_connection.delete(ids=[chunk_id], namespace="pastConversations")
        print(f"Deleted chunk {chunk_id} from Pinecone and MongoDB")

    def delete_short_chunks(self):
        """
        Deletes chunks with less than 100 characters
        """
        query = {
            "$expr": { "$lt": [{ "$strLenCP": "$content" }, 100] },
            "metadata.type": "email"
        }
        result = self.mongodb_connection.find(query)
        chunks = [document for document in result]
        print("Deleting chunks with less than 100 characters: ", len(chunks))

        for chunk in chunks:
            self.delete_chunk(str(chunk['_id']))


    def remove_duplicates_from_databases(self):
        """
        Removes duplicates from Pinecone and MongoDB
        """
        pipeline = [
            {
                "$match": {
                    "metadata.type": "email"
                }
            },
            {
                "$group": {
                    "_id": "$content",
                    # _id should be the first ten characters of the content
                    # "_id": { "$substr": ["$content", 0, 10] },
                    "count": {"$sum": 1},
                    "documents": {"$push": "$$ROOT"}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]

        result = list(self.mongodb_connection.aggregate(pipeline))
        print("Deleting number of chunks that are in the DB more than once: ", len(result))
        if len(result) != 0:
            for document in result:
                for duplicate in document['documents']:
                    if duplicate['_id'] != document['documents'][0]['_id']:
                        self.delete_chunk(str(duplicate['_id']))


    def remove_substrings_from_database(self):
        not_unique_content_ids = []
        docs = self.mongodb_connection.find()
        contents = [(doc['_id'], doc['content']) for doc in docs]

        start_time = time.time()
        for i in range(len(contents)):
            substring_found = False
            for j in range(len(contents)):
                if i != j and contents[i][1] in contents[j][1]:
                    substring_found = True
                    break
            if substring_found:
                not_unique_content_ids.append(contents[i][0])

            elapsed_time = time.time() - start_time
            remaining_time = elapsed_time / (i + 1) * (len(contents) - (i + 1))
            print(
                f"\r{str(round((i + 1) / len(contents) * 100, 2))}% checked, approx. remaining time: {round(remaining_time / 60, 2)} minutes",
                end="")

        print("\rDeleting number of chunks that are substrings of other chunks: ", len(not_unique_content_ids))
        teil_strings_c = []
        for teil_string in not_unique_content_ids:
            # convert into str
            teil_string = str(teil_string)
            teil_strings_c.append(teil_string)

        for teil_string in teil_strings_c:
            self.delete_chunk(teil_string)


    def remove_table_of_contents_manuals(self):
        """
        Deletes table of contents for the manuals from Pinecone and MongoDB since they are redundant
        """
        query = {
                  "metadata.type": "manuals",
                    "content": {
                    "$regex": "\\.\\.\\.\\.\\.\\.\\.",
                    "$options": "i"
                  }
                }
        result = self.mongodb_connection.find(query)
        chunks = [document for document in result]
        print("Deleting redundant table of contents of manuals: ", len(chunks))

        for chunk in chunks:
            self.delete_chunk(str(chunk['_id']))

    def remove_chunks_with_no_spaces(self):
        """
        Deletes chunks with no spaces from Pinecone and MongoDB since they are redundant
        """
        query = { "content": { "$not": { "$regex": " " } } }

        result = self.mongodb_connection.find(query)
        chunks = [document for document in result]
        print("Deleting chunks with no spaces: ", len(chunks))

        for chunk in chunks:
            self.delete_chunk(str(chunk['_id']))

    def remove_trash_chunks(self):
        """
        Deletes chunks with trash content from Pinecone and MongoDB
        """
        query = { "content": { "$regex": "^[͟r\n \\>\\\r]+$" } }
        query_2 = {"content": {"$regex": "=\\?utf-8\\?B\\?[^?]+\\?="}}

        result = self.mongodb_connection.find(query)
        result_2 = self.mongodb_connection.find(query_2)
        chunks = [document for document in result]
        chunks.extend([document for document in result_2])
        print("Deleting chunks with non-sense content: ", len(chunks))

        for chunk in chunks:
            self.delete_chunk(str(chunk['_id']))