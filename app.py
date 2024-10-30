from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

import atexit
import time
import os

from routes import auth_bp, hist_bp, over_bp
from services.overview_services import *
from services.spotify_db import create_tables

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(hist_bp)
app.register_blueprint(over_bp)

socketio = SocketIO(app)

load_dotenv()
app.config['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIPY_CLIENT_ID')
app.config['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIPY_CLIENT_SECRET')
app.config['SPOTIPY_REDIRECT_URI'] = os.getenv('SPOTIPY_REDIRECT_URI')

thread_started = False
executor = ThreadPoolExecutor(max_workers=2)

def shutdown(signum, frame):
    executor.shutdown(wait=True)

atexit.register(shutdown)

@app.before_request
def startup():
    global thread_started
    if not thread_started:
        thread_started = True
        executor.submit(update_current_track)
        time.sleep(5)
        executor.submit(update_playlists)

@app.route('/')
def home():
    return render_template('overview.html')

@socketio.on('connect')
def handle_connect():
    socketio.emit('song_update', get_current_song_and_check_playlists())

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5050, debug=True)