from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-text', methods=['POST'])
def submit_text():
    data = request.get_json()
    user_text = data.get('userText', '')
    response_message = f'Received: {user_text}'
    return jsonify({'message': response_message})

if __name__ == '__main__':
    app.run(debug=True)

