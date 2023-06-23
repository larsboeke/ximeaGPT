class EmailDatabaseDeleter:
    def __init__(self, pinecone_connection, mongodb_connection):
        """
        :param pinecone_connection:
        :param mongodb_connection:
        """
        self.pinecone_connection = pinecone_connection
        self.mongodb_connection = mongodb_connection

    def deleteCases(self, updated_cases):
        """
        Delete all entries from cases from the mongodb and pinecone
        database in order to push a completely new version of the case lateron
        :param updated_cases: list of updated cases
        """
        for case in updated_cases:
            # TODO: check for working
            mongodb_filter = {"metadata.case_id": str(case[0])}
            #wrong: mongodb_filter = {"case_id": case[0]}
            #wrong: pinecone_filter = {"metadata.case_id": str(case[0])}

            chunks = []
            for chunk in self.mongodb_connection.find(mongodb_filter, {}):
                chunks.append(str(chunk["_id"]))

            self.mongodb_connection.delete_many(mongodb_filter)
            # TODO; Wrong sth with pinecone_filter
            self.pinecone_connection.delete(ids = chunks, namespace = 'pastConversations')
