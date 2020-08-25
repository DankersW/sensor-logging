from src.mqtt_config import MqttConfig
from src.formatter import Formatter

from datetime import datetime
import paho.mqtt.client as mqtt


class SensorLogger:

    @staticmethod
    def generate_filename():
        date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return 'log_{}.txt'.format(date_time)

    def __init__(self):
        self.formatter = Formatter()
        self.filename = self.generate_filename()
        self.mqtt_client = self.setup_mqtt()
        self.mqtt_client.loop_forever()

    def __del__(self):
        pass

    def log(self, data):
        log_msg = self.formatter.construct_log_message(data)
        self.write_to_file(log_msg)

    def setup_mqtt(self):
        client = mqtt.Client()
        client.connect(MqttConfig.broker_address, MqttConfig.port, MqttConfig.stay_alive)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.subscribe(MqttConfig.telemetry_topic)
        return client

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(MqttConfig.telemetry_topic)

    def on_message(client, userdata, msg):
        time = datetime.datetime.now()
        payload = msg.payload.decode('utf-8')
        print("{} | Received message: \"{}\" on Topic: \"{}\"".format(time, payload, msg.topic))

    def write_to_file(self, log_msg):
        with open(self.filename, "a") as file:
            file.write(log_msg + '\n')
        file.close()


if __name__ == '__main__':
    sl = SensorLogger()
    d = b'\x00\x00\x01t\x1a\xa3\x07\xe8$6942b0b0-2ece-4ea2-89a2-2f837bfdec59\x04\x04\xd4\x01\xb5'
    sl.log(d)
