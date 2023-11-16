import json
import random
import requests
import librosa
import soundfile as sf
import pydub
import wave
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip

print("Starting the video generation process...")

# Fetch multiple random videos from Pexels API
print("Fetching video URLs from Pexels API...")
response = requests.get("https://api.pexels.com/videos/search?query=night+drive", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
response_json = json.loads(response.text)
video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
random.shuffle(video_urls)

print(f"Loaded {len(video_urls)} video URLs.")

# Load audio file and detect bpm
print("Loading audio file and detecting BPM...")
audio, sr = librosa.load("dreams.mp3.mp3", mono=True)
audio_duration = librosa.get_duration(y=audio, sr=sr)
tempo = librosa.beat.tempo(y=audio, sr=sr)[0]
print(f"Loaded audio file with BPM of {tempo}.")

# Convert audio data to mp3 file
print("Converting audio data to mp3 file...")
with wave.open("audio.wav", "w") as wav_file:
    wav_file.setparams((1, 2, sr, 0, "NONE", "not compressed"))
    wav_file.writeframes(audio.tobytes())
audio_mp3 = pydub.AudioSegment.from_file("audio.wav", format="wav")
audio_mp3.export("audio.mp3", format="mp3")
print("Audio data converted to mp3 file.")

# Prepare a list to store the subclips
subclips = []

# Calculate the number of clips needed and the duration of each clip
subclip_duration = 60/tempo
num_clips = int(audio_duration / subclip_duration)
print(f"Preparing to create {num_clips} subclips of duration {subclip_duration} seconds.")

# Process each video
for i in range(num_clips):
    # Load video file
    video_url = video_urls[i % len(video_urls)]
    try:
        print(f"Loading video file from {video_url}...")
        video = VideoFileClip(video_url)
    except OSError:
        print(f"Error: Unable to load video from {video_url}. Skipping...")
        continue
    # Calculate start and end times for this subclip in the video
    start_time = (i * subclip_duration) % video.duration
    end_time = start_time + subclip_duration
    print(f"Extracting subclip from time {start_time} to {end_time}...")
    # Extract subclip and add it to the list
    subclip = video.subclip(start_time, end_time)
    subclips.append(subclip)
    print(f"Subclip extracted and added to the list.")

print("Concatenating all subclips into final video...")
final_video = concatenate_videoclips(subclips)
print("Loading final audio file...")
final_audio = AudioFileClip("audio.mp3")
print("Attaching audio to the final video...")
final_video = final_video.set_audio(final_audio)
print("Writing final video file to disk...")
final_video.write_videofile("final_videoBPM.mp4", codec='libx264', audio_codec='aac')
print("Video generation completed!")
