from flask import Flask, render_template, jsonify
from flask_apscheduler import APScheduler
import pickle
import requests
import datetime
import sqlite3
import json
import time
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.abspath('..'),"data","tcbl.db")

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# @scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
# def job1():
#     print('Job 1 executed')

@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*14, misfire_grace_time=900)
def retrieve_venue_sessions():
    print("starting to fetch sessions")
    start_date =  datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.today()+datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    venue_names = ["lyle", "canning","royalvictoria", "stratford"]
    for venue_name in venue_names:
        print(f"Fetching sessions for {venue_name}")
        venue_sessions = requests.get(f'https://{venue_name}.newhamparkstennis.org.uk/v0/VenueBooking/lyle_newhamparkstennis_org_uk/GetVenueSessions?resourceID=&startDate={start_date}&endDate={end_date}').content
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue, content) VALUES (?, ?)''', (venue_name, venue_sessions) )
        con.commit()
        print(f'Finished fetching data for {venue_name} start: {start_date} end: {end_date}')
        time.sleep(30)


def get_venue_sessions(venue_name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''select * from requests where venue=? order by rowid desc limit 1;''', (venue_name,) )
    query_out = cur.fetchone()

    venue_sessions = json.loads(query_out[2])
    venue_name = query_out[1]
    sessions = []

    for court in venue_sessions.get("Resources"):
        court_name = court.get("Name")
        for day in court.get("Days"):
            date = time.mktime(datetime.datetime.strptime(day.get("Date"), "%Y-%m-%dT%H:%M:%S").timetuple())
            for session in day.get("Sessions"):
                name = session.get("Name")
                start = session.get("StartTime")
                end = session.get("EndTime")
                if name == "6"or name=="10":
                    if end - start > 60:
                        for i in range(((end-start)//60)):
                            start_sess = start +60*i
                            end_sess = start +60*(i+1)
                            assert end_sess<=end
                            sessions.append({
                                "venue_name":venue_name,
                                "date":date,
                                "court_name":court_name,
                                "name":name,
                                "start":start_sess,
                                "end":end_sess})
                    else:
                        sessions.append({"venue_name":venue_name,"date":date,"court_name":court_name,"name":name,
                                         "start":start,
                                         "end":end})
    return sessions
    

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/GetVenueSessions") 
def get_venue_session():
    venue_names = ["lyle", "canning","royalvictoria", "stratford"]
    data = []

    for venue_name in venue_names:
        data+=get_venue_sessions(venue_name)
    
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
