import agent.AIResponse_copy as a
import agent.Agent_functions as f

"""
liste, score =f.similar(["2x2 binning","Resolution"])
print(str(liste))
print(str(score))
"""


class_used = a.AiResponse_test(1,"Please run this query for me! Select id_feature From product_database Where id_feature = '8';")
answer, source = class_used.chat_completion_request()
print("assistant_message")
print(answer)

user_prompt = 'start'
while str(user_prompt) != 'stop':
    user_prompt = input("what is your question?")
    class_used.add_user_prompt(str(user_prompt))
    answer, source = class_used.chat_completion_request()
    print("assistant_message")
    print(answer)
    print(str(source))


