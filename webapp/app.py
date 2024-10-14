from flask import Flask, render_template, Response, url_for, request, redirect, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socket = SocketIO(app)

@app.route('/')
def home():
    return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)