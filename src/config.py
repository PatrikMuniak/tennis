import yaml
from const import 

venue_config=None

class Venue(yaml.YAMLObject):
    def __init__(self, venue_name, venue_id, url, booking_url, latlng):
        self.venue_name = venue_name
        self.venue_id = venue_id
        self.url = url
        self.booking_url = booking_url
        self.latlng = latlng
    def __repr__(self):
         return "%s(venue_name=%r venue_id=%r url=%r booking_url=%r latlng=%r)" % (
             self.__class__.__name__, self.venue_name, self.venue_id, self.url, self.booking_url, self.latlng)

# every request is a for loop, it can be optimized
# if a parameter is missing there should be an error 
class Venue_Config:
    def __init__(self, path) -> None:
        self.path = path
        self.cfg_dict = self.load_config()

    def load_config(self):
        with open('config.yaml', 'r') as file:
            venue_config = yaml.safe_load(file)
        return venue_config
    
    def retrieve_params(self, *args):
        out = []
        for venue in self.cfg_dict.get("venue_list",[]):
            row = {}
            for arg in args:
                row[arg]=venue.get(arg, None)

            out.append(row)

        return out

    def get_by_id(self, key, *args):
        for venue in self.cfg_dict.get("venue_list",[]):
            if key == venue["venue_id"]:
                row = {}
                for arg in args:
                    row[arg]=venue.get(arg, None)

                return row

            
        return -1
    
    def ids(self):
        ids = set()
        venue_list = self.cfg_dict.get("venue_list",[])
        for venue in venue_list:
            ids.add(venue.get("venue_id"))
        if len(ids) != len(venue_list):
            raise Exception("Venue missing id in config")
        return ids



venues_cfg = Venue_Config("config.yaml")
venue_config = venues_cfg.cfg_dict
