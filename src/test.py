import yaml
from const import VENUE_LIST, CONFIG_PATH

# venue_name: Lyle Park Tennis Courts
# venue_id: lyle
# url: https://lyle.newhamparkstennis.org.uk/v0/VenueBooking/lyle_newhamparkstennis_org_uk/GetVenueSessions?resourceID=&startDate={start_date}&endDate={end_date}&_={ts}
# booking_url: https://lyle.newhamparkstennis.org.uk/Booking/BookByDate#?date={date}&role=guest
# latlng: [51.50191898205893, 0.024873357726036438]


class VenueEntry(object):
    def __init__(self, venue_name, venue_id, url, booking_url, latlng):
        self.venue_name = venue_name
        self.venue_id = venue_id
        self.url = url
        self.booking_url = booking_url
        self.latlng = latlng
    
    def __repr__(self):
        return "VenueEntry(venue_name={} venue_id={} url={} booking_url={} latlng={})".format(self.venue_name, self.venue_id, self.url, self.booking_url, self.latlng)
    
class VenueList(object):
    def __init__(self):
        self._venue_list = []

    def add_entry(self, *args, **kvargs):
        entry = VenueEntry(*args, **kvargs)
        self._venue_list.append(entry)

    
    def list_entries(self):
        for entry in self._venue_list:
            print(entry)

    def __len__(self):
        return len(self._venue_list)


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




cfg = VenueConfig()
cfg.set_cfg_path(CONFIG_PATH)
cfg.load_venue_list()
print(len(cfg.venue_list))
print(cfg.cfg_path)
cfg.venue_list.list_entries()
