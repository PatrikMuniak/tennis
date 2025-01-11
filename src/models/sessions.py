from const import BOOKING_URL
from const import DB_PATH, REQUEST, RESOURCES, DAYS, SESSIONS, BOOKING_URL
import json
import utils
from .request import Request, Database, Requests
from config import venues_cfg

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
        self._sessions = self.generate_sessions(request)
        
    
    def get_sessions(self):
        return self._sessions


    def _get_day_sessions(self, day_data):
        day_sessions = []
        for session in day_data.get(DAYS.Sessions):
            s = {
                    "sessionName":session.get(SESSIONS.Name), 
                    "start":session.get(SESSIONS.StartTime), 
                    "end":session.get(SESSIONS.EndTime),
                    "date":utils.parse_dt_str_to_unix(day_data.get(DAYS.Date))
                }
            day_sessions.extend(self._split_session_by_hour(s))
        return day_sessions

    def _get_resource_sessions(self, resource_data):
        name = resource_data.get(RESOURCES.Name)
        resource_sessions = []

        for day in resource_data.get(RESOURCES.Days):
            day_sess = self._get_day_sessions(day)
            for  session in day_sess:
                session["court_name"] = name
                resource_sessions.append(session)
        return resource_sessions

    def _convert_json_to_sessions(self, json_content):
        sessions = []
        content = json.loads(json_content)
        resources_list = content.get(REQUEST.Resources)
        for resource in resources_list:
            
            resource_sessions = self._get_resource_sessions(resource)

            for s in resource_sessions:
                s["venue_id"] = self.venue_id
                sessions.append(s)
        return sessions
    
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

    def generate_sessions(self, request: Request):
        res = []
        req_list = self._convert_json_to_sessions(request.content)
        for session in req_list:
            s = dict(session)
            s["venue_name"] = self.venue_name
            s[BOOKING_URL] = utils.generate_booking_url(self.venue_id, s["date"])
            if self.is_session_free(session):
                res += self._split_session_by_hour(s)
        return res


def get_inflated_last_request(id):
    if venues_cfg.venue_list.has_id(id):
        db = Database(DB_PATH)
        requests = Requests(db)
        request = requests.query_db_last_record(id)
        s = Sessions(request, venues_cfg)
        return s.get_sessions()
    else:
        return list()
        


