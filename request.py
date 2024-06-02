import requests
import pickle
venue_sessions = requests.get('https://stratford.newhamparkstennis.org.uk/v0/VenueBooking/lyle_newhamparkstennis_org_uk/GetVenueSessions?resourceID=&startDate=2024-06-10&endDate=2024-06-10&roleId=&_=1717152154207')
print(venue_sessions.json())

f = open("stratford202406001-10.pickle", "wb")
pickle.dump(venue_sessions, f)
