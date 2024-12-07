from const import BOOKING_URL
from utils import get_time_from_int, generate_booking_url

class FreeSessions:
    def __init__(self, venue_id, request, venues_cfg):
        self.venue_id = venue_id
        # what if there is no such id?
        self.venue_name = venues_cfg.venue_list.get_by_id(venue_id, "venue_name")[0]
        self._sessions = self.initialize_sessions(request, venues_cfg)

    
    def get_sessions(self):
        return self._sessions
    
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
    
    def is_session_free(self, session):
        if session["sessionName"].isnumeric():
            return True
        else:
            return False

    def initialize_sessions(self, request, venues_cfg):
        res = []
        req_list = request.get_resources()
        for session in req_list:
            s = dict(session)
            s["venue_name"] = self.venue_name
            s["venue_id"] = self.venue_id
            s[BOOKING_URL] = generate_booking_url(self.venue_id, s["date"])
            if self.is_session_free(session):
                res += self.split_by_session(s)
        return res
