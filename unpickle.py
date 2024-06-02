import pickle

f = open("lyle202406001-10.pickle","rb")
venue_sessions_req = pickle.load(f)
ven_sess = venue_sessions_req.json()
redis = []
courts_location = "lyle"
for court in ven_sess.get("Resources"):
    court_name = court.get("Name")
    for day in court.get("Days"):
        date = day.get("Date")
        for session in day.get("Sessions"):
            # print(session)
            name = session.get("Name")
            start = session.get("StartTime")
            end = session.get("EndTime")
            if name == "6" or name=="10":
                if end-start>60:
                    # split
                    redis.append({"courts_location":courts_location,"date":date, "court_name":court_name, "start_time":start_time, "end_time":end_time, desc })
                print(date, court_name, name, start/60, end/60)
