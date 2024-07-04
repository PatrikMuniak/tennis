import sqlite3
import json
from const import DB_PATH
from config import venues_cfg
class DateTime(object): 
    dt = None

    
# venue id if you remove a venue id from the enum then it's not gonna be recognized
# venue id is an id so it has to be unique

class Json(object):
    content = ''


class Request(object):
    dt = None
    venue_id = None
    content = None

# def validate_id(id):
#     ve
    
def get_last_request(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''select * from requests where venue_id=? order by rowid desc limit 1;''', (id,) )
    query_out = cur.fetchone()
    venue_sessions = json.loads(query_out[2])
    return venue_sessions

