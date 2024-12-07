from flask_apscheduler import APScheduler
import datetime
import time
import sqlite3
import requests
from const import DB_PATH  
from config import venues_cfg
from models.request import Request
from models.free_sessions import FreeSessions
import logging

scheduler = APScheduler()


@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*5, misfire_grace_time=900) #60*14
def retrieve_venue_sessions():
    logging.info("starting to fetch sessions")
    start_date =  datetime.datetime.today()
    end_date = (datetime.datetime.today()+datetime.timedelta(days=13))

    for venue_id in venues_cfg.venue_list.ids():
        start = time.time()
        url = venues_cfg.venue_list.generate_pull_url(venue_id, start_date, end_date)
        logging.info(f"Fetching sessions for {venue_id} url: {url}")
        venue_sessions = requests.get(url).content
        end = time.time()
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue_id, content) VALUES (?, ?)''', (venue_id, venue_sessions) )
        con.commit()
        r = Request()
        r.load_json(venue_sessions)
        s = FreeSessions(venue_id, r, venues_cfg)

        for session in s.get_sessions():
            
            request_date = int(time.time())
            court_name = session["court_name"]
            date = session["date"]
            sessionName = session["sessionName"] 
            
            start = session["start"]
            end = session["end"]
            venue_name = session["venue_name"] 
            booking_url = session["booking_url"] 
            cur.execute('''INSERT INTO sessions 
                            (request_date,
                            court_name,
                            date, 
                            sessionName, 
                            start, 
                            end, 
                            venue_name, 
                            venue_id, 
                            booking_url) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (request_date,
               court_name,
               date,
               sessionName,
               start,
               end,
               venue_name,
               venue_id,
               booking_url))
        con.commit()
        logging.info(f'Finished fetching data for {venue_id} start: {start_date} end: {end_date} time_request: {round(end-start, 2)} ')
        time.sleep(10)
