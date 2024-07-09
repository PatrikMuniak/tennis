from flask_apscheduler import APScheduler
import datetime
import time
import sqlite3
import requests
from const import DB_PATH  
from config import venues_cfg

scheduler = APScheduler()


@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*14, misfire_grace_time=900)
def retrieve_venue_sessions():
    print("starting to fetch sessions")
    start_date =  datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.today()+datetime.timedelta(days=13)).strftime('%Y-%m-%d')

    for venue in venues_cfg.venue_list.ids():
        venue_id = venue.get("venue_id")
        start = time.time()
        print("Retrieved from config url:",venue.get("url"))
        url = venue.get("url").format(start_date=start_date, end_date=end_date, ts=int(time.time()*1000))
        print(f"Fetching sessions for {venue_id} url: {url}")
        venue_sessions = requests.get(url).content
        end = time.time()
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue_id, content) VALUES (?, ?)''', (venue_id, venue_sessions) )
        con.commit()
        print(f'Finished fetching data for {venue_id} start: {start_date} end: {end_date} time_request: {round(end-start, 2)} ')
        time.sleep(10)

# I query like here but then I process 

# scrape_dt, venue_id, startTime, endTime, 


# whenever we query we query we need to loop through as we need to inlate some values, so maybe just put the values 

# if we insert the rows every time then we just pick 