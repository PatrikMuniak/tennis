import yaml
from const import VENUE_LIST, CONFIG_PATH, BOOKING_URL
from collections.abc import Sequence
import datetime
import time
# every request is a for loop, it can be optimized
# if a parameter is missing there should be an error
 



class VenueEntry(object):
    def __init__(self, venue_name, venue_id, url, booking_url, latlng):
        self.venue_name = venue_name
        self.venue_id = venue_id
        self.url = url
        self.booking_url = booking_url
        self.latlng = latlng
    
    def get(self, name: str) -> str:
        return getattr(self, name)
    
    def __repr__(self):
        return "VenueEntry(venue_name={} venue_id={} url={} booking_url={} latlng={})".format(self.venue_name, self.venue_id, self.url, self.booking_url, self.latlng)
    
class VenueList(object):
    def __init__(self):
        self._venue_list = []

    def add_entry(self, **kvargs):
        entry = VenueEntry(**kvargs)
        self._venue_list.append(entry)

    def list_entries(self):
        for entry in self._venue_list:
            print(entry)

    def __len__(self):
        return len(self._venue_list)

    def ids(self):
        ids = set()
        for entry in self._venue_list:
            ids.add(entry.venue_id)
        if len(ids) != len(self._venue_list):
            raise Exception("Venue missing id in config")
        return ids
    
    def has_id(self, id):
        if id in self.ids():
            return True
        else:
            return False
    
    def get_by_id(self, key, *args):
        for venue in self._venue_list:
            if key == venue.venue_id:
                row = list()
                for arg in args:
                    row.append(venue.get(arg))
                return tuple(row)
        return -1

    def retrieve_params(self, *args) -> dict:
        out = []
        for venue in self._venue_list:
            row = {}
            for arg in args:
                row[arg]=venue.get(arg)

            out.append(row)

        return out
    
    def inflate_pull_url(self, url_template, start_date, end_date):
        start = start_date.strftime('%Y-%m-%d')
        end = end_date.strftime('%Y-%m-%d')
        ts = int(time.time()*1000)
        inflated_url = url_template.format(start_date=start, end_date=end, ts=ts)
        return inflated_url

    def generate_pull_url(self, venue_id, start_date, end_date):
        url_template = self.get_by_id(venue_id, "url")[0]
        inflated_url = self.inflate_pull_url(url_template, start_date, end_date)
        return inflated_url

class VenueConfig:
    def __init__(self):
        self.venue_list = VenueList()
        self.cfg_path = None

    def get_config(self):
        venue_config = None
        with open(self.cfg_path, 'r') as file:
            venue_config = yaml.safe_load(file)
        
        return venue_config
    
    def set_cfg_path(self, cfg_path):
        self.cfg_path = cfg_path

    def load_venue_list(self):
        venue_config = self.get_config()
        venue_list_dict = venue_config.get(VENUE_LIST)
        vn_lst = VenueList()
        for venue in venue_list_dict:
            vn_lst.add_entry(**venue)
        self.venue_list = vn_lst

venues_cfg = VenueConfig()
venues_cfg.set_cfg_path(CONFIG_PATH)
venues_cfg.load_venue_list()



