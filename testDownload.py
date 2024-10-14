from pytubefix import YouTube
from moviepy.editor import *

# Replace with the URL of the YouTube video you want to download
video_url = "https://www.youtube.com/watch?v=3HYfPz8lvDI"  # Replace VIDEO_ID with the actual video ID

try:
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the highest resolution stream (video)
    stream = yt.streams.get_highest_resolution()
    
    # Download the video
    video_file = stream.download(output_path='path_to_save') 

    print(f"Downloaded: {yt.title} successfully!")

    # Convert the downloaded video to MP3
    mp3_file = video_file.replace(".mp4", ".mp3")  
    video_clip = AudioFileClip(video_file)
    video_clip.write_audiofile(mp3_file)

    video_clip.close()

    print(f"Converted to MP3: {mp3_file} successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
