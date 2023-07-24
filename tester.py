import agent.AIResponse_copy as a
import agent.Agent_functions as f

similar =f.similar(["Framerate"])
print(str(similar))
#answer = f.get_openai_response(user_question="What are different Framerate we have in our product database?", feature_list=['xiapi_FrameRate',])

#print(str(answer))

class_used = a.AiResponse_test(1,"What is the Framerate we have in our product database of MR285MU_BH?")
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


