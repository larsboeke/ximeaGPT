from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os
import uploadData
from werkzeug.utils import secure_filename
import agent
import uploadData
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

#set up the connection to the Mongodb
client = MongoClient('mongodb://192.168.11.30:27017/')
db = client['XIMEAGPT']
users_collection = db['users']
#structure of users collection
# {
#     "_id": "unique_user_id",
#     "email": "user's username",
#     "password"?
#     "chats": ["chat_id1", "chat_id2", ...]
# }
chats_collection = db['chats']
#structure of chats collection
# {
#     "_id": "unique_chat_id",
#     "user_id": "user_id",
#     "chat_title": "",
#     "messages": [
    #     {
    #         "sender": "user/client",
    #         "message": "The message sent by the user",
    #         "timestamp": "timestamp"
    #     },
    #     {
    #         "sender": "backend",
    #         "message": "The response generated by the backend",
    #         "timestamp": "timestamp",
    #         "feedback": { "rating": "positive/negative",
    #                        "comment": ""}
    #     },
    #     ...

    #       {"client_msg": "",
    #        "backend_msg": "",
    #        "timestamp": "",
    #        "feedback":""}



    # ],
# }
#Routing for the chatbot page
@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_name = secure_filename(file.filename)
    return f"File '{file_name}' uploaded successfully."

#react to client message
def generate_backend_message(client_msg):
    generated_message = agent.agent(client_msg)['output']
    print(generated_message)
    return generated_message

#resive client messages and send response
@socketio.on('client_message')
def handleMessage(client_msg):
    print(f"Client message: {client_msg}")
    backend_msg = generate_backend_message(client_msg)
    message_document = {
        'client_message': client_msg,
        'backend_response': backend_msg
    }
    chats_collection.insert_one(message_document)
    emit('backend_message', backend_msg, broadcast=False)

@socketio.on('send_message')
def handle_message(data):
    chat_id = data['chat_id']
    client_msg = data['text']
    time = data['time']
    backend_msg = agent.agent(client_msg)['output']
    message_document = {
        'client_message': client_msg,
        'backend_response': backend_msg,
        'timestamp': time
    }
    chats_collection.update_one({'_id': chat_id}, {'$push': {'messages': message_document}})
     # Get the updated chat document
    chat = chats_collection.find_one({'_id': chat_id})
    # Emit the updated chat document back to the client
    socketio.emit('chat_updated', chat, room=chat_id)

@socketio.on('start_chat')
def start_chat(user_id):
    chat_document = {
        'user_id': user_id,
        'messages': []
    }
    chat = chats_collection.insert_one(chat_document)
    chat_id = chat.inserted_id
    # Emit the chat ID back to the client
    socketio.emit('chat_started', {'chat_id': str(chat_id)})
    #TO-DO:add on the client side socket.on('chat_started')


#Routing for the admin panel
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard.html')

@app.route('/admin/documents')
def admin_documents():
    return render_template('documents.html')

@app.route('/admin/upload')
def admin_upload():
    return render_template('upload.html')

@app.route('/admin/feedback')
def admin_feedback():
    return render_template('feedback.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
 


