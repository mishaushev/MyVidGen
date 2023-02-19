def my_vid_gen_exec():
    
    import json
    import random
    import requests
    import librosa
    import soundfile as sf
    import pydub
    import wave

    from moviepy.editor import VideoFileClip, concatenate_videoclips

    # Fetch multiple random videos from Pexels API
    response = requests.get("https://api.pexels.com/videos/search?query=beach", headers={"Authorization": "jXIcrareVIEdvejaJkrhTrlbsiDc2D1BtUOSWoZw6sv5om8ggLuY6BWw"})
    print("Response received from Pexels API")
    response_json = json.loads(response.text)
    print("Response JSON loaded")
    video_urls = [v['video_files'][0]['link'] for v in response_json['videos']]
    random.shuffle(video_urls)
    print("Video URLs shuffled")

    # Load audio file and detect beats
    audio, sr = librosa.load("hyper-drive_TK14031475.mp3.mp3", mono=True)
    print("Audio loaded")
    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
    print("Beats detected")
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print("Beat times calculated")

    # Convert audio data to mp3 file

    # write the numpy array to a wave file
    with wave.open("audio.wav", "w") as wav_file:
        wav_file.setparams((1, 2, sr, 0, "NONE", "not compressed"))
        wav_file.writeframes(audio.tobytes())
    print("Audio data written to wave file")

    # Convert audio data to mp6 file
    audio_mp3 = pydub.AudioSegment.from_file("audio.wav", format="wav")
    print("Audio data converted to mp3 format")
    audio_mp3.export("audio.mp3", format="mp3")
    print("Audio data exported to mp3 file")

    # Prepare a list to store the subclips
    subclips = []   

    #Process each video

    for i, video_url in enumerate(video_urls):
        # Load video file
        video = VideoFileClip(video_url)
        print(f"Video {i+1} loaded")
        video_duration = 2
        beat_times_filtered = [time for time in beat_times if time < video_duration]
        for beat_time in beat_times_filtered:
            subclip = video.subclip(0, beat_time)
            subclips.append(subclip)
        print(f"Subclips of video {i+1} extracted")

    final_video = concatenate_videoclips(subclips)

    print("Subclips concatenated to form final video")
    final_audio = pydub.AudioSegment.from_file("hyper-drive_TK14031475.mp3.mp3", format="mp3")
    print("Audio file loaded")
    final_audio.export("audio.mp3", format="mp3")
    print("Audio exported to the programm folder")
    final_video.write_videofile("final_video.mp4", audio="audio.mp3", codec='libx264', audio_codec='aac')
    print("Your MVideo is done")
#Call def my_vid_gen():
my_vid_gen_exec()