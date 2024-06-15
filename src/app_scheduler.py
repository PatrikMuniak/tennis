from flask_apscheduler import APScheduler
import datetime
import time
import sqlite3
import requests
from const import DB_PATH  
from config import venue_config
scheduler = APScheduler()


@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*14, misfire_grace_time=900)
def retrieve_venue_sessions():
    print("starting to fetch sessions")
    start_date =  datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.today()+datetime.timedelta(days=13)).strftime('%Y-%m-%d')

    for venue in venue_config.get("venue_list"):
        venue_name = venue.get("venue_name")
        venue_id = venue.get("venue_id")
        start = time.time()
        print("Retrieved from config url:",venue.get("url"))
        url = venue.get("url").format(start_date=start_date, end_date=end_date, ts=int(time.time()*1000))
        print(f"Fetching sessions for {venue_name} url: {url}")
        venue_sessions = requests.get(url).content
        end = time.time()
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue_id, venue_name, content) VALUES (?, ?, ?)''', (venue_id, venue_name, venue_sessions) )
        con.commit()
        print(f'Finished fetching data for {venue_name} start: {start_date} end: {end_date} time_request: {round(end-start, 2)} ')
        time.sleep(10)