from pytz import timezone
from json import dumps
from datetime import datetime


class Formatter:
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
