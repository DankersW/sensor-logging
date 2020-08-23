from dataclasses import dataclass


class SensorLogger:
    @dataclass
    class Sizes:
        name: int
        time: int = 8
        nlen: int = 1
        temp: int = 3
        humi: int = 2

    @dataclass
    class Offsets:
        mandatory_fields: int
        time: int = 0
        nlen: int = 8
        name: int = 9

    @staticmethod
    def decode_binary_data(data, start_pos, end_pos, numerical):
        bin_slice = data[start_pos:end_pos]
        if numerical:
            return int.from_bytes(bin_slice, byteorder='big')
        else:
            return bin_slice.decode('UTF-8')

    def __init__(self):
        self.setup_mqtt()

    def setup_mqtt(self):
        pass

    def decode_log_data(self, bin_data):
        log_man = self.get_mandatory_fields(bin_data)
        log_opt = self.get_optional_fields(bin_data)
        log = {**log_man, **log_opt}

        print('log: {}'.format(log))

    def get_mandatory_fields(self, data):
        self.Sizes.name = self.decode_binary_data(data, start_pos=self.Offsets.nlen, numerical=True,
                                                  end_pos=self.Offsets.nlen + self.Sizes.nlen)
        timestamp = self.decode_binary_data(data, start_pos=self.Offsets.time, numerical=True,
                                            end_pos=self.Offsets.time + self.Sizes.time)
        name = self.decode_binary_data(data, start_pos=self.Offsets.name, numerical=False,
                                       end_pos=self.Offsets.name + self.Sizes.name)
        return {'timestamp': timestamp, 'name': name}

    def get_optional_fields(self, data):
        self.Offsets.mandatory_fields = self.Offsets.name + self.Sizes.name
        size_optional_fields = len(data) - self.Offsets.mandatory_fields
        if size_optional_fields == self.Sizes.temp:
            return {'temp': self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                                    end_pos=self.Offsets.mandatory_fields + self.Sizes.temp)}
        elif size_optional_fields == self.Sizes.humi:
            return {'humi': self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                                    end_pos=self.Offsets.mandatory_fields + self.Sizes.humi)}
        elif size_optional_fields == self.Sizes.temp + self.Sizes.humi:
            temp = self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                           end_pos=self.Offsets.mandatory_fields + self.Sizes.temp)
            humi = self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields + self.Sizes.temp,
                                           end_pos=self.Offsets.mandatory_fields + self.Sizes.temp + self.Sizes.humi,
                                           numerical=True)
            return {'temp': temp, 'humi': humi}
        else:
            return {}


if __name__ == '__main__':
    sl = SensorLogger()
    d = b'\x00\x00\x01t\x1a\xa3\x07\xe8$6942b0b0-2ece-4ea2-89a2-2f837bfdec59\x04\x04\xd4\x01\xb5'
    sl.decode_log_data(d)
