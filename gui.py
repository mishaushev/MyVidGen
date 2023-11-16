import tkinter as tk
from tkinter import filedialog
import MyVidGenOne  # Assuming your script is in MyVidGenOne.py

def select_audio():
    global audio_path
    audio_path = filedialog.askopenfilename()  # User selects the audio file
    audio_label.config(text=audio_path)

def my_vid_gen_exec():
    api_key = api_key_entry.get()
    query = query_entry.get()
    MyVidGenOne.my_vid_gen_exec(audio_path, api_key, query)
  # Call your script function

# Create the main window
root = tk.Tk()
root.title("Video Generator")

# Audio File Selection
audio_label = tk.Label(root, text="Select an Audio File")
audio_label.pack()
audio_button = tk.Button(root, text="Browse", command=select_audio)
audio_button.pack()

# Pexels API Input
api_key_label = tk.Label(root, text="Enter Pexels API Key")
api_key_label.pack()
api_key_entry = tk.Entry(root)
api_key_entry.pack()

# Search Query Input
query_label = tk.Label(root, text="Enter Search Query")
query_label.pack()
query_entry = tk.Entry(root)
query_entry.pack()

# Generate Button
generate_button = tk.Button(root, text="Generate Video", command=my_vid_gen_exec)
generate_button.pack()

# Run the application
root.mainloop()
