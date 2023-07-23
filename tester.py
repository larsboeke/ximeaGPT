import agent.AIResponse_copy as a
import agent.Agent_functions as f



class_used = a.AiResponse_test(1,"'What is the longest Exposure Time our cameras support? Check out the different kind of values that are inside of the product database!;")
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


