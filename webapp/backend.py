from pytubefix import YouTube
from moviepy.editor import AudioFileClip
from transformers import pipeline
import os
import whisper
import math

class Backend:
    def __init__(self):
        self.Transcribe_model = whisper.load_model("base")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def Video_to_Mp3(self, link):
        try:
            yt = YouTube(link)
            stream = yt.streams.get_highest_resolution()
            video_file = stream.download(output_path='saved_mp3')
            
            print(f"Downloaded: {yt.title} successfully!")

            mp3_file = video_file.replace(".mp4", ".mp3")
            video_clip = AudioFileClip(video_file)
            video_clip.write_audiofile(mp3_file)

            video_clip.close()
            print(f"Converted to MP3: {mp3_file} successfully!")

            os.remove(video_file)
            print(f"Deleted MP4 file: {video_file} successfully!")
            
            return mp3_file
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  

    def transcribe(self, fileName):
        result = self.Transcribe_model.transcribe(f"saved_mp3/{fileName}.mp3")
        return result['text'] 

    def breakDown(self, text, max_length=1024):
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

    def sumUp(self, fileName):
        transcribed_text = self.transcribe(fileName)
        
        if transcribed_text:
            chunks = self.breakDown(transcribed_text)
            summaries = []

            for chunk in chunks:
                summary = self.summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])

            final_summary = self.summarizer(" ".join(summaries), max_length=130, min_length=30, do_sample=False)
            return final_summary[0]['summary_text']
        else:
            print("Transcription failed or returned no text.")
            return None
