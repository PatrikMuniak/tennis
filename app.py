from flask import Flask, render_template
import pickle
import requests
from datetime import datetime

app = Flask(__name__)

def get_venue_sessions(venue_name):
    sessions = []
    venue_sessions = requests.get(f'https://{venue_name}.newhamparkstennis.org.uk/v0/VenueBooking/lyle_newhamparkstennis_org_uk/GetVenueSessions?resourceID=&startDate=2024-06-01&endDate=2024-06-14&roleId=&_=1717152154207').json()
    for court in venue_sessions.get("Resources"):
        court_name = court.get("Name")
        for day in court.get("Days"):
            date = datetime.strptime(day.get("Date"), "%Y-%m-%dT%H:%M:%S").strftime("%A, %d/%m/%Y")
            for session in day.get("Sessions"):
                # print(session)
                name = session.get("Name")
                start = session.get("StartTime")
                end = session.get("EndTime")
                if name == "6"or name=="10":
                    if end - start > 60:
                        for i in range((end-start//60)+1):
                            start_sess = start +60*i
                            end_sess = start +60*(i+1)
                            sessions.append({"venue_name":venue_name,"date":date,"court_name":court_name,"name":name,"start":start_sess/60,"end":end_sess/60})
                    else:
                        sessions.append({"venue_name":venue_name,"date":date,"court_name":court_name,"name":name,"start":start/60,"end":end/60})
        return sessions
    

@app.route("/")
def main():
    print("making request")
    venue_names = ["lyle", "canning","royalvictoria", "stratford"]
    sessions_table = []

    for venue_name in venue_names:
        sessions_table+=get_venue_sessions(venue_name)
    
    
    return render_template("main.html", sessions_table=sessions_table)

