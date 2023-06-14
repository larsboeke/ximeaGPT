"""from Case import Case
from Chunker import Chunker
from Email import Email
from PlainTextFromCaseProvider import PlainTextFromCaseProvider
from PlainTextFromEmailProvider import PlainTextFromEmailProvider"""
from CaseRepository import CaseRepository
from SQLConnectionProvider import SQLConnectionProvider
from EmailRepository import EmailRepository
from Email import Email
from PlainTextFromEmailProvider import PlainTextFromEmailProvider
from Case import Case
from PlainTextFromCaseProvider import PlainTextFromCaseProvider

sql_connection = SQLConnectionProvider().create_connection()

all_cases = CaseRepository().get_cases(sql_connection)

#Liste an Email-Objekten 
print(all_cases[5][0])
email_for_one_case = EmailRepository().get_emails_for_case(all_cases[5][0], sql_connection)

one_case = Case(all_cases[5][0], sql_connection)

print(one_case.emails)

one_full_content = PlainTextFromCaseProvider.provide_full_content(one_case)









