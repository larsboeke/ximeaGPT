from CaseRepository import CaseRepository
from SQLConnectionProvider import SQLConnectionProvider
from EmailRepository import EmailRepository
from Email import Email
from PlainTextFromEmailProvider import PlainTextFromEmailProvider
from Case import Case
from PlainTextFromCaseProvider import PlainTextFromCaseProvider
from EmailChunker import EmailChunker

sql_connection = SQLConnectionProvider().create_connection()

all_cases = CaseRepository(sql_connection).get_cases()

#Liste an Email-Objekten 
print(all_cases[5][0])
#TODO: move sql_connection to object generation (into the init)
emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(all_cases[5][0])

#TODO: 
one_case = Case(all_cases[5][0], emails_for_one_case)
content = PlainTextFromCaseProvider().provide_full_content(one_case)

chunks = EmailChunker().chunk_data(content, one_case.metadata)

print(chunks)










