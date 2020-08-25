from dataclasses import dataclass

@dataclass
class MqttConfig:
    broker_address: str = '127.0.0.1'
    port: int = 1883
    stay_alive: int = 60
    telemetry_topic: str = 'sensordata'
    control_topic: str = 'commands'
