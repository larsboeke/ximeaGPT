from get_message import get_full_message_from_one_case
from get_cases_from_db import get_all_cases, get_new_cases
from email_chunker import chunk_email

# SOME EXAMPLES:

# Get all email cases
get_all_cases()

# Get all email cases, newer than x days
cases = get_new_cases(13)

# Get full message of example case "443028c8-a026-eb11-96e8-00155d0b2a0b"
case = get_full_message_from_one_case("443028c8-a026-eb11-96e8-00155d0b2a0b")

result = chunk_email("443028c8-a026-eb11-96e8-00155d0b2a0b")
print(result)
# Some example queries
"""
case, metadata = get_full_message_from_one_case("44e1f779-96f4-ed11-9718-00155d0b2a0b")
case, metadata = get_full_message_from_one_case("f5fe8c80-88e2-ed11-9717-00155d0b2a0b")
print(case)
print(metadata)
print(cases)
for caset in cases:
    print(caset[0])
    case, metadata = get_full_message_from_one_case(caset[0])
    print(case)"""
