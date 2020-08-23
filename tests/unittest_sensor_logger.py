import unittest

from src.sensor_logger import SensorLogger


class TestIdFromTopic(unittest.TestCase):
    def test_decoding(self):
        logger = SensorLogger()
        bin_data = [b'\x00\x00\x01t\x17\x18\x8d\xc4$b7c94abd-a591-45de-9d62-d4a69c973e1f\x022x\x02\xfe',
                    b'\x00\x00\x01t\x17\x18^\xd4$b7c94abd-a591-45de-9d62-d4a69c973e1f\t&\xc8\x03\x99',
                    b'\x00\x00\x01t\x17\x18L\xd2$b7c94abd-a591-45de-9d62-d4a69c973e1f',
                    b'\x00\x00\x01t\x17\x18\x1a\x08$b7c94abd-a591-45de-9d62-d4a69c973e1f\x04g$',
                    b'\x00\x00\x01t\x17\x18)\xfa$b7c94abd-a591-45de-9d62-d4a69c973e1f\x03]\x88\x01\xcd']
        for data in bin_data:
            logger.decode_binary_data(data)
