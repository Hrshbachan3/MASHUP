# Assignment-5: MASHUP

# Name: Hrsh Dhingra
# Roll no. 102103443

# app

from flask import Flask, request, render_template, send_file
import os
import subprocess
import zipfile
import smtplib
from email.message import EmailMessage
import youtube_dl
from moviepy.editor import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def download_videos(singer, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'max_downloads': num_videos,
        'default_search': 'ytsearch',
        'verbose': True,  # Add the verbose flag
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f'{singer}'])
        except youtube_dl.DownloadError as e:
            print(f"Error occurred: {e}")
            print("Unable to download videos. Please try again later.")
            return
        except Exception as e:
            print(f"Error occurred: {e}")
            return

def convert_to_audio():
    for filename in os.listdir('.'):
        if filename.endswith('.webm'):
            audio = AudioFileClip(filename)
            audio.write_audiofile(f'{filename[:-5]}.mp3')
            os.remove(filename)

def cut_audio(duration):
    for filename in os.listdir('.'):
        if filename.endswith('.mp3'):
            audio = AudioFileClip(filename)
            audio = audio.subclip(0, duration)
            audio.write_audiofile(f'cut_{filename}')
            os.remove(filename)

def merge_audios(output_file):
    audio_files = [file for file in os.listdir('.') if file.startswith('cut_') and file.endswith('.mp3')]
    audio_clips = [AudioFileClip(file) for file in audio_files]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile(output_file)

def mashup(singer, num_videos, duration, output_file):
    try:
        download_videos(singer, num_videos)
        convert_to_audio()
        cut_audio(duration)
        merge_audios(output_file)
        print("Mashup completed successfully!")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def send_email(email, file_path):
    msg = EmailMessage()
    msg['From'] = 'schawla_be21@thapar.edu'
    msg['To'] = email
    msg['Subject'] = 'Mashup Result'
    msg.set_content('Please find attached the result of the mashup.')

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('schawla_be21@thapar.edu', '25@Svea')
        smtp.send_message(msg)

@app.route('/mashup', methods=['POST'])
def process_mashup():
    singer = request.form['singer']
    num_videos = int(request.form['num_videos'])
    duration = int(request.form['duration'])
    email = request.form['email']

    output_file = 'mashup_output.mp3'

    success = mashup(singer, num_videos, duration, output_file)

    if success:
        with zipfile.ZipFile('mashup_result.zip', 'w') as zipf:
            zipf.write(output_file)
        send_email(email, 'mashup_result.zip')
        os.remove(output_file)
        return 'Mashup result sent to your email!'
    else:
        return 'Error occurred during mashup. Please try again later.'

if __name__ == '__main__':
    app.run(debug=True)
