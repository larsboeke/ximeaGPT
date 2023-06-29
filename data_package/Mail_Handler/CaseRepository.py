

class CaseRepository:
    def __init__(self, sql_connection):
        """
        :param sql_connection:
        """
        self.connection, self.cursor = sql_connection

    def get_all_cases(self):
        """
        Get all cases
        :return results: list of cases
        :rtype: list
        """
        query = "SELECT DISTINCT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails]"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_updated_cases(self):
        """
        Get cases where new activities have been added since last upload
        :return results: list of cases
        """
        query = "SELECT DISTINCT [regardingobjectid]" \
                "FROM [AI:Lean].[dbo].[CrmEmails]" \
                "WHERE [regardingobjectid] IN ( " \
                    "SELECT [regardingobjectid] " \
                    "FROM [AI:Lean].[dbo].[CrmEmails] " \
                    "GROUP BY [regardingobjectid] " \
                    "HAVING COUNT(*) > SUM(CAST([is_uploaded] AS INT)))"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results