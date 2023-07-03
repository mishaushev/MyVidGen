def my_vid_gen_exec():
    import json
    import requests
    import librosa
    import soundfile as sf
    import pydub
    import wave
    from tqdm import tqdm
    from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
    import urllib.request

    print("Starting VidGenerator...")

    # Fetch a random video from Pexels API
    response = requests.get("https://api.pexels.com/videos/search?query=beach", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
    print("Response received from Pexels API")
    response_json = json.loads(response.text)
    print("Response JSON loaded")
    video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
    # Randomly pick 1 video
    video_url = random.choice(video_urls)

    # Load audio file and detect bpm
    print("Loading audio file and detecting BPM...")
    audio, sr = librosa.load("dreams.mp3", mono=True)
    audio_duration = librosa.get_duration(y=audio, sr=sr)
    tempo = librosa.beat.tempo(y=audio, sr=sr)[0]

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
    subclip_duration = 60 / tempo
    num_clips = int(audio_duration / subclip_duration)

    print(f"Generating {num_clips} video clips of {subclip_duration} seconds each...")

    try:
        print(f"Downloading video file from {video_url}...")
        urllib.request.urlretrieve(video_url, "temp.mp4")
        print(f"Loading video file from {video_url}...")
        video = VideoFileClip("temp.mp4")
    except Exception as e:
        print(f"Error: Unable to load video from {video_url}. Exiting...")
        print(f"Exception: {str(e)}")
        return

    for i in tqdm(range(num_clips), desc="Generating video clips"):
        # Calculate start and end times for this subclip in the video, looping back to the start if necessary
        start_time = (i * subclip_duration) % video.duration
        end_time = start_time + subclip_duration
        if end_time > video.duration:
            end_time = video.duration  # Clip to video duration if necessary
        # Extract subclip and add it to the list
        subclip = video.subclip(start_time, end_time)
        subclips.append(subclip)

    print("Concatenating subclips...")
    final_video = concatenate_videoclips(subclips)

    print("Loading audio file...")
    final_audio = AudioFileClip("audio.mp3")
    
    print("Finalizing video with audio...")
    final_clip = final_video.set_audio(final_audio)

    print("Writing final video file...")
    final_clip.write_videofile("final_videoBPM.mp4", codec='libx264')

    print("Video generation completed!")

# Call the function
my_vid_gen_exec()
