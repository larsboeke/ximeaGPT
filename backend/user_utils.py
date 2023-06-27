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
        
        # TODO
        # add conversation to user

        conversation_id = generate_chat_id()
        
        #add conversation entry to conversatoin collection
        entry = {
            'converation_id': conversation_id,
            'messages': [] 
            }
        conversations_mongo.insert_one(entry)

        #add conversation id to user
        user = user_mongo.find_one({'user_id': user_id})
        conversations = user['conversations']
        conversations_updated = conversations.append(conversation_id)
        user_mongo.update_one({'user_id': user_id}, {'$set': {'conversations': conversations_updated}})
        
        return conversation_id
        
def generate_chat_id():
    while True:

        id = str(uuid4())
        if not conversations_mongo.find_one({'user_id': id}):

            return id

def add_message(conversation_id, role, content):
        message = {"role": role, "content": content}
        conversation = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']
        updated_messages = conversation.append(message)
        update_query = conversations_mongo.update_one({'convesation_id': conversation_id}, {'$set': {'messages': updated_messages }})

def add_function(conversation_id, function_name, content):
    message = {"role": 'function','function_name': function_name, "content": content}
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']
    updated_messages = conversation.append(message)
    conversations_mongo.update_one({'convesation_id': conversation_id}, {'$set': {'messages': updated_messages }})

def get_past_messages(user_id, conversation_id):
    messages = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']

    return messages

def get_past_cleaned_conversations(user_id):
    #get all conversation IDs
    user = user_mongo.find_one({'user_id': user_id})
    conversation_ids = user['conversations']

    if conversation_ids:
        #get conversations for user_id and sort by time
        conversations = conversations_mongo.find(conversation_ids)
        conversations_list = list(conversations)

        #clear conversation from function and system messages
        cleared_converations = []
        for conversation in conversations_list:
            cleared_conversation = []
            for message in conversation:

                if message["role"] == "system" or message["role"] == "function":
                    cleared_conversation.append(message)
            
            cleared_converations.append(cleared_conversation)

        sorted_conversations = sorted(conversations_list, key=lambda x: x['datetime'])
        
        return sorted_conversations
    return []






