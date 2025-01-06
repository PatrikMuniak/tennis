from flask_apscheduler import APScheduler
import datetime
import time
import sqlite3
import requests
from const import DB_PATH  
from config import venues_cfg
from models.request import Request, Requests, Database
from models.free_sessions import FreeSessions
import logging


logging.basicConfig(level=logging.INFO)
scheduler = APScheduler()


@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*14, misfire_grace_time=900) #60*14
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

        req = Request()
        req.save(venue_id, venue_sessions)


        
        logging.info(f'Finished fetching data for {venue_id} start: {start_date} end: {end_date} time_request: {round(end-start, 2)} ')
        time.sleep(10)


# req = Request()
#         req.load_json(venue_sessions, venue_id)
#         # passing an empty request doesn't make sense
#         s = FreeSessions(req, venues_cfg)
#         con = sqlite3.connect(DB_PATH)
#         cur = con.cursor()

#         for session in s.get_sessions():
            
#             request_date = int(time.time())
#             court_name = session["court_name"]
#             date = session["date"]
#             sessionName = session["sessionName"] 
            
#             start = session["start"]
#             end = session["end"]
#             venue_name = session["venue_name"] 
#             booking_url = session["booking_url"] 
#             cur.execute('''INSERT INTO sessions 
#                             (request_date,
#                             court_name,
#                             date, 
#                             sessionName, 
#                             start, 
#                             end, 
#                             venue_name, 
#                             venue_id, 
#                             booking_url) 
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#               (request_date,
#                court_name,
#                date,
#                sessionName,
#                start,
#                end,
#                venue_name,
#                venue_id,
#                booking_url))
#         con.commit()



@scheduler.task('interval', id='cleanup_old_requests_records', seconds=60*30, misfire_grace_time=900) #60*14
def cleanup_venue_sessions():
    db = Database(DB_PATH)
    requests = Requests(db)
    requests.remove_records_older_than_a_week()
    
# if something is older than 7 days remove