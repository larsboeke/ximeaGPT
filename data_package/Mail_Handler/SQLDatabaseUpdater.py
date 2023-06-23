

class SQLDatabaseUpdater:
    def __init__(self, sql_connection):
        """
        :param sql_connection:
        """
        self.connection, self.cursor = sql_connection

    def update_case(self, caseid):
        """
        Set specific case as uploaded in database (set is_uploaded = 1)
        :param caseid: [regardingobjectid] in database
        """
        update_query = f"UPDATE [AI:Lean].[dbo].[CrmEmails] SET [is_uploaded] = 1 " \
                       f"WHERE [regardingobjectid] = '{caseid}'"
        self.cursor.execute(update_query)
        self.connection.commit()