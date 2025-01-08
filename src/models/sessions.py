from const import BOOKING_URL
from utils import generate_booking_url
#  Added this item but I need to continue
# class Session:
#     def __init__(self, venue_id, date, court_name, sessionName, start, end):
#         self.sessionName = sessionName
#         self.start = start
#         self.end = end
#         self.date = date
#         self.court_name = court_name
#         self.venue_id = venue_id

class Sessions:
    def __init__(self, request, venues_cfg):
        self.venue_id = request.venue_id
        # what if there is no such id?
        self.venue_name = venues_cfg.get_venue_name(self.venue_id)
        self._sessions = self.initialize_sessions(request)

    
    def get_sessions(self):
        return self._sessions
    
    def _split_session_by_hour(self, session):
        res = []
        header_start_time = "start"
        header_end_time = "end"

        if session[header_end_time] - session[header_start_time] > 60:
            for i in range(((session[header_end_time] - session[header_start_time])//60)):
                temp_s = dict(session)
                start_sess = temp_s[header_start_time] +60*i
                end_sess = temp_s[header_start_time] +60*(i+1)
                temp_s[header_start_time] = start_sess
                temp_s[header_end_time] = end_sess
                assert end_sess<=temp_s[header_end_time]
                res.append(temp_s)
        else:
            res.append(session)
        
        return res
    
    def is_session_free(self, session):
        if session["sessionName"].isnumeric():
            return True
        else:
            return False

    def initialize_sessions(self, request):
        res = []
        req_list = request.get_sessions()
        for session in req_list:
            s = dict(session)
            s["venue_name"] = self.venue_name
            s[BOOKING_URL] = generate_booking_url(self.venue_id, s["date"])
            if self.is_session_free(session):
                res += self._split_session_by_hour(s)
        return res


    def get_inflated_last_request(self, id):
        if venues_cfg.venue_list.has_id(id):
            db = Database(DB_PATH)
            requests = Requests(db)
            request = requests.query_db_last_record(id)
            s = Sessions(request, venues_cfg)
            return s.get_sessions()
        else:
            return list()
        


