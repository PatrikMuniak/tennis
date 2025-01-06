import sqlite3
import json
from const import DB_PATH, REQUEST, RESOURCES, DAYS, SESSIONS, BOOKING_URL
from config import venues_cfg
import datetime
import time
from .free_sessions import FreeSessions
from utils import parse_dt_str_to_unix

#the session part should go to another class 
class Request(object):
    def __init__(self):
        self.dt = None
        self.venue_id = None
        self.__sessions = []
    

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

                self.__sessions.append(s)
        
    
    def save(self, venue_id, content):
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''INSERT INTO requests (venue_id, content, dt) VALUES (?, ?, ?)''', (venue_id, content, dt) )
        con.commit()
        con.close()
    
    def load_from_db(self, query_output):
        self.dt = query_output[0]
        self.venue_id = query_output[1]
        content = query_output[2]

        self.load_json(content, self.venue_id)
        
    
    def get_sessions(self):
        return self.__sessions
    
class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def update(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        con.commit()
        con.close()

    def fetchone(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        result = cur.fetchone()
        con.close()
        return result


class Requests:
    def __init__(self, database):
        self.database = database

    def remove_records_older_than_a_week(self):
        self.database.update('''DELETE FROM requests WHERE date(dt) < date('now','-7 days');''')
    
    def query_db_last_record(self, id):

        query_out = self.database.fetchone('''SELECT * FROM requests WHERE venue_id=? ORDER BY rowid desc LIMIT 1;''', (id,) )
        request = Request()
        request.load_from_db(query_out)
        return request
        

def get_inflated_last_request(id):
    if venues_cfg.venue_list.has_id(id):
        db = Database(DB_PATH)
        requests = Requests(db)
        request = requests.query_db_last_record(id)
        s = FreeSessions(request, venues_cfg)
        return s.get_sessions()
    else:
        return list()
        
