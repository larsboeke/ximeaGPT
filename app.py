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
from upload.Uploader import Uploader
import backend.feedback_utils as feedback
from flask_cors import CORS
import shutil


app = Flask(__name__, template_folder='Frontend/templates')
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_DIRECTORY'] = 'temp/'
CORS(app)
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
       conversations = usr.get_chat_ids(current_user.id)
       #print(conversations)
       print(current_user.id)
       return render_template('chatbot.html', chats=conversations[::-1])     
    else:
        return render_template('login.html')



@app.route('/admin/upload', methods=['POST'])
def upload():
    print("FILE IS LOADING.....")
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_name = secure_filename(file.filename)
    print("Following file is uploaded succesfully --->", file_name)
    temp_path = os.path.join(
        app.config['UPLOAD_DIRECTORY'],
        secure_filename(file.filename))
    file.save(temp_path)
    Uploader().uploadPDF_local(temp_path)
    shutil.rmtree(app.config['UPLOAD_DIRECTORY'])
    os.mkdir(app.config['UPLOAD_DIRECTORY'])
    return f"File '{file_name}' uploaded successfully."

#react to client message
def generate_backend_message(conversation_id, user_prompt):
    #create airesponse object and request chat completion
    print("generate_backend_message: CONVERSTION ID FOR QUERY: " , conversation_id)
    response_request = AiResponse(conversation_id, user_prompt)
    assistant_message, sources = response_request.chat_completion_request()
    print("generate_backend_message: Conversation ID for query " , conversation_id)    
    return assistant_message, sources



#recieve client messages and send response
@socketio.on('send_message')
def handle_message(data):
    print("Socket: send_message: AiResponse started")
    #print(current_user.id)
    chat_id = data['chat_id']
    client_msg = data['text']
    print(f"Socket: send_message: Client message: {client_msg}")
    assistant_message, sources = generate_backend_message(chat_id, client_msg)

    data = {'assistant_message': assistant_message, 'sources': sources}
    print(f"Socket: send_message: Backend message: {assistant_message}")
    #add sources here
    # Emit the updated chat document back to the client ADD SOURCES
    socketio.emit('receive_response', data)




@socketio.on('start_chat')
def start_chat(user_id, user_message): 
    #print(current_user.is_authenticated)
    print("Socket: shart_chat: started")
     
    chat_id, title = usr.create_chat(user_id, user_message)
    print("Socket: shart_chat: CONVERSTION ID FOR NEW CHAT: " + chat_id)
    print("Socket: shart_chat: generated title: " + title)

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
    feedback.add_feedback(chunk_id)

def generate_report(startdate, enddate):
    start_time_today = startdate.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time_today = enddate.replace(hour=23, minute=59, second=59, microsecond=999999)
    print(f"Selected daterange: from {start_time_today} to {end_time_today}")

    report = activity.generate_report(start_time_today, end_time_today)
    activity_cost = report['activity_cost']
    cost_per_message = report['cost_per_message']
    activity_count = report['activity_count']
    avg_response_time = report['avg_response_time']
    graph_data = report['graph_data']
    print(f"GRAPHDATA: {graph_data}")
    return activity_cost, cost_per_message, activity_count, avg_response_time

@socketio.on('update_stats')
def update_stats(startdate, enddate):
    print(f"Selected daterange JS: from {startdate} to {enddate}")
    activity_cost, cost_per_message, activity_count, avg_response_time = generate_report(datetime.fromisoformat(startdate), datetime.fromisoformat(enddate))
    stats = {'activity_cost': activity_cost, 'cost_per_message': cost_per_message, 'activity_count': activity_count, 'avg_response_time': avg_response_time}
    socketio.emit('updated_stats', stats)

@socketio.on('upload_text')
def upload_text(text):
    Uploader().uploadText(text)
    print(f"Following text is uploaded: '{text}'")

@socketio.on('upload_url')
def upload_url(url):
    Uploader().uploadURL(url)
    print(f"Following url is uploaded {url}")

@socketio.on('reset_all_feedback')
def handle_reset_all_feedback():
    feedback.reset_all_down_ratings()

@socketio.on('reset_feedback')
def handle_reset_feedback(chunk_id):
    print(f"You reseted feedback of chunk with id", chunk_id)
    feedback.reset_down_rating(chunk_id)

@socketio.on('delete_chunk')
def handle_delete_chunk(chunk_id):
    print(f"You deleted chunk with id", chunk_id)
    feedback.delete_chunk(chunk_id)
    
#Routing for the admin panel
@app.route('/admin/dashboard')
def admin_dashboard():
    now = datetime.now()
    activity_cost, cost_per_message, activity_count, avg_response_time = generate_report(now, now)    
    return render_template('dashboard.html', activity_cost=activity_cost, cost_per_message=cost_per_message, activity_count=activity_count, avg_response_time=avg_response_time)

@app.route('/admin/documents')
def admin_documents():
    return render_template('documents.html')

@app.route('/admin/upload')
def admin_upload():
    return render_template('upload.html')
@app.route('/admin/feedback')
def admin_feedback():
    all_feedback = feedback.get_all_cleaned_rated_chunks()
    return render_template('feedback.html', all_feedback = all_feedback)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True, host='0.0.0.0')
 


