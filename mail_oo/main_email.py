"""from Case import Case
from Chunker import Chunker
from Email import Email
from PlainTextFromCaseProvider import PlainTextFromCaseProvider
from PlainTextFromEmailProvider import PlainTextFromEmailProvider"""
from SQLConnection import SQLConnectionProvider

case_id = "123"

sql_connection = SQLConnectionProvider().create_connection()

print(sql_connection)






