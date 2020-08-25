from src.mqtt_config import MqttConfig
from src.decoder import Decoder

from threading import Thread
import subprocess
import paho.mqtt.client as mqtt


class SensorReader(Thread):
    def __init__(self, simulator_command):
        Thread.__init__(self)
        self.decoder = Decoder()
        self.running = False
        self.mqtt_client = self.setup_mqtt()
        self.process = subprocess.Popen(simulator_command, shell=False, stdout=subprocess.PIPE)

    def __del__(self):
        self.mqtt_client.disconnect()

    def run(self):
        self.read_sensor()

    def setup_mqtt(self):
        client = mqtt.Client()
        client.connect(MqttConfig.broker_address, MqttConfig.port, MqttConfig.stay_alive)
        self.running = True
        return client

    def read_sensor(self):
        while self.running:
            bin_plength = self.read_binary_data(self.decoder.Sizes.plen)
            package_length = int.from_bytes(bin_plength, byteorder='big')
            bin_package = self.read_binary_data(package_length - self.decoder.Sizes.plen)
            log_msg = self.decoder.decode_log_data(bin_package)
            self.mqtt_client.publish(topic=MqttConfig.telemetry_topic, payload=log_msg, qos=0)

    def read_binary_data(self, read_size):
        while True:
            binary_data = self.process.stdout.read(read_size)
            if binary_data:
                return binary_data
