from flask_apscheduler import APScheduler
import datetime
import time
import requests
from const import DB_PATH  
from config import venues_cfg
from models.request import Request, Requests, DateTs
from models.database import Database

import logging

logging.basicConfig(level=logging.INFO)
scheduler = APScheduler()

@scheduler.task('interval', id='retrieve_venue_sessions', seconds=60*14, misfire_grace_time=900) #60*14
def retrieve_venue_sessions():
    logging.info("starting to fetch sessions")
    start_date =  datetime.datetime.today()
    end_date = (datetime.datetime.today()+datetime.timedelta(days=13))

    for venue_id in venues_cfg.venue_list.ids():
        
        url = venues_cfg.venue_list.generate_pull_url(venue_id, start_date, end_date)
        logging.info(f"Fetching sessions for {venue_id} url: {url}")
        r = requests.get(url)

        dt = DateTs()
        dt.value = time.time()
        req = Request(dt=dt, venue_id=venue_id, content=r.content)

        db = Database(DB_PATH)
        rs_obj = Requests(db)
        rs_obj.insert(req)

        logging.info(f'Finished fetching data for {venue_id} start: {start_date} end: {end_date} time_request: {r.elapsed.total_seconds()} ')
        time.sleep(10)

@scheduler.task('interval', id='cleanup_old_requests_records', seconds=60*30, misfire_grace_time=900)
def cleanup_venue_sessions():
    db = Database(DB_PATH)
    requests = Requests(db)
    requests.remove_records_older_than_a_week()
