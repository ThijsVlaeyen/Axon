from flask import Blueprint, render_template

strava_bp = Blueprint('strava_bp', __name__)

@strava_bp.route('/strava')
def strava():
    return render_template('strava.html')