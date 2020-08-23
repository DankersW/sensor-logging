class SensorLogger:
    def __init__(self):
        self.setup_mqtt()

    def setup_mqtt(self):
        pass

    def decode_binary_data(self, data):

        size_time = 8
        size_nlen = 1

        bin_timestamp = data[0:size_time]
        bin_nlen = data[size_time:size_time+size_nlen]
        timestamp = int.from_bytes(bin_timestamp, byteorder='big')
        size_name = int.from_bytes(bin_nlen, byteorder='big')
        print('{} = {} | {} {}'.format(bin_timestamp, timestamp, bin_nlen, size_name))


if __name__ == '__main__':
    sl = SensorLogger()
    d = b'\x00\x00\x01t\x1a\xa3\x07\xe8$6942b0b0-2ece-4ea2-89a2-2f837bfdec59\x04\x04\xd4\x01\xb5'
    sl.decode_binary_data(d)
