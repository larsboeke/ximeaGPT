class EmailDatabaseDeleter:
    def __init__(self, pinecone_connection, mongodb_connection, sql_connection):
        """
        :param pinecone_connection:
        :param mongodb_connection:
        :param sql_connection:
        """
        self.pinecone_connection = pinecone_connection
        self.mongodb_connection = mongodb_connection
        self.connection, self.cursor = sql_connection

    def deleteCases(self, updated_cases):
        """
        Delete all entries from cases from the mongodb and pinecone
        database in order to push a completely new version of the case lateron
        :param updated_cases: list of updated cases
        """
        for case in updated_cases:
            mongodb_filter = {"metadata.source_id": str(case[0])}
            print("Case to be deleted: ", case[0])
            mongodb_chunk_ids = []
            for mongodb_chunk_id in self.mongodb_connection.find(mongodb_filter, {}):
                mongodb_chunk_ids.append(str(mongodb_chunk_id["_id"]))
            #print(mongodb_chunk_ids)
            if mongodb_chunk_ids:
                self.pinecone_connection.delete(ids = mongodb_chunk_ids, namespace ='emails')
                self.mongodb_connection.delete_many(mongodb_filter)

    def delete_null_activities(self):
        """
        Delete all entries from CrmEmails where description is NULL
        """
        delete_query = "DELETE FROM [AI:Lean].[dbo].[CrmEmails] WHERE [description] IS NULL"
        self.cursor.execute(delete_query)
        self.connection.commit()

