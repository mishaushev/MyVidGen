import json
import random
import requests
import librosa
import soundfile as sf
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Fetch multiple random videos from Pexels API
response = requests.get("https://api.pexels.com/videos/search?query=jumping", headers={"Authorization": "563492ad6f91700001000001ffe8bbcab84343649c1acaaad1a446d9"})
response_json = json.loads(response.text)
video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
random.shuffle(video_urls)

# Load audio file and detect beats
audio, sr = sf.read("nasty.mp3", dtype='int16', channels=2)
tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Prepare a list to store the subclips

subclips = []

# Process each video
for i, video_url in enumerate(video_urls):
    # Load video file
    video = VideoFileClip(video_url)
    subclip = video.subclip(0, 2)
    subclips.append(subclip)

final_video = concatenate_videoclips(subclips)
final_video.write_videofile("final_video.mp4")
