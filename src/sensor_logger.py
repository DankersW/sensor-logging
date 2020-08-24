from dataclasses import dataclass
from datetime import datetime
from pytz import timezone
from json import dumps


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
    def generate_filename():
        date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return 'log_{}.txt'.format(date_time)

    @staticmethod
    def decode_binary_data(data, start_pos, end_pos, numerical):
        bin_slice = data[start_pos:end_pos]
        if numerical:
            return int.from_bytes(bin_slice, byteorder='big')
        else:
            return bin_slice.decode('UTF-8')

    @staticmethod
    def timestamp_to_iso8601(timestamp):
        timestamp /= 1000
        location = 'Europe/Stockholm'
        tz = timezone(location)
        return datetime.fromtimestamp(timestamp, tz).isoformat()

    @staticmethod
    def convert_kelvin_to_celcius(temp_kelvin):
        # Converting to two decimal precision
        temp_celsius = (int(((temp_kelvin / 1000) - 273.15) * 100) / 100)
        return temp_celsius

    def __init__(self):
        self.filename = self.generate_filename()
        self.setup_mqtt()

    def setup_mqtt(self):
        pass

    def log(self, bin_data):
        data_dict = self.decode_log_data(bin_data)
        log_msg = self.construct_log_message(data_dict)
        self.write_to_file(log_msg)

    def decode_log_data(self, bin_data):
        log_man_fields = self.decode_mandatory_fields(bin_data)
        log_opt_fields = self.decode_optional_fields(bin_data)
        return {**log_man_fields, **log_opt_fields}

    def decode_mandatory_fields(self, data):
        self.Sizes.name = self.decode_binary_data(data, start_pos=self.Offsets.nlen, numerical=True,
                                                  end_pos=self.Offsets.nlen + self.Sizes.nlen)
        timestamp = self.decode_binary_data(data, start_pos=self.Offsets.time, numerical=True,
                                            end_pos=self.Offsets.time + self.Sizes.time)
        name = self.decode_binary_data(data, start_pos=self.Offsets.name, numerical=False,
                                       end_pos=self.Offsets.name + self.Sizes.name)
        return {'timestamp': timestamp, 'name': name}

    def decode_optional_fields(self, data):
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

    def construct_log_message(self, data_dict):
        iso8601_time = self.timestamp_to_iso8601(data_dict.get('timestamp'))
        name = data_dict.get('name')
        log_msg = {'timestamp': iso8601_time, 'name': name}
        if 'temp' in data_dict.keys():
            temp = self.convert_kelvin_to_celcius(data_dict.get('temp'))
            log_msg.update({'temperature': temp})
        if 'humi' in data_dict.keys():
            humi = data_dict.get('humi') / 100
            log_msg.update({'humidity': humi})
        return dumps(log_msg)

    def write_to_file(self, log_msg):
        with open(self.filename, "a") as file:
            file.write(log_msg + '\n')
        file.close()


if __name__ == '__main__':
    sl = SensorLogger()
    d = b'\x00\x00\x01t\x1a\xa3\x07\xe8$6942b0b0-2ece-4ea2-89a2-2f837bfdec59\x04\x04\xd4\x01\xb5'
    sl.log(d)
