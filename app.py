from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import pdfChunker
from flask import request
from werkzeug.utils import secure_filename
import openai
import agent
 
openai.api_key = os.getenv("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")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_name = secure_filename(file.filename)
    save_pdf_file(file_name, file)
    return f"File '{file_name}' uploaded successfully."

#react to client message
def generate_backend_message(client_msg):
    #ai_response = ai.create_ai_response(client_msg)
    generated_message = agent.agent(client_msg)

    return generated_message

#resive client messages and send response
@socketio.on('client_message')
def handleMessage(client_msg):
    print(f"Client message: {client_msg}")

    backend_msg = agent.agent(client_msg)
    emit('backend_message', backend_msg, broadcast=True)

#pdfupload
@socketio.on('pdf_upload')
def handle_pdf_upload(data):
    file_name = data['fileName']
    file_data = data['fileData']
    print(f"Uploading PDF file: {file_name}")

    upload_response = save_pdf_file(file_name, file_data)
    emit('pdf_upload_response', upload_response, broadcast=True)

#save pdf file and send embeddings to pinecone
def save_pdf_file(file_name, file):
    # Replace this with your desired directory
    upload_folder = '/home/lorenzboke/uni/ailean/src/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    path = upload_folder + "/" + file_name
    file.save(os.path.join(upload_folder, file_name))
    pdfChunker.chunkPDF(path)
    return f"File '{file_name}' uploaded successfully."




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
