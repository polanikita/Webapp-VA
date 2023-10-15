from flask import Flask, jsonify, request, url_for, redirect, render_template_string, render_template
from datetime import date, datetime

import wave
import sys
import pyaudio
import time

app = Flask(__name__)

# Create a dictionary to store clinic IDs and passwords
clinic_ids = {'NYU': '123', 'COL': '234'}
current_clinic_id = []

# Variable to track recording status
is_recording = False

@app.route('/start_recording', methods=['GET'])
def start_recording():
    global is_recording
    if not is_recording:
        # Set recording flag to True
        is_recording = True

        # Place your audio recording code here
        # This code will be executed when the "Record Audio" button is clicked

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1 if sys.platform == 'darwin' else 2
        RATE = 44100
        RECORD_SECONDS = 15
        filename = time.strftime("%Y%m%d-%H%M%S")
        # print(type(filename))
        with wave.open(filename+".wav", 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            print('Recording...')
            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                wf.writeframes(stream.read(CHUNK))
            print('Done')

            stream.close()
            p.terminate()

        # Set recording flag to False when recording is done
        is_recording = False

    return '', 200  # Return an empty response with a 200 status code

@app.route('/check_recording_status', methods=['GET'])
def check_recording_status():
    global is_recording
    return jsonify({'recording': is_recording})


@app.route('/', methods=['GET', 'POST'])
def login():
    global clinic_id
    error_message = ''
    if request.method == 'POST':
        current_clinic_id.clear()
        clinic_id = request.form.get('clinic_id')
        current_clinic_id.append(clinic_id)
        password = request.form.get('password')
        if clinic_id in clinic_ids and clinic_ids[clinic_id] == password:
            return redirect(url_for('welcome'))
        else:
            error_message = 'Incorrect Clinic ID or password. Please try again.'

    return render_template('login.html', error_message=error_message)



@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    clinic_id = current_clinic_id[0]  # Assuming current_clinic_id is a list containing the current clinic_id value
    return render_template('welcome.html', clinic_id=clinic_id)



    
@app.route('/patient_charts', methods=['POST'])
def patient_charts(): 
    return render_template('patient_charts.html')





@app.route('/view_profile', methods=['GET'])
def view_profile():
    
    return render_template('view_profile.html')
   


@app.route('/record_audio', methods=['POST'])
def record_audio():
    #if request.form.get('action') == 'record_audio':
    return render_template('record_audio.html')
    #else:
        #return 'Invalid request'


@app.route('/scheduled_calls', methods=['GET', 'POST'])
def scheduled_calls():
    #if request.method == 'POST':
        # Handle form submission here
        # Retrieve form data using request.form.get('field_name')
        #pass 
    return render_template('scheduled_calls.html')



if __name__ == '__main__':
    app.run(debug=True)
