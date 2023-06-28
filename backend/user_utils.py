import pymongo
import openai
import os
import json
from uuid import uuid4
from datetime import datetime as dt


client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
conversations_mongo = db['conversations']
user_mongo = db['users']



def add_user():
    #add new user with no conversatoins user_id = cookie
    
    user_id = generate_user_id()
    entry = {
        'user_id': user_id,
        'conversations': []
        }
    user_mongo.insert_one(entry)

    return user_id


def generate_user_id():
    while True:

        id = str(uuid4())
        print(id)
        print(type(id))
        if not user_mongo.find_one({'user_id': id}):

            return id
        

def create_chat(user_id):
        
        conversation_id = generate_chat_id()
        
        #add conversation entry to conversatoin collection
        entry = {
            'conversation_id': conversation_id,
            'messages': [{"role": "system", "content": "You are a helpful assistant, helping out the customer support in the Company XIMEA. Base your Answers as much as possible on information gathered by the functions."}] 
            }
        conversations_mongo.insert_one(entry)

        #add conversation id to user
        user = user_mongo.find_one({'user_id': user_id})
        conversations = user['conversations']

        # if conversations == None:
        #     conversations_updated = [conversation_id]
        # else:
        #     conversations_updated = conversations.append(conversation_id)
    
        user_mongo.update_one({'user_id': user_id}, {'$push': {'conversations': conversation_id}})
        print("created new chat with id:" + conversation_id)
        return conversation_id
        
def generate_chat_id():
    while True:

        id = str(uuid4())
        if not conversations_mongo.find_one({'user_id': id}):

            return id

def add_message(conversation_id, role, content):
    message = {"role": role, "content": content, "timestamp": dt.now()}
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']
    updated_messages = conversation.append(message)
    update_query = conversations_mongo.update_one({'convesation_id': conversation_id}, {'$set': {'messages': updated_messages }})

def add_function(conversation_id, function_name, content):
    message = {"role": 'function','function_name': function_name, "content": content}
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']
    updated_messages = conversation.append(message)
    conversations_mongo.update_one({'convesation_id': conversation_id}, {'$set': {'messages': updated_messages }})

def retrieve_conversation(conversation_id):
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})

    # Remove timestamps from messages
    conversation['messages'] = [{k: v for k, v in msg.items() if k != 'timestamp'} for msg in conversation['messages']]

    return conversation['messages']

# def get_past_cleaned_conversations(user_id):
#     #get all conversation IDs
#     user = user_mongo.find_one({'user_id': user_id})
#     conversation_ids = user['conversations']
#     print(conversation_ids)
#     if conversation_ids:
#         #get conversations for user_id and sort by time
#         conversations = conversations_mongo.find({"conversation_id": {"$in": conversation_ids}})
#         print(conversations)
#         # conversations = conversations_mongo.find(conversation_ids)
#         # conversations_list = list(conversations)

#         #clear conversation from function and system messages
#         cleared_conversations = []
#         for conversation in conversations:
#             cleared_conversation = {'conversation_id': conversation['conversation_id'], 'messages': []}
#             for message in conversation['messages']:

#                 if message["role"] == "system" or message["role"] == "function":
#                     cleared_conversation['messages'].append(message)
            
#             cleared_conversations.append(cleared_conversation)

#         #sorted_conversations = sorted(conversations, key=lambda x: x['datetime'])
        
#         return cleared_conversations
#     return []

def get_chat_ids(user_id):
    user = user_mongo.find_one({'user_id': user_id})
    conversation_ids = user['conversations']
    # filteres_conversation_ids = []
    # #filter conversations for empty converations
    # conversations = conversations_mongo.find({'conversation_id': conversation_ids})
    # print(str(conversations))
    # for conversation in conversation_ids:
    #     conv = conversations_mongo.find_one({'conversation_id' : conversation})
    #     if conv is not None:
    #         messages = conv['messages']
            
    #         if len(messages) > 1:
    #             filteres_conversation_ids.append(conversation)


    return conversation_ids

def get_messages(chat_id):
    chat = conversations_mongo.find_one({'conversation_id': chat_id})

    filteres_messages = []
    for message in chat['messages']:
        if message['role'] == 'user' or message['role'] == 'assistant':
            filteres_messages.append(message)

    return filteres_messages






