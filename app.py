from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os
import uploadData
from werkzeug.utils import secure_filename
import agent
import uploadData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('login.html')

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
    emit('backend_message', backend_msg, broadcast=False)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
 


