import sqlite3
import json
import time
import datetime

DB_PATH = "data/tcbl.db"

def run(query_out):
    for query in query_out:
        venue_sessions = json.loads(query[2])

        count_sessions = 0
        for court in venue_sessions.get("Resources"):
            court_name = court.get("Name")

            for day in court.get("Days"):

                date = day.get("Date")
                if date == "2024-06-28T00:00:00":
                    for session in day.get("Sessions"):
                        name = session.get("Name")
                        start = session.get("StartTime")
                        end = session.get("EndTime")
                        if name == "6"or name=="10":
                            if end - start > 60:
                                for i in range(((end-start)//60)):
                                    count_sessions+=1
                            else:
                                count_sessions+=1

        print(f"{query[0]}|{count_sessions}|")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
for day in range(10,30):
    for s, e in [("00:00:00","10:00:00"),
                 ("10:00:00","20:00:00"),
                 ("20:00:00","23:59:59")]:
        cur.execute(f'select * from requests where venue_id="lyle" and dt>="2024-06-{day} {s}" and dt<="2024-06-{day} {e}";' )
        query_output = cur.fetchall()
        run(query_output)

