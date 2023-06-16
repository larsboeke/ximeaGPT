from data_package.Mail_Handler.CaseRepository import CaseRepository
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
from data_package.Mail_Handler.EmailRepository import EmailRepository
from data_package.Mail_Handler.Case import Case
from data_package.Mail_Handler.PlainTextFromCaseProvider import PlainTextFromCaseProvider
from data_package.Chunk_Handler.Chunker import Chunker

sql_connection = SQLConnectionProvider().create_connection()

all_cases = CaseRepository(sql_connection).get_cases()

#Liste an Email-Objekten
print(all_cases[5][0])
#TODO: move sql_connection to object generation (into the init)
emails_for_one_case = EmailRepository(sql_connection).get_emails_for_case(all_cases[5][0])

#TODO: 
one_case = Case(all_cases[5][0], emails_for_one_case)
content = PlainTextFromCaseProvider().provide_full_content(one_case)

chunks = Chunker().data_to_chunks(content, one_case.metadata)

print(chunks)










