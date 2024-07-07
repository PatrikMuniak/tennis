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

class Day:
    def __init__(self) -> None:
        self.date = None
        self.sessions = []
    
    def load_from_dict(self, content_dict):
        self.date = content_dict.get(DAYS.Date)
        for session in content_dict.get(DAYS.Sessions):
            s = Session()
            s.load_from_dict(session)
            self.sessions.append(s)



class Resource:
    def __init__(self) -> None:
        self.days = []
        self.name = None

    def load_from_dict(self, content_dict):
        self.name = content_dict.get(RESOURCES.Name)
        for day in content_dict.get(RESOURCES.Days):
            d = Day()
            d.load_from_dict(day)
            self.days.append(d)

class Request(object):
    def __init__(self):
        self.resources = []

    def load_json(self, json_file):

        with open(json_file, "r") as f:
            content = json.loads(f.read())
            resources_list = content.get(REQUEST.Resources)
            for resource in resources_list:
                r = Resource()
                r.load_from_dict(resource)
                self.resources.append(r)





r = Request()
r.load_json("test.json")
print(r.resources)