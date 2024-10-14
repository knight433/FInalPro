from pytubefix import YouTube
from moviepy.editor import AudioFileClip
from transformers import pipeline
import os
import whisper
import math

class Backend:
    def __init__(self):
        self.transcribe_model = whisper.load_model("base")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.filename = ''
        self.video_title = ''  # Add this line to store the video title

    def video_to_mp3(self, link):
        try:
            yt = YouTube(link)
            stream = yt.streams.get_highest_resolution()
            video_file = stream.download(output_path='saved_mp3')
            
            self.video_title = yt.title  # Store the video title here

            print(f"Downloaded: {self.video_title} successfully!")

            mp3_file = video_file.replace(".mp4", ".mp3")
            video_clip = AudioFileClip(video_file)
            video_clip.write_audiofile(mp3_file)

            video_clip.close()
            print(f"Converted to MP3: {mp3_file} successfully!")

            os.remove(video_file)
            print(f"Deleted MP4 file: {video_file} successfully!")

            self.filename = mp3_file  # Correctly assign the filename
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None 

    def __transcribe(self):
        # Use self.filename instead of self.fileName
        result = self.transcribe_model.transcribe(self.filename)
        return result['text']

    def __break_down(self, text, max_length=1024):
        """Breaks the text into smaller chunks."""
        tokens = self.summarizer.tokenizer.encode(text, truncation=False)
        num_chunks = math.ceil(len(tokens) / max_length)

        chunks = []
        for i in range(num_chunks):
            start = i * max_length
            end = start + max_length
            chunk = tokens[start:end]
            chunks.append(self.summarizer.tokenizer.decode(chunk, skip_special_tokens=True))

        return chunks

    def sum_up(self):
        transcribed_text = self.__transcribe()
        
        if transcribed_text:
            chunks = self.__break_down(transcribed_text)
            summaries = []

            for chunk in chunks:
                summary = self.summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])

            final_summary = self.summarizer(" ".join(summaries), max_length=130, min_length=30, do_sample=False)
            return final_summary[0]['summary_text']
        else:
            print("Transcription failed or returned no text.")
            return None
