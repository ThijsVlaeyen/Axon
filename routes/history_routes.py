from flask import Blueprint, render_template, jsonify, request
from services.history_services import *

hist_bp = Blueprint('hist_bp', __name__)

@hist_bp.route('/history')
def history():
    return render_template('history.html')

@hist_bp.route('/recent_songs_data', methods=['GET'])
def recent_songs_data():
    recent_songs = get_recent_songs()
    return jsonify(recent_songs)

@hist_bp.route('/get_status', methods=['GET'])
def get_stat():
    return {'status': get_status()}, 200

@hist_bp.route('/change_status', methods=['POST'])
def change_stat():
    value = request.json.get('value')
    if value != '':
        set_status(value)
        return jsonify({"status": "success", "received_value": value}), 200
    else:
        return jsonify({"status": "error", "message": "No value received"}), 400
    
@hist_bp.route('/change_statistic', methods=['POST'])
def change_stati():
    statistic_id = request.json.get('statistic_id')
    status = request.json.get('status')
    if statistic_id != '' and status != '':
        update_statistic(statistic_id, status)
        return jsonify({"status": "success", "received_value": request.json}), 200
    else:
        return jsonify({"status": "error", "message": "No value received"}), 400