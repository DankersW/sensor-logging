from src.mqtt_config import MqttConfig
from src.formatter import Formatter

from datetime import datetime
from threading import Thread
import paho.mqtt.client as mqtt


class SensorLogger(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.formatter = Formatter()
        self.filename = self.generate_filename()

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(MqttConfig.broker_address, MqttConfig.port, MqttConfig.stay_alive)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def __del__(self):
        self.mqtt_client.disconnect()

    def run(self):
        self.mqtt_client.loop_forever()

    @staticmethod
    def generate_filename():
        date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return 'log_{}.txt'.format(date_time)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.mqtt_client.subscribe(MqttConfig.telemetry_topic)

    def on_message(self, client, userdata, msg):
        time = datetime.now()
        payload = msg.payload.decode('utf-8')
        print("{} | Received message: \"{}\" on Topic: \"{}\"".format(time, payload, msg.topic))
        self.log(payload)

    def log(self, data):
        data_dict = eval(data)
        log_msg = self.formatter.construct_log_message(data_dict)
        self.write_to_file(log_msg)

    def write_to_file(self, log_msg):
        with open(self.filename, "a") as file:
            file.write(log_msg + '\n')


if __name__ == '__main__':
    sl = SensorLogger()
    sl.start()
