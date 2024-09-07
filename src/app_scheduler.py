from flask_apscheduler import APScheduler
import datetime
import time
import sqlite3
import requests
from const import DB_PATH  
from config import venues_cfg

scheduler = APScheduler()


@scheduler.task('interval', id='retrieve_venue_sessions', seconds=1, misfire_grace_time=900) #60*14
def retrieve_venue_sessions():
    print("starting to fetch sessions")
    start_date =  datetime.datetime.today()
    end_date = (datetime.datetime.today()+datetime.timedelta(days=13))

    for venue_id in venues_cfg.venue_list.ids():
        start = time.time()
        url = venues_cfg.venue_list.generate_pull_url(venue_id, start_date, end_date)
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