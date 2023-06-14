from SQLConnectionProvider import SQLConnectionProvider
 
class CaseRepository:

    def get_cases(self, sql_connection):
        connection, cursor = sql_connection
        query = "SELECT DISTINCT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails]"
        # not distinct but ordered by date: SELECT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] ORDER BY [createdon] ASC
        cursor.execute(query)
        results = cursor.fetchall()
        return results