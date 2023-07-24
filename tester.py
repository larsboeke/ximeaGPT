import agent.AIResponse_copy as a
import agent.Agent_functions as f

# similar =f.similar(["framerate"])
# print(str(similar))
# similar_list = f.similar_embeddings(["framerate","binning"])
# print(str(similar_list))
#answer = f.get_openai_response(user_question="What are different Framerate we have in our product database?", feature_list=['xiapi_FrameRate',])

#print(str(answer))

class_used = a.AiResponse_test(1,"Does MU9PM-BH have Linux x64 Support? ")
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


