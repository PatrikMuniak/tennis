import os

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