import unittest

from src.formatter import Formatter
from json import loads


class TestSensorLogger(unittest.TestCase):
    def test_construct_log_message(self):
        formatter = Formatter()
        data_dicts = [{'timestamp': 1598218877404, 'name': 'test', 'temp': 106418, 'humi': 437},
                      {'timestamp': 1598218899446, 'name': 'test', 'humi': 293},
                      {'timestamp': 1598218909979, 'name': 'test', 'temp': 524257},
                      {'timestamp': 1598218955897, 'name': 'a125r2g2e', 'temp': 51061, 'humi': 286},
                      {'timestamp': 1598218965165, 'name': 'a125r2g2e', 'humi': 609},
                      {'timestamp': 1598218977394, 'name': 'a125r2g2e', 'temp': 193940, 'humi': 874},
                      {'timestamp': 1598219517931, 'name': '445t-e1'}]
        truth_list = [{"timestamp": "2020-08-23T23:41:17.404000+02:00", "name": "test", "temperature": -166.73, "humidity": 4.37},
                      {"timestamp": "2020-08-23T23:41:39.446000+02:00", "name": "test", "humidity": 2.93},
                      {"timestamp": "2020-08-23T23:41:49.979000+02:00", "name": "test", "temperature": 251.1},
                      {"timestamp": "2020-08-23T23:42:35.897000+02:00", "name": "a125r2g2e",
                       "temperature": -222.08, "humidity": 2.86},
                      {"timestamp": "2020-08-23T23:42:45.165000+02:00", "name": "a125r2g2e", "humidity": 6.09},
                      {"timestamp": "2020-08-23T23:42:57.394000+02:00", "name": "a125r2g2e",
                       "temperature": -79.2, "humidity": 8.74},
                      {"timestamp": "2020-08-23T23:51:57.931000+02:00", "name": "445t-e1"}]
        for data_dict, truth in zip(data_dicts, truth_list):
            result_jsonstr = formatter.construct_log_message(data_dict)
            result = loads(result_jsonstr)
            self.assertEqual(result.get('name'), truth.get('name'))
            self.assertEqual(result.get('timestamp'), truth.get('timestamp'))
            self.assertEqual(result.get('temperature'), truth.get('temperature'))
            self.assertEqual(result.get('humidity'), truth.get('humidity'))
