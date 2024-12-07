from const import VENUE_NAME, BOOKING_URL, VENUE_ID, LATLNG
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

def get_time_from_int(time_int):
    return f"{time_int // 60}:{time_int%60}"

def inflate_booking_url(url_template, date):
    # url template should be an obj, at themoment the func is aware of the format of the str and the parameter
    date_str = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
    inflated_url = url_template.format(date=date_str)
    return inflated_url

def generate_booking_url(venue_id, date): 
    url_template = venues_cfg.venue_list.get_by_id(venue_id, BOOKING_URL)[0]
    inflated_url = inflate_booking_url(url_template, date)
    return inflated_url

@time_it
def get_venue_sessions(venue_id):
    return rq.get_inflated_last_request(venue_id)


def get_venues_list():

    return venues_cfg.venue_list.retrieve_params(VENUE_NAME, VENUE_ID)

def get_venues_for_map():
    # the function is aware of the fields names
    return venues_cfg.venue_list.retrieve_params(VENUE_NAME, VENUE_ID, LATLNG)


