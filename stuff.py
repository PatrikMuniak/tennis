import json
from collections import namedtuple

request_fields = ("Resources",)
Request = namedtuple("Request", request_fields)

REQUEST = Request(*request_fields)

resources_fileds = ("Name", "Days")
Resources = namedtuple("Resources", resources_fileds)
RESOURCES = Resources(*resources_fileds)

# print(Request.Resources)

# Days
days_fileds = ("Date", "Sessions")
Days = namedtuple("Days", days_fileds)
DAYS = Days(*days_fileds)

# Sessions
sessions_fileds = ("Name", "StartTime", "EndTime")
Sessions = namedtuple("Sessions", sessions_fileds)
SESSIONS = Sessions(*sessions_fileds)




# with open("test.json", "r") as f:
#     content = json.loads(f.read())

# print(Request.Resources)
# print(content.get(Request.Resources))


