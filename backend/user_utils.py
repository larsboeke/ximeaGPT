import pymongo
import openai
import os
import json
from uuid import uuid4
from datetime import datetime as dt
from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for


client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
conversations_mongo = db['conversations']
user_mongo = db['users']



def add_user(username, password_hash):

    entry = {
        'user_id': username,
        'password_hash': password_hash,
        'conversations': []
        }
    user_mongo.insert_one(entry)

    return username


def generate_user_id():
    while True:

        id = str(uuid4())
        print(id)
        print(type(id))
        if not user_mongo.find_one({'user_id': id}):

            return id
        

def create_chat(user_id, user_prompt):
        
        conversation_id = generate_chat_id()
        
        #add conversation entry to conversatoin collection
        entry = {
            'conversation_id': conversation_id,
            'messages': [{"role": "system", "content": "You are a helpful assistant to the customer support in the Company XIMEA. Base your Answers as much as possible on information gathered by the functions. Use Functions calls as much as appropriat"}] 
            }
        conversations_mongo.insert_one(entry)

        title = generate_chat_title(user_prompt)
    
        print(user_id)
        print(conversation_id)
        
        test = user_mongo.update_one({'user_id': user_id}, {'$push': {'conversations': {'conversation_id' : conversation_id, 'title': title}}})
        print(test)
        print("created new chat with id:" + conversation_id)
        return conversation_id, title


def generate_chat_title(user_prompt):#
    
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'system', 'content': 'Your are a assiatant that generates descriptive Titlesof Chats based on the first User Message. ONLY CREATE TITLES THAT CONTAIN LESS THAN 3 WORDS. DO NOT USE MORE THAN THREE WORDS!'},
                    {'role': 'user', 'content': user_prompt}]
    )

    title = response['choices'][0]['message']['content']
    print(title)
    return title

def delete_chat(user_id, chat_id):
    conversations_mongo.delete_one({'conversation_id': chat_id})
    user_mongo.update_one({'user_id': user_id},{ '$pull': { 'conversations': { 'conversation_id': chat_id} }})
    print(f"Conversation is deleted with following id", chat_id)
        
def generate_chat_id():
    while True:

        id = str(uuid4())
        if not conversations_mongo.find_one({'user_id': id}):

            return id

def add_message(conversation_id, role, content):
    message = {"role": role, "content": content, "timestamp": dt.now()}
    conversations_mongo.update_one({'conversation_id': conversation_id}, {'$push': {'messages': message}})
    print('added message')

def add_assistant_message(conversation_id, content, sources):
    message = {'role': 'assistant', 'content': content, 'timestamp': dt.now(), 'sources': sources}
    conversations_mongo.update_one({'conversation_id': conversation_id}, {'$push': {'messages': message}})
    print('added assistant message')


def add_function(conversation_id, function_name, content):
    message = {"role": 'function','function_name': function_name, "content": content}
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})['messages']
    updated_messages = conversation.append(message)
    conversations_mongo.update_one({'convesation_id': conversation_id}, {'$set': {'messages': updated_messages }})

def retrieve_conversation(conversation_id):
    print(conversation_id)
    conversation = conversations_mongo.find_one({'conversation_id': conversation_id})
    # Remove timestamps from messages
    conversation = [{k: v for k, v in msg.items() if k != 'timestamp' and k != 'sources'} for msg in conversation['messages']]

    return conversation



def get_chat_ids(user_id):
    user = user_mongo.find_one({'user_id': user_id})
    conversation_ids = user['conversations']

    #sort chat IDs by Time!!

    return conversation_ids

def get_messages(chat_id):
    chat = conversations_mongo.find_one({'conversation_id': chat_id})

    filtered_messages = []

    messages = chat['messages']
    

    for message in messages:
        if message['role'] == 'user' or message['role'] == 'assistant':

            if 'timestamp' in message:
                message['timestamp'] = message['timestamp'].isoformat()

            filtered_messages.append(message)


    return filtered_messages






