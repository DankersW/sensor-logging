from src.mqtt_config import MqttConfig
from src.decoder import Decoder

import subprocess
import paho.mqtt.client as mqtt


class SensorReader:
    def __init__(self, simulator_command):
        self.decoder = Decoder()
        self.running = False
        self.mqtt_client = self.setup_mqtt()
        self.process = subprocess.Popen(simulator_command, shell=False, stdout=subprocess.PIPE)
        self.read_sensor()

    def __del__(self):
        self.mqtt_client.disconnect()

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
            print('{} - {} | {} | {}'.format(bin_plength, bin_package, package_length, log_msg))
            self.mqtt_client.publish(topic=MqttConfig.telemetry_topic, payload=log_msg, qos=0)

    def read_binary_data(self, read_size):
        while True:
            binary_data = self.process.stdout.read(read_size)
            if binary_data:
                return binary_data


if __name__ == '__main__':
    cmd = './sensor_data_simulator.x86_64-unknown-linux-gnu'
    arg = '--name=445t-e1'
    command = [cmd]#, arg]

    sensor_reader = SensorReader(command)