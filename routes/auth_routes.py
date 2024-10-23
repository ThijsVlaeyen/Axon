from flask import Blueprint, request, redirect, render_template

from services.auth_services import *

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/authorize')
def handle_authorize():
    return redirect(authorize_url())

@auth_bp.route('/authenticate')
def authenticate():
    return render_template('authenticate.html')

@auth_bp.route('/callback')
def handle_callback():
    callback(request.args.get('code'))
    return "Spotify account linked successfully! You can close this window."


