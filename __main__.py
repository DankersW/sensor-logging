from src.sensor_reader import SensorReader
from src.sensor_logger import SensorLogger

from time import sleep
from subprocess import Popen


def start_mqtt_broker_locally():
    start_broker_command = ['mosquitto', '-v']
    Popen(start_broker_command)
    sleep(2)


start_mqtt_broker_locally()

sensor_logger = SensorLogger()
sensor_logger.start()

command = ['./src/sensor_data_simulator.x86_64-unknown-linux-gnu']
sensor_reader = SensorReader(command)
sensor_reader.start()
