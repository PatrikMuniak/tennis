import sqlite3

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
#  the order should be decided by the requests class
    def load_from_db(self, query_output):
        self.dt = query_output[0]
        self.venue_id = query_output[1]
        self.content = query_output[2]


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
    
    # here I can use a decorator that initialized the cursor and after the query is complete closes the connection

    def update(self, query, args=set()):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        con.commit()
        con.close()

    def fetchone(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        result = cur.fetchone()
        con.close()
        return result
    
    def fetchall(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        result = cur.fetchall()
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
    
    def insert(self, request):
        self.database.update('''INSERT INTO requests (venue_id, content, dt) VALUES (?, ?, ?)''', (request.venue_id, request.content, request.dt) )

    def get_all_by_venue_id(self, venue_id):
        query_out = self.database.fetchall('''SELECT * FROM requests WHERE venue_id=?;''', (venue_id,) )
        return query_out
    
    def get_venue_ids(self):
        return self.database.fetchall("SELECT UNIQUE(venue_id) FROM requests;")
    
    def has_venue_id(self, id):
        return id in self.get_venue_ids()     
