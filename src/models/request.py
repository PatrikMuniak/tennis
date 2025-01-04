import sqlite3
import json
from const import DB_PATH, REQUEST, RESOURCES, DAYS, SESSIONS, BOOKING_URL
from config import venues_cfg
import datetime
import time
from .free_sessions import FreeSessions
from utils import parse_dt_str_to_unix

# class Day:
#     def __init__(self) -> None:
#         self._sessions = []

    
#     def load_from_dict(self, day):
#         for session in day.get(DAYS.Sessions):
#             self._sessions.append({"sessionName":session.get(SESSIONS.Name), 
#                                    "start":session.get(SESSIONS.StartTime), 
#                                    "end":session.get(SESSIONS.EndTime),
#                                    "date":parse_dt_str_to_unix(day.get(DAYS.Date))
#                                    })

#     def to_list(self):
#         return self._sessions

class Resource:
    def __init__(self) -> None:
        self._sessions = []
        self.name = None

    def get_day_sessions(self, day_data):
        day_sessions = []
        for session in day_data.get(DAYS.Sessions):
            day_sessions.append({"sessionName":session.get(SESSIONS.Name), 
                                   "start":session.get(SESSIONS.StartTime), 
                                   "end":session.get(SESSIONS.EndTime),
                                   "date":parse_dt_str_to_unix(day_data.get(DAYS.Date))
                                   })
        return day_sessions

    def load_from_dict(self, resource_data):
        name = resource_data.get(RESOURCES.Name)
        for day in resource_data.get(RESOURCES.Days):
            day_sess = self.get_day_sessions(day)
            for  session in day_sess:
                session["court_name"] = name
                self._sessions.append(session)

    def to_list(self):
        return self._sessions



class Request(object):
    def __init__(self):
        self.dt = None
        self.venue_id = None
        self._sessions = []

    def get_day_sessions(self, day_data):
        day_sessions = []
        for session in day_data.get(DAYS.Sessions):
            day_sessions.append({"sessionName":session.get(SESSIONS.Name), 
                                   "start":session.get(SESSIONS.StartTime), 
                                   "end":session.get(SESSIONS.EndTime),
                                   "date":parse_dt_str_to_unix(day_data.get(DAYS.Date))
                                   })
        return day_sessions

    def get_resource_sessions(self, resource_data):
        name = resource_data.get(RESOURCES.Name)
        resource_sessions = []

        for day in resource_data.get(RESOURCES.Days):
            day_sess = self.get_day_sessions(day)
            for  session in day_sess:
                session["court_name"] = name
                resource_sessions.append(session)
        return resource_sessions

    def load_json(self, json_content, venue_id):
        self.venue_id = venue_id

        content = json.loads(json_content)
        resources_list = content.get(REQUEST.Resources)
        for resource in resources_list:
            
            resource_sessions = self.get_resource_sessions(resource)

            for s in resource_sessions:
                s["venue_id"] = venue_id

                self._sessions.append(s)
        
    
    def save(self, venue_id, content):
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue_id, content, dt) VALUES (?, ?, ?)''', (venue_id, content, dt) )
        con.commit()
    
    def query_db_last_record(self, id):

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        cur.execute('''select * from requests where venue_id=? order by rowid desc limit 1;''', (id,) )
        query_out = cur.fetchone()

        self.dt = query_out[0]
        self.venue_id = query_out[1]
        content = query_out[2]

        self.load_json(content, self.venue_id)
        
    
    def get_sessions(self):
        return self._sessions
    

def get_inflated_last_request(id):
    if venues_cfg.venue_list.has_id(id):
        req = Request()
        req.query_db_last_record(id)
        s = FreeSessions(req, venues_cfg)
        return s.get_sessions()
    else:
        return list()
        
