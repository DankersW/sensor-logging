from src.decoder import Decoder

import unittest


class TestDecoder(unittest.TestCase):
    bin_data = [b'\x00\x00\x01t\x1dD\xb9\xdc\x04test\x01\x9f\xb2\x01\xb5',
                b'\x00\x00\x01t\x1dE\x0f\xf6\x04test\x01%',
                b'\x00\x00\x01t\x1dE9\x1b\x04test\x07\xff\xe1',
                b'\x00\x00\x01t\x1dE\xecy\ta125r2g2e\x00\xc7u\x01\x1e',
                b'\x00\x00\x01t\x1dF\x10\xad\ta125r2g2e\x02a',
                b'\x00\x00\x01t\x1dF@r\ta125r2g2e\x02\xf5\x94\x03j',
                b'\x00\x00\x01t\x1dN\x7f\xeb\x07445t-e1']

    def test_decoding_mandatory_fields(self):
        decoder = Decoder()
        truth_list = [{'timestamp': 1598218877404, 'name': 'test'},
                      {'timestamp': 1598218899446, 'name': 'test'},
                      {'timestamp': 1598218909979, 'name': 'test'},
                      {'timestamp': 1598218955897, 'name': 'a125r2g2e'},
                      {'timestamp': 1598218965165, 'name': 'a125r2g2e'},
                      {'timestamp': 1598218977394, 'name': 'a125r2g2e'},
                      {'timestamp': 1598219517931, 'name': '445t-e1'}]
        for data, truth in zip(self.bin_data, truth_list):
            result = decoder.decode_mandatory_fields(data)
            self.assertEqual(result, truth)

    def test_decoding_optional_fields(self):
        decoder = Decoder()
        name_sizes = [4, 4, 4, 9, 9, 9, 7]
        truth_list = [{'temp': 106418, 'humi': 437}, {'humi': 293}, {'temp': 524257}, {'temp': 51061, 'humi': 286},
                      {'humi': 609}, {'temp': 193940, 'humi': 874}, {}]
        for data, truth, name_size in zip(self.bin_data, truth_list, name_sizes):
            decoder.Sizes.name = name_size
            result = decoder.decode_optional_fields(data)
            self.assertEqual(result, truth)