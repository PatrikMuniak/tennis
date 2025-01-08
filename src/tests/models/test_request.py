import unittest
from models.request import Request, Database, Requests
from models.sessions import Sessions
from config import venues_cfg
import json
from datetime import datetime, timedelta
from utils import serialize_datetime
import os

class TestRequest(unittest.TestCase):

    def test_get_inflated_last_request_with_results(self):
        json_str = {
            "Resources": [
                {
                    "Name": "Court 1",
                    "Days": [
                        {
                            "Date": "2024-12-07T00:00:00",
                            "Sessions": [
                                    {
                                    "Name": "12",
                                    "StartTime": 15*60,
                                    "EndTime": 17*60,
                                    }
                            ]
                                
                        }
                    ]
                }
            ]
        }

        expect = [{'court_name': 'Court 1', 'date': 1733529600.0, 'sessionName': '12', 'start': 900, 'end': 960, 'venue_name': 'Canning Town Recreation Ground Tennis Courts', 'venue_id': 'canning', 'booking_url': 'https://canning.newhamparkstennis.org.uk/Booking/BookByDate#?date=2024-12-07&role=guest'}, {'court_name': 'Court 1', 'date': 1733529600.0, 'sessionName': '12', 'start': 960, 'end': 1020, 'venue_name': 'Canning Town Recreation Ground Tennis Courts', 'venue_id': 'canning', 'booking_url': 'https://canning.newhamparkstennis.org.uk/Booking/BookByDate#?date=2024-12-07&role=guest'}]

        
        req = Request()
        req.load_json(json.dumps(json_str),"canning")
        s = Sessions(req, venues_cfg)
        self.assertEqual(s.get_sessions(), expect)



    def test_get_inflated_last_request_empty(self):
        json_str = {
            "Resources": [
                {
                    "Name": "Court 1",
                    "Days": [
                        {
                            "Date": "2024-12-07T00:00:00",
                            "Sessions": [
                                    {
                                    "Name": "Booking",
                                    "StartTime": 15*60,
                                    "EndTime": 17*60,
                                    }
                            ]
                                
                        }
                    ]
                }
            ]
        }

        expect = []
        
        req = Request()
        req.load_json(json.dumps(json_str),"canning")
        req.venue_id="canning"
        s = Sessions(req, venues_cfg)
        self.assertEqual(s.get_sessions(), expect)
    
    def test_get_inflated_last_request_empty(self):
        db_file = "../data/test.db"
        if os.path.isfile(db_file):
            os.remove(db_file)
            print("Setting up the Removing test db file.")
        db = Database(db_file)
        db.update("""CREATE TABLE requests (
                    dt DATETIME DEFAULT CURRENT_TIMESTAMP,
                    venue_id VARCHAR(40),
                    content TEXT
                );
                """)
        requests = Requests(db)
        req_old = Request(dt=serialize_datetime(datetime.today() - timedelta(days= 8)), venue_id="test", content="")
        req_new = Request(dt=serialize_datetime(datetime.today()), venue_id="test", content="")
        requests.insert(req_old)
        requests.insert(req_new)
        self.assertEqual(len(requests.get_all_by_venue_id("test")), 2)
        requests.remove_records_older_than_a_week()
        self.assertEqual(len(requests.get_all_by_venue_id("test")), 1)
        if os.path.isfile(db_file):
            os.remove(db_file)



        

if __name__ == '__main__':
    unittest.main()