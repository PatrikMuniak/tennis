import datetime
import time


class DateTs:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, unix_ts):
        self._value = datetime.datetime.fromtimestamp(unix_ts, datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')

    def now(self):
        self.value(time.time())
    
    @staticmethod
    def convert_dt_str_to_unix(datetime_string):
        tuple_dt = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S").timetuple()
        unix_dt = time.mktime(tuple_dt)
        return unix_dt
    
#the session part should go to another class 
class Request(object):
    """
    Request is the row of the table requests
    it's made of:
        - dt
        - venue_id
        - content
    """
    def __init__(self, dt=None, venue_id=None, content=""):
        self.dt = dt
        self.venue_id = venue_id
        self.content = content
   

class Requests:
    def __init__(self, database):
        self.database = database

    def remove_records_older_than_a_week(self):
        self.database.update('''DELETE FROM requests WHERE date(dt) < date('now','-7 days');''')
    
    def query_db_last_record(self, id):

        query_out = self.database.fetchone('''SELECT dt, venue_id, content FROM requests WHERE venue_id=? ORDER BY rowid desc LIMIT 1;''', (id,) )
        dt = DateTs()
        dt.value = DateTs.convert_dt_str_to_unix(query_out[0])
        request = Request(dt=dt, content=query_out[2], venue_id=query_out[1])
        return request
    
    def insert(self, request: Request):
        self.database.update('''INSERT INTO requests (venue_id, content, dt) VALUES (?, ?, ?)''', (request.venue_id, request.content, request.dt.value) )

    def get_all_by_venue_id(self, venue_id):
        query_out = self.database.fetchall('''SELECT * FROM requests WHERE venue_id=?;''', (venue_id,) )
        return query_out
    
    def get_venue_ids(self):
        return self.database.fetchall("SELECT UNIQUE(venue_id) FROM requests;")
    
    def has_venue_id(self, id):
        return id in self.get_venue_ids()     
