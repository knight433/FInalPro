import whisper
import sumUP

# model = whisper.load_model("base")
# result = model.transcribe("path_to_save/The Worst Hotel in Las Vegas.mp3")
# print(result["text"])

te = '''The sun is shining brightly today. It is a perfect day for a walk in the park. Many people are enjoying the weather, playing games, and having picnics. The flowers are blooming, and the birds are singing. Everyone seems to be in a good mood, appreciating the beautiful day.'''


sumer = sumUP.summarizerText(te)
print(sumer.sum_up())


