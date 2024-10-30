from flask import Blueprint, render_template, jsonify

from services.overview_services import *
from services.statistic_services import get_statistics, get_activity

over_bp = Blueprint('over_bp', __name__)

@over_bp.route('/statistics')
def statistics():
    return render_template('statistics.html', data=get_statistics())

@over_bp.route('/api/activity', methods=['GET'])
def activity():
    data = get_activity()
    return jsonify(data)

@over_bp.route('/current_song', methods=['GET'])
def current_song():
    return get_current_song_and_check_playlists(), 200