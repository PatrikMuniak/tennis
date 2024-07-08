import json
from stuff import REQUEST, RESOURCES, DAYS, SESSIONS

class Session:
    def __init__(self) -> None:
        self.name = None
        self.start_time = None 
        self.end_time = None

    def load_from_dict(self,content_dict):
        self.name = content_dict.get(SESSIONS.Name)
        self.start_time = content_dict.get(SESSIONS.StartTime)
        self.end_time = content_dict.get(SESSIONS.EndTime)
    
    def to_dict(self):
        return {"sessionName":self.name, "startTime":self.start_time, "endTime":self.end_time }

class Day:
    def __init__(self) -> None:
        self.date = None
        self._sessions = []
    
    def load_from_dict(self, content_dict):
        self.date = content_dict.get(DAYS.Date)
        for session in content_dict.get(DAYS.Sessions):
            s = Session()
            s.load_from_dict(session)
            self._sessions.append(s)

    def to_list(self):
        return [dict(date=self.date, **s.to_dict()) for s in self._sessions]



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

    def to_dict(self):
        res=[]
        for d in self._days:
            res+=[dict(name=self.name, **s) for s in d.to_list()]
        return res

class Request(object):
    def __init__(self):
        self._resources = []

    def load_json(self, json_file):

        with open(json_file, "r") as f:
            content = json.loads(f.read())
            resources_list = content.get(REQUEST.Resources)
            for resource in resources_list:
                r = Resource()
                r.load_from_dict(resource)
                self._resources.append(r)
    
    def get_resources(self):
        return [r.to_dict() for r in self._resources]
    
    def process_sessions(self):
        





r = Request()
r.load_json("test.json")
print(r.get_resources())