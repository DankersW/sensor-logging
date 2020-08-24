import unittest

from src.sensor_logger import SensorLogger
from json import loads


class TestIdFromTopic(unittest.TestCase):
    bin_data = [b'\x00\x00\x01t\x1dD\xb9\xdc\x04test\x01\x9f\xb2\x01\xb5',
                b'\x00\x00\x01t\x1dE\x0f\xf6\x04test\x01%',
                b'\x00\x00\x01t\x1dE9\x1b\x04test\x07\xff\xe1',
                b'\x00\x00\x01t\x1dE\xecy\ta125r2g2e\x00\xc7u\x01\x1e',
                b'\x00\x00\x01t\x1dF\x10\xad\ta125r2g2e\x02a',
                b'\x00\x00\x01t\x1dF@r\ta125r2g2e\x02\xf5\x94\x03j',
                b'\x00\x00\x01t\x1dN\x7f\xeb\x07445t-e1']

    def test_decoding_mandatory_fields(self):
        logger = SensorLogger()
        truth_list = [{'timestamp': 1598218877404, 'name': 'test'},
                      {'timestamp': 1598218899446, 'name': 'test'},
                      {'timestamp': 1598218909979, 'name': 'test'},
                      {'timestamp': 1598218955897, 'name': 'a125r2g2e'},
                      {'timestamp': 1598218965165, 'name': 'a125r2g2e'},
                      {'timestamp': 1598218977394, 'name': 'a125r2g2e'},
                      {'timestamp': 1598219517931, 'name': '445t-e1'}]
        for data, truth in zip(self.bin_data, truth_list):
            result = logger.decode_mandatory_fields(data)
            self.assertEqual(result, truth)

    def test_decoding_optional_fields(self):
        logger = SensorLogger()
        name_sizes = [4, 4, 4, 9, 9, 9, 7]
        truth_list = [{'temp': 106418, 'humi': 437}, {'humi': 293}, {'temp': 524257}, {'temp': 51061, 'humi': 286},
                      {'humi': 609}, {'temp': 193940, 'humi': 874}, {}]
        for data, truth, name_size in zip(self.bin_data, truth_list, name_sizes):
            logger.Sizes.name = name_size
            result = logger.decode_optional_fields(data)
            self.assertEqual(result, truth)

    def test_construct_log_message(self):
        logger = SensorLogger()
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
            result_jsonstr = logger.construct_log_message(data_dict)
            result = loads(result_jsonstr)
            self.assertEqual(result.get('name'), truth.get('name'))
            self.assertEqual(result.get('timestamp'), truth.get('timestamp'))
            self.assertEqual(result.get('temperature'), truth.get('temperature'))
            self.assertEqual(result.get('humidity'), truth.get('humidity'))
