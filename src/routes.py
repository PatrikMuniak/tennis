import json
from flask import Blueprint, render_template, jsonify, request
from utils import get_venue_sessions, get_venues_list
from config import venue_config

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route("/")
def main():
    return render_template("main.html")

@pages.route("/map")
def map():
    return render_template("map.html")

@pages.route("/GetVenueSessions") 
def get_venue_session():
    venue_id = request.args.get('venueId')
    # venue_names = [venue.get("venue_id") for venue in venue_config.get("venue_list")]
    # venue_names = ["stratford"]
    data = []

    # for venue_id in venue_names:
    data+=get_venue_sessions(venue_id)
    print(venue_id, len(data))
    
    return jsonify(data)


@pages.route("/venues") 
def get_venues():
    data = get_venues_list()
    return jsonify(data)
