from flask import Blueprint, render_template

from services.overview_services import *

over_bp = Blueprint('over_bp', __name__)

@over_bp.route('/statistics')
def statistics():
    return render_template('statistics.html')

@over_bp.route('/current_song', methods=['GET'])
def current_song():
    return get_current_song_and_check_playlists(), 200