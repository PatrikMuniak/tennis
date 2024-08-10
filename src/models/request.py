import sqlite3
import json
from const import DB_PATH, REQUEST, RESOURCES, DAYS, SESSIONS, BOOKING_URL
from config import venues_cfg
import datetime
import time

class Session:
    header_name = "sessionName"
    header_start_time = "start"
    header_end_time = "end"
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
    
    def to_list_portioned(self):
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
    
    def parse_dt_str_to_unix(self, datetime_string):
        tuple_dt = datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S").timetuple()
        unix_dt = time.mktime(tuple_dt)
        return unix_dt

    
    def load_from_dict(self, content_dict):
        self.date = self.parse_dt_str_to_unix(content_dict.get(DAYS.Date))
        for session in content_dict.get(DAYS.Sessions):
            s = Session()
            s.load_from_dict(session)
            self._sessions.append(s)

    def to_list(self):
        return [dict(date=self.date, **s.to_dict()) for s in self._sessions]

    def to_list_portioned(self):
        res = []
        for s in self._sessions:
            res+=[dict(date=self.date, **p) for p in s.to_list_portioned()]
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
            res+=[dict(court_name=self.name, **s) for s in d.to_list()]
        return res

class Request(object):
    def __init__(self):
        self._resources = []

    def load_json(self, json_content):

        content = json.loads(json_content)
        resources_list = content.get(REQUEST.Resources)
        for resource in resources_list:
            r = Resource()
            r.load_from_dict(resource)
            self._resources.append(r)
    
    def get_resources(self):
        res = []
        for r in self._resources:
            res+=r.to_list()
        return res
    


class SessionsProgram:
    def __init__(self, venue_id, request, venues_cfg):
        self.venue_id = venue_id
        # what if there is no such id?
        self.venue_name = venues_cfg.venue_list.get_by_id(venue_id, "venue_name")[0]
        self.sessions = self.initialize_sessions(request, venues_cfg)
    

    
    def split_by_session(self, s):
        res = []
        header_start_time = "start"
        header_end_time = "end"

        if s[header_end_time] - s[header_start_time] > 60:
            for i in range(((s[header_end_time] - s[header_start_time])//60)):
                temp_s = dict(s)
                start_sess = temp_s[header_start_time] +60*i
                end_sess = temp_s[header_start_time] +60*(i+1)
                temp_s[header_start_time] = start_sess
                temp_s[header_end_time] = end_sess
                assert end_sess<=temp_s[header_end_time]
                res.append(temp_s)
        else:
            res.append(s)
        
        return res


# "venue_name":venue_name,
# "date":date,
# "court_name":court_name,
# "name":name,
# "start":start_sess,
# "end":end_sess})
    

    def initialize_sessions(self, request, venues_cfg):
        res = []
        req_dict = request.get_resources()
        for session in req_dict:
            s = dict(session)
            s["venue_name"] = self.venue_name
            s[BOOKING_URL] = venues_cfg.venue_list.generate_booking_url(self.venue_id, s["date"])
            res += self.split_by_session(s)
        return res


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
        s = SessionsProgram(id, r, venues_cfg)
        venue_sessions = s.sessions
        print(venue_sessions[0])
        
    return venue_sessions

