from flask import Blueprint, request, redirect
import requests

from datetime import datetime, timedelta

from services.auth_services import *
from database import get_db_connection

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/authorize')
def handle_authorize():
    return redirect(authorize_url())

@auth_bp.route('/callback')
def handle_callback():
    callback(request.args.get('code'))
    return "Spotify account linked successfully! You can close this window."


