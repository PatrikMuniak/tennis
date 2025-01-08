from flask import Blueprint, render_template, jsonify, request, send_from_directory
from utils import get_venue_sessions, get_venues_list, get_venues_for_map


pages = Blueprint('pages', __name__, template_folder='static/templates')

@pages.route("/")
def main():
    return render_template("main.html")

@pages.route("/map")
def map():
    return render_template("map.html")

@pages.route("/GetVenueSessions") 
def get_venue_session():
    venue_id = request.args.get('venueId')
    data = get_venue_sessions(venue_id)
    return jsonify(data)

@pages.route("/venues") 
def get_venues():
    data = get_venues_list()
    return jsonify(data)

@pages.route("/markerData") 
def get_marker_data():
    data = get_venues_for_map()
    return jsonify(data)

@pages.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')