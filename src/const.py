import os
import json
from collections import namedtuple


DB_PATH = os.path.join(os.path.abspath('..'),"data","tcbl.db")
CONFIG_PATH = "config.yaml"

# constants for values here randomly on const are too scattered and are not part of a group so people can make a mistake and 
# chnage them and use them somewhere else 
VENUE_LIST = "venue_list"
VENUE_NAME = "venue_name"
VENUE_ID = "venue_id"
URL = "url"
BOOKING_URL = "booking_url"
LATLNG = "latlng"



request_fields = ("Resources",)
Request = namedtuple("Request", request_fields)

REQUEST = Request(*request_fields)

resources_fileds = ("Name", "Days")
Resources = namedtuple("Resources", resources_fileds)
RESOURCES = Resources(*resources_fileds)

# print(Request.Resources)

# Days
days_fileds = ("Date", "Sessions")
Days = namedtuple("Days", days_fileds)
DAYS = Days(*days_fileds)

# Sessions
sessions_fileds = ("Name", "StartTime", "EndTime")
Sessions = namedtuple("Sessions", sessions_fileds)
SESSIONS = Sessions(*sessions_fileds)


