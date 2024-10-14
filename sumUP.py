from transformers import pipeline

class summarizerText:
    def __init__(self, givTexts):
        self.text = givTexts
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def split_text(self, chunk_size=1024):
        # Split text into chunks of up to chunk_size tokens
        sentences = self.text.split('. ')  # Split by sentence
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length <= chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(". ".join(current_chunk) + ".")
                current_chunk = [sentence]
                current_length = sentence_length
        
        if current_chunk:
            chunks.append(". ".join(current_chunk) + ".")
        
        return chunks

    def sum_up(self):
        text_chunks = self.split_text()  # Split the text into manageable chunks
        summary_chunks = []
        
        for chunk in text_chunks:
            ret = self.summarizer(chunk, max_length=50, min_length=10, do_sample=False)
            summary_chunks.append(ret[0]['summary_text'])
        
        return " ".join(summary_chunks)  # Combine the summarized chunks into a final summary


