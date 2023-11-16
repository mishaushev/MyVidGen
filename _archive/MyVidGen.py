def my_vid_gen_exec():
    import json
    import random
    import requests
    import librosa
    import soundfile as sf
    import pydub
    import wave
    from tqdm import tqdm

    from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

    print("Starting VidGenerator...")

    # Fetch multiple random videos from Pexels API
    response = requests.get("https://api.pexels.com/videos/search?query=beach", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
    print("Response received from Pexels API")
    response_json = json.loads(response.text)
    print("Response JSON loaded")
    video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
    random.shuffle(video_urls)
    print("Video URLs shuffled")

    # Randomly pick 3 videos
    video_urls = random.sample(video_urls, 3)

    # Load audio file and detect bpm
    print("Loading audio file and detecting BPM...")
    audio, sr = librosa.load("dreams.mp3.mp3", mono=True)
    audio_duration = librosa.get_duration(y=audio, sr=sr)

    # Convert audio data to mp3 file
    print("Converting audio data to mp3 file...")
    with wave.open("audio.wav", "w") as wav_file:
        wav_file.setparams((1, 2, sr, 0, "NONE", "not compressed"))
        wav_file.writeframes(audio.tobytes())
    audio_mp3 = pydub.AudioSegment.from_file("audio.wav", format="wav")
    audio_mp3.export("audio.mp3", format="mp3")
    print("Audio converted to mp3.")

    # Prepare a list to store the subclips
    subclips = []

    # Calculate the number of clips needed and the duration of each clip
    num_clips = 100  # We will create 100 subclips
    subclip_duration = audio_duration / num_clips  # Adjust the duration of each subclip so that they cover the entire audio

    print(f"Generating {num_clips} video clips of {subclip_duration} seconds each...")

    for i in tqdm(range(num_clips), desc="Generating video clips"):
        # Choose a video URL, looping back to the start if necessary
        video_url = video_urls[i % len(video_urls)]
        # Try to load video file
        try:
            video = VideoFileClip(video_url)
        except OSError:
            print(f"Error: Unable to load video from {video_url}")
            continue
        # Calculate start and end times for this subclip in the video
        start_time = (i * subclip_duration) % video.duration
        end_time = start_time + subclip_duration
        if end_time > video.duration:
            end_time = video.duration  # Clip to video duration if necessary
        # Extract subclip and add it to the list
        subclip = video.subclip(start_time, end_time)
        subclips.append(subclip)

    print("Concatenating subclips...")
    final_video = concatenate_videoclips(subclips)

    print("Writing final video file with audio...")
    final_audio = AudioFileClip("audio.mp3")
    final_video.write_videofile("final_videoBPM.mp4", codec='libx264', audio=final_audio, audio_codec='aac')

    print("Video generation completed!")

# Call the function
my_vid_gen_exec()
