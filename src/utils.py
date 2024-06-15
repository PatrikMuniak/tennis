from const import DB_PATH
import json
import sqlite3
import datetime
import time

def get_venue_sessions(venue_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''select * from requests where venue_id=? order by rowid desc limit 1;''', (venue_id,) )
    query_out = cur.fetchone()

    venue_sessions = json.loads(query_out[2])
    venue_name = query_out[3]
    venue_id = query_out[1]
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