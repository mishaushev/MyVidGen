import subprocess

def my_vid_gen_exec():
    import json
    import random
    import requests
    import librosa
    import soundfile as sf
    import pydub
    import wave
    import os
    import shutil
    from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

    print("Starting VidGenerator...")

    # Fetch multiple random videos from Pexels API
    response = requests.get("https://api.pexels.com/videos/search?query=flowers", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
    print("Response received from Pexels API")
    response_json = json.loads(response.text)
    print("Response JSON loaded")
    video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]

    # Randomly pick 1 video
    video_url = random.choice(video_urls)

    # Load audio file and detect bpm
    print("Loading audio file and detecting BPM...")
    audio_file_path = "Input/014 Beat 2023 wav.wav"
    audio, sr = librosa.load(audio_file_path, mono=True)
    audio_duration = librosa.get_duration(y=audio, sr=sr)

    # Calculate the number of clips needed
    num_clips = int(audio_duration // 2)  # Each video clip is roughly 2 seconds

    # Download the video
    print(f"Downloading video from {video_url}...")
    video_file_path = "Exports/temp.mp4"
    with requests.get(video_url, stream=True) as r:
        with open(video_file_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print(f"Video downloaded to {video_file_path}")

    # Load the video
    video = VideoFileClip(video_file_path)

    # Generate the video clips
    print("Generating video clips...")
    subclips = []
    for i in range(num_clips):
        start_time = (i * 2) % video.duration
        end_time = start_time + 2
        if end_time > video.duration:
            end_time = video.duration  # Clip to video duration if necessary
        subclip = video.subclip(start_time, end_time)
        subclips.append(subclip)

    # Loop the video until it matches the length of the audio
    while len(subclips) * 2 < audio_duration:
        subclips.extend(subclips)

    # Trim the excess video to match the length of the audio
    subclips = subclips[:int(audio_duration // 2)]

    # Create the final clip
    print("Creating the final clip...")
    final_clip = concatenate_videoclips(subclips)

    print("Writing final video file...")
    final_clip.write_videofile("Exports/final_video_no_audio.mp4", codec='libx264')

    print("Merging audio and video...")
    # This command takes the video without audio and the original audio file, and creates a new video file that has the audio attached.
    # This is done using the ffmpeg software. The "-ar 44100" flag resamples the audio to 44100 Hz, which should be compatible with most videos.
    command = ['ffmpeg', '-i', 'Exports/final_video_no_audio.mp4', '-i', audio_file_path, '-c:v', 'copy', '-c:a', 'aac', '-ar', '44100', 'Exports/final_videoBPM.mp4']
    subprocess.run(command, check=True)

    print("Video generation completed!")

# Call the function
my_vid_gen_exec()
