import json
import random
import requests
import librosa
import soundfile as sf
import pydub
import wave
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Fetch multiple random videos from Pexels API
response = requests.get("https://api.pexels.com/videos/search?query=night+drive", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
response_json = json.loads(response.text)
video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
random.shuffle(video_urls)

# Load audio file and detect bpm
audio, sr = librosa.load("hyper-drive_TK14031475.mp3.mp3", mono=True)
tempo = librosa.beat.tempo(y=audio, sr=sr)[0]

# Convert audio data to mp3 file
with wave.open("audio.wav", "w") as wav_file:
    wav_file.setparams((1, 2, sr, 0, "NONE", "not compressed"))
    wav_file.writeframes(audio.tobytes())
audio_mp3 = pydub.AudioSegment.from_file("audio.wav", format="wav")
audio_mp3.export("audio.mp3", format="mp3")

# Prepare a list to store the subclips
subclips = []

# Process each video
for i, video_url in enumerate(video_urls):
    # Load video file
    video = VideoFileClip(video_url)
    # Calculate the duration of each subclip based on the bpm of the song
    subclip_duration = 60/tempo
    # Create subclips for the entire duration of the video
    for j in range(int(video.duration/subclip_duration)):
        start_time = j*subclip_duration
        end_time = start_time + subclip_duration
        subclip = video.subclip(start_time, end_time)
        subclips.append(subclip)

final_video = concatenate_videoclips(subclips)
final_audio = pydub.AudioSegment.from_file("hyper-drive_TK14031475.mp3.mp3", format="mp3")
final_video.write_videofile("final_videoBPM.mp4", codec='libx264', audio_codec='aac')
