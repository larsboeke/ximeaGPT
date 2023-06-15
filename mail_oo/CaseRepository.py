from SQLConnectionProvider import SQLConnectionProvider
 
class CaseRepository:
    def __init__(self, sql_connection):
        self.connection, self.cursor = sql_connection

    def get_cases(self):
        query = "SELECT DISTINCT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails]"
        # not distinct but ordered by date: SELECT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] ORDER BY [createdon] ASC
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results