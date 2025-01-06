import unittest
from models.request import Request, Database
from models.free_sessions import FreeSessions
from config import venues_cfg
import json

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
        s = FreeSessions(req, venues_cfg)
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
        s = FreeSessions(req, venues_cfg)
        self.assertEqual(s.get_sessions(), expect)
    
    def test_get_inflated_last_request_empty(self):
        db = Database("../data/test.db")

if __name__ == '__main__':
    unittest.main()