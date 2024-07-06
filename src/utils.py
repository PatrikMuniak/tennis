from const import DB_PATH, VENUE_NAME
import json
import sqlite3
import datetime
import time
from config import venues_cfg
from models import request as rq
import logging


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end =  time.time()
        logging.debug(f"{func.__name__} time:{round(end-start,2)}")
        return res
    return wrapper

def parse_dt_str_to_unix(datetime_string):
    tuple_dt = datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S").timetuple()
    unix_dt = time.mktime(tuple_dt)
    return unix_dt

def inflate_booking_url(url_template, date):
    # url template should be an obj, at themoment the func is aware of the format of the str and the parameter
    date_str = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    inflated_url = url_template.format(date=date_str)
    return inflated_url

def generate_booking_url(venue_id, date): 
    url_template = venues_cfg.venue_list.get_by_id(venue_id, "booking_url")[0]
    inflated_url = inflate_booking_url(url_template, date)
    return inflated_url

@time_it
def get_venue_sessions(venue_id):
    venue_sessions = rq.get_last_request(venue_id)
    venue_name = venues_cfg.venue_list.get_by_id(venue_id, VENUE_NAME)[0]
    print(venue_name)
    sessions = []

    for court in venue_sessions.get("Resources"):
        court_name = court.get("Name")
        for day in court.get("Days"):
            date = parse_dt_str_to_unix(day.get("Date"))
            for session in day.get("Sessions"):
                name = session.get("Name")
                start = session.get("StartTime")
                end = session.get("EndTime")
                booking_url = generate_booking_url(venue_id, date)
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
                                         "end":end,
                                         "booking_url":booking_url})
    return sessions

def get_venues_list():

    return venues_cfg.venue_list.retrieve_params("venue_name", "venue_id")

def get_venues_for_map():
    # the function is aware of the fields names
    return venues_cfg.venue_list.retrieve_params("venue_name", "venue_id", "latlng")

