# Assignment-5: MASHUP

# Name: Hrsh Dhingra
# Roll no. 102103443

import os
import sys
import subprocess
from pytube import YouTube
from pydub import AudioSegment


def download_videos(singer, num_videos):
    try:
        for i in range(num_videos):
            query = f'{singer} song'
            yt = YouTube(f"https://www.youtube.com/results?search_query={query}")
            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path='downloads', filename=f'video_{i}')
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Unable to download videos. Please try again later.")
        return

def convert_to_audio():
    for filename in os.listdir('downloads'):
        if filename.endswith('.mp4'):
            mp4_file = os.path.join('downloads', filename)
            audio = AudioSegment.from_file(mp4_file, format="mp4")
            audio.export(os.path.join('audios', f'{filename[:-4]}.mp3'), format="mp3")
            os.remove(mp4_file)

def cut_audio(duration):
    for filename in os.listdir('audios'):
        if filename.endswith('.mp3'):
            mp3_file = os.path.join('audios', filename)
            audio = AudioSegment.from_file(mp3_file, format="mp3")
            audio = audio[:duration * 1000]  
            audio.export(os.path.join('cut_audios', filename), format="mp3")

def merge_audios(output_file):
    audio_files = [os.path.join('cut_audios', file) for file in os.listdir('cut_audios') if file.endswith('.mp3')]
    combined = AudioSegment.empty()
    for file in audio_files:
        combined += AudioSegment.from_file(file, format="mp3")
    combined.export(output_file, format="mp3")

def mashup(singer, num_videos, duration, output_file):
    try:
        download_videos(singer, num_videos)
        convert_to_audio()
        cut_audio(duration)
        merge_audios(output_file)
        print("Mashup completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)
    
    singer = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_file = sys.argv[4]
    mashup(singer, num_videos, duration, output_file)
