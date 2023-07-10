from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_login import current_user
from flask_socketio import SocketIO, emit
import flask
import os
#import old_stuff.uploadData as uploadData
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from agent.AIResponse import AiResponse
#import uploadData
from pymongo import MongoClient
import backend.user_utils as usr
import backend.activity_utils as activity
from datetime import datetime  

app = Flask(__name__, template_folder='Frontend/templates')
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#set up the connection to the Mongodb
client = MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']
users_collection = db['users']
chats_collection = db['chats']

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    u = users_collection.find_one({"user_id": user_id})
    if not u:
        return None
    return User(u['user_id'], u['password_hash'])

@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    if not users_collection.find_one({'user_id': user_id}):
        return

    user = User(user_id)
    
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(username, password)
        user = users_collection.find_one({"user_id": username})
    

        if user and check_password_hash(user['password_hash'], password):
            print("username and pw match")
            user_obj = User(user['user_id'], user['password_hash'])
            login_user(user_obj)
            print(current_user.is_authenticated)
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if users_collection.find_one({"user_id": username}):
            return render_template('register.html', usernameExists= "Username already exists")
        else:            
            password_hash = generate_password_hash(password)
            usr.add_user(username, password_hash)
            print("registered user")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
    # Check if the user has a cookie
        conversations = usr.get_chat_ids(current_user.id)
        #print(conversations)
        # if 'ailean_user_id' in request.cookies:
        #     user_id = request.cookies.get('ailean_user_id')
        #     conversations = usr.get_chat_ids(user_id)
        #     print(conversations)
        #     return render_template('chatbot.html', user_id=user_id, chats=conversations)
        print(current_user.id)
        return render_template('chatbot.html', chats=conversations[::-1])
        
    else:
        return render_template('login.html')
        
        # else:
        #     user_id = usr.add_user()
        #     response = flask.make_response()
        #     response.set_cookie('ailean_user_id', user_id)
        #     #conversations = usr.get_chat_ids(user_id)
        #     return response, render_template('chatbot.html', user_id=user_id)



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
def generate_backend_message(conversation_id, user_prompt):
    #create airesponse object and request chat completion
    print("CONVERSTION ID FOR QUERY: " + conversation_id)
    response_request = AiResponse(conversation_id, user_prompt)
    assistant_message, sources = response_request.chat_completion_request()
    print("Conversation ID for query " + conversation_id)    
    return assistant_message, sources



#recieve client messages and send response
@socketio.on('send_message')
def handle_message(data):
    print("AiResponse started")
    #print(current_user.id)
    chat_id = data['chat_id']
    client_msg = data['text']
    print(f"Client message: {client_msg}")
    assistant_message, sources = generate_backend_message(chat_id, client_msg)

    data = {'assistant_message': assistant_message, 'sources': sources}
    print(f"Backend message: {assistant_message}")
    #add sources here
    # Emit the updated chat document back to the client ADD SOURCES
    socketio.emit('receive_response', data)




@socketio.on('start_chat')
def start_chat(user_id, user_message): 
    #print(current_user.is_authenticated)
    print("started chat")
     
    chat_id, title = usr.create_chat(user_id, user_message)
    print("started chat with id" + chat_id)

    data = {'chat_id': chat_id, 'title': title}
    # Emit the chat ID back to the client
    socketio.emit('chat_started', data)

@socketio.on('delete_chat')
def delete_chat(username, chat_id):
    ##Delete chat function from User
    usr.delete_chat(username, chat_id)

@socketio.on('open_chat')
def open_chat(chat_id):
    #chat_id = data['chat_id']
    messages = usr.get_messages(chat_id)
    socketio.emit('chat_opened', messages)
    

    
@socketio.on('rate_chunk')
def rate_chunk(chunk_id):
    print(f"You rated a chunk with id", chunk_id)
    #here logic for rating a chunk

    
#Routing for the admin panel
@app.route('/admin/dashboard')
def admin_dashboard():
    now = datetime.now()

# create start_date and end_date with today's date but different time
    start_time_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    report = activity.generate_report(start_time_today, end_time_today)
    stat1 = report['activity_cost']
    stat2 = report['cost_per_message']
    stat3 = report['activity_count']
    stat4 = report['avg_response_time']
    return render_template('dashboard.html', stat1=stat1, stat2=stat2, stat3=stat3, stat4=stat4)

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
    socketio.run(app, port=5000, debug=True)
 


