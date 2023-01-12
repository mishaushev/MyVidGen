import requests
import json
import moviepy.editor as mp
import librosa

# Pexels API key
api_key = "563492ad6f91700001000001ffe8bbcab84343649c1acaaad1a446d9"

# Topic to search for
topic = "jump"

# Download the videos from Pexels
videos = []
res = requests.get(f"https://api.pexels.com/v1/videos/search?query={topic}",headers={"Authorization": api_key})

if res.status_code == 429:
    retry_after = int(res.headers["Retry-After"])
    print(f"API rate limit exceeded, waiting for {retry_after} seconds")
    time.sleep(retry_after)
    res = requests.get(f"https://api.pexels.com/v1/videos/search?query={topic}",headers={"Authorization": api_key})

data = json.loads(res.text)
num_of_videos = min(5, len(data["videos"]))

for i in range(num_of_videos):
    if not data["videos"]:
      break
    video = data["videos"][i]
    if "video_files" in video:
        video_url = video["video_files"][0]["link"]
    elif "url" in video:
        video_url = video["url"]
    elif "download" in video:
        video_url = video["download"]
    else:
        continue
    video = mp.VideoFileClip(video_url)
    videos.append(video)

# Load the audio and get the beats
audio = mp.AudioFileClip("nasty.mp3")
y, sr = librosa.load(audio.filename)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beats = librosa.frames_to_time(beats, sr=sr)

# Chop the videos to the beats
chopped_videos = []
for video in videos:
    chopped_video = mp.concatenate_videoclips([video.subclip(start, end) for start, end in zip(beats, beats[1:])])
    chopped_videos.append(chopped_video)

# Concatenate the videos
final_video = mp.concatenate_videoclips(chopped_videos, method="compose")

# Add audio to video
final_video = final_video.set_audio(audio)

# To increase the audio volume of final video
final_video = final_video.audio_normalize()

# Save the final video
final_video.write_videofile("final_video.mp4", fps=24, preset='1080p')

