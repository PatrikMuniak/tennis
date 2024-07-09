import sqlite3
import json
from const import DB_PATH, REQUEST, RESOURCES, DAYS, SESSIONS
from config import venues_cfg
from utils import generate_booking_url

class Session:
    header_name = "sessionName"
    header_start_time = "startTime"
    header_end_time = "endTime"
    def __init__(self) -> None:
        self.name = None
        self.start_time = None 
        self.end_time = None

    def load_from_dict(self,content_dict):
        self.name = content_dict.get(SESSIONS.Name)
        self.start_time = content_dict.get(SESSIONS.StartTime)
        self.end_time = content_dict.get(SESSIONS.EndTime)
    
    def to_dict(self):
        return {self.header_name:self.name, self.header_start_time:self.start_time, self.header_end_time:self.end_time }
    
    def to_inflated_list(self):
        res = []

        if self.end_time - self.start_time > 60:
            for i in range(((self.end_time - self.start_time)//60)):
                start_sess = self.start_time +60*i
                end_sess = self.start_time +60*(i+1)
                assert end_sess<=self.end_time
                res.append({
                    self.header_name:self.name,
                    self.header_start_time:start_sess,
                    self.header_end_time:end_sess})
        else:
            res.append({self.header_name:self.name,
                        self.header_start_time:self.start_time,
                        self.header_end_time:self.end_time})
        return res

class Day:
    def __init__(self) -> None:
        self.date = None
        self._sessions = []
        self.booking_url = generate_booking_url(self.venue_id, self.date)
    
    def load_from_dict(self, content_dict):
        self.date = content_dict.get(DAYS.Date)
        for session in content_dict.get(DAYS.Sessions):
            s = Session()
            s.load_from_dict(session)
            self._sessions.append(s)

    def to_list(self):
        return [dict(date=self.date, **s.to_dict()) for s in self._sessions]

    def to_inflated_list(self):
        res = []
        for s in self._sessions:
            res+=[dict(date=self.date, **p) for p in s.to_inflated_list()]
        return res



class Resource:
    def __init__(self) -> None:
        self._days = []
        self.name = None

    def load_from_dict(self, content_dict):
        self.name = content_dict.get(RESOURCES.Name)
        for day in content_dict.get(RESOURCES.Days):
            d = Day()
            d.load_from_dict(day)
            self._days.append(d)

    def to_list(self):
        res=[]
        for d in self._days:
            res+=[dict(name=self.name, **s) for s in d.to_list()]
        return res

    def to_inflated_list(self):
        res=[]
        for d in self._days:
            res+=[dict(name=self.name, **s) for s in d.to_inflated_list()]
        return res

class Request(object):
    def __init__(self):
        self._resources = []
        self.venue_id = None
        self.dt = None 

    def load_json(self, content):
        content = json.loads(content)
        resources_list = content.get(REQUEST.Resources)
        for resource in resources_list:
            r = Resource()
            r.load_from_dict(resource)
            self._resources.append(r)

    def load_json_file(self, json_file):

        with open(json_file, "r") as f:
            content = json.loads(f.read())
            resources_list = content.get(REQUEST.Resources)
            for resource in resources_list:
                r = Resource()
                r.load_from_dict(resource)
                self._resources.append(r)
    
    def get_resources(self):
        return [r.to_list() for r in self._resources]
    
    def get_resources_inflated(self):
        return [r.to_inflated_list() for r in self._resources]


# venue id if you remove a venue id from the enum then it's not gonna be recognized
# venue id is an id so it has to be unique

def get_inflated_last_request(id):
    venue_sessions = []
    if venues_cfg.venue_list.has_id(id):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('''select * from requests where venue_id=? order by rowid desc limit 1;''', (id,) )
        query_out = cur.fetchone()
        r = Request()
        r.load_json(query_out[2])
        venue_sessions = r.get_resources_inflated()
        print(venue_sessions)
    return venue_sessions

