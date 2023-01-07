import os
import requests
from pytube import YouTube
from tqdm import tqdm

# Prompt user to enter URL of YouTube video
url = input("Enter the URL of the YouTube video: ")

# Connect to YouTube and retrieve video information
yt = YouTube(url)

# Display title of video
print(yt.title)

# Download best available video in highest resolution
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# Determine current directory where script is located
current_folder = os.path.dirname(os.path.abspath(__file__))

# Create and configure tqdm widget
t = tqdm(total=video.filesize, unit='B', unit_scale=True, desc=video.title, leave=True)

# Retrieve download URL
response = requests.get(video.url, stream=True)

# Download video in chunks and display progress
chunk_size = 1024
for chunk in response.iter_content(chunk_size=chunk_size):
    t.update(len(chunk))
    with open(os.path.join(current_folder, video.default_filename), 'ab') as f:
        f.write(chunk)

# Close tqdm widget after download is complete
t.close()


