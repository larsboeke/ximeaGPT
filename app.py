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

pdf_list = [
        "http://www.ximea.com/downloads/usb3/manuals/xic_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiC",
        "http://www.ximea.com/downloads/usb3/manuals/xiq_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiQ",
        "http://www.ximea.com/downloads/usb3/manuals/xiq_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiQ",
        "http://www.ximea.com/downloads/usb3/manuals/xid_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiD",
        "http://www.ximea.com/downloads/usb2/manuals/ximu_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiMu",
        "http://www.ximea.com/downloads/cb/manuals/xix_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiX",
        "https://www.ximea.com/downloads/cb/manuals/xib_xib64_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xib_xib64",
        "https://www.ximea.com/downloads/usb3/manuals/xispec_technical_manual.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xiSpec",
        "https://www.ximea.com/files/ADPT-MX_description.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=ADPT-MX",
        "https://www.ximea.com/files/flatribbon-cable-description.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=cable",
        "https://www.ximea.com/files/xEC2-connector-description.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xEC2",
        "https://www.ximea.com/files/xSWITCH-multi-camera-platform-description.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=xSwitch",
        "https://www.ximea.com/files/MTP-cabling-Whitepaper.pdf?utm_source=newsletter&utm_medium=email&utm_campaign=MTP",
        "https://www.ximea.com/files/brochures/MX377-High-resolution-Large-sCMOS-camera-brochure.pdf",
        "https://www.ximea.com/files/brochures/xiC-USB3_1-Sony-CMOS-Pregius-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiQ-USB3-Vision-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiD-USB3-High-end-CCD-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiSpec-Hyperspectral-HSI-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiSpec-Hyperspectral-HSI-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiMU-Smallest-USB-5Mpix-camera-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiJ-sCMOS-scientific-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiX-Embedded-multi-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiB64-High-speed-PCIe-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiB-High-resolution-PCIe-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiFLY-Multi-camera-setup-platform-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiRAY-Compact-high-resolution-X-RAY-cameras-brochure-HQ.pdf",
        "https://www.ximea.com/files/brochures/xiX%20Infographic.pdf",
        "https://www.ximea.com/files/brochures/xiSWITCH%20Infographic.pdf"
]

url_list = [
    "https://www.ximea.com/support/projects/allprod/wiki/SCMOS_cameras_with_Back_illumination",
    "https://www.ximea.com/support/wiki/allprod/Cooled_CCD_cameras_-_support_page",
    "https://www.ximea.com/support/projects/allprod/wiki/FAQ_-_Cooled_CCD_cameras",
    "https://www.ximea.com/en/products/xilab-application-specific-custom-oem/Embedded-vision-cameras-xiX",
    "https://www.ximea.com/support/wiki/apis/XIMEA_API_Software_Package",
    "https://www.ximea.com/support/wiki/apis/XIMEA_Linux_Software_Package",
    "https://www.ximea.com/support/wiki/allprod/XIMEA_CamTool",
    "https://www.ximea.com/support/wiki/allprod/Recording_of_Videos_and_Image_Sequences_in_CamTool",
    "https://www.ximea.com/support/projects/allprod/wiki/Camtool_plugin",
    "https://www.ximea.com/support/wiki/allprod/Lua_scripting_in_CamTool",
    "https://www.ximea.com/support/wiki/allprod/Look_up_table"
]
# ? https://www.ximea.com/en/products/camera-manual?utm_source=newsletter&utm_medium=email&utm_campaign=overview
# ? https://www.ximea.com/en/products/xilab-application-specific-custom-oem/scientific-scmos-cameras-with-front-back-illumination%20https:/www.ximea.com/support/projects/allprod/wiki/SCMOS_cameras_with_Back_illumination
# Knowledge Base: https://www.ximea.com/support/wiki/allprod/Knowledge_Base
# Third-party Libraries and software packages: https://www.ximea.com/support/projects/vision-libraries/wiki

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
    return f"File '{file_name}' uploaded successfully."

#react to client message
def generate_backend_message(client_msg):
    #ai_response = ai.create_ai_response(client_msg)
    generated_message = agent.agent(client_msg)['output']
    print(generated_message)
    return generated_message

#resive client messages and send response
@socketio.on('client_message')
def handleMessage(client_msg):
    print(f"Client message: {client_msg}")
    backend_msg = generate_backend_message(client_msg)
    emit('backend_message', backend_msg, broadcast=False)

def upload_pdf(pdf_list):
    for pdf in pdf_list:
        uploadData.uploadPDF(pdf)

def upload_url(url_list):
    for url in url_list:
        uploadData.uploadURL(url)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
 


