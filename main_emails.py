from get_message import get_full_message_from_one_case
from get_cases_from_db import get_all_cases, get_new_cases

# Get all email cases
get_all_cases()

# Get all email cases, newer than x days
get_new_cases(13)

# Get full message of example case "443028c8-a026-eb11-96e8-00155d0b2a0b"
# case, metadata = get_full_message_from_one_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
case, metadata = get_full_message_from_one_case("95739A8C-00EA-ED11-9717-00155D0B2A0B")

print(case)
#print(metadata)
