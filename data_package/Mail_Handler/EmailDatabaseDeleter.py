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
            self.mongodb_connection.delete_one({'_id': case[0]})
            self.pinecone_connection.delete(case[0])
