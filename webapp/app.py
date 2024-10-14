from flask import Flask, request, render_template, jsonify
from backend import Backend 

app = Flask(__name__)
backend = Backend()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form.get('link')
    
    if not video_link:
        return render_template('index.html', error="No link provided")
    
    backend.video_to_mp3(video_link)
    summary = backend.sum_up()
    
    if summary:
        # Pass the title along with the summary to the template
        return render_template('index.html', summary=summary, title=backend.video_title, link=video_link)
    else:
        return render_template('index.html', error="Failed to summarize the video")


if __name__ == '__main__':
    app.run(debug=True)
