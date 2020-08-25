![sensor-logging-tests](https://github.com/DankersW/sensor-logging/workflows/sensor-logging-tests/badge.svg)
# Sensor-logging
The Sensor-logging assignment consist of two major instances. One instance that handles the simulator and decodes its 
output. Whereas the other one saves the sensor data to a log file in the desired format. The log file follows the 
naming convention ```log_[year][month][day]-[hour][minutes][seconds].txt``` and the generated logfile will be places 
under at the same location as where the program started. 

For the network communication between the instances MQTT is used. 

Also, in the repo one can find a directory containing basic unit tests as well as a Github workflow folder 
(Github Actions). Github Actions is a convenient way of implementing CI chains on Github.
  
## to ask
- what is the location of the device, for the timestamp
- should temperature be in degrees celcius or kelvin, the data contradicts itself. 

## Setup 
```bash
git clone https://github.com/DankersW/sensor-logging.git
cd sensor-logging
python3.7 __main__.py
```

## Prerequisites
Install Python3.7 and a MQTT broker on the linux machine.
### Python
Have a version of ``` python >= 3.7.0 ```


Install python3 dependencies
```bash
pip3 install -r requirements.txt
```

### MQTT broker

Install an MQTT broker, E.Q. Mosquitto, and verify it is running 
```bash
sudo apt-get install -y mosquitto
systemctl status mosquitto
```

add the following to ```/etc/mosquitto/conf.d/myconfig.conf```. Make sure to have a newline at the end of the file

```bash
persistence false

# mqtt
listener 1883
protocol mqtt

```

Restart the MQTT broker and you're good to go
```
sudo service mosquitto restart
```
(Make sure port TCP:1883 is open on your firewall)


## Possible system improvements
* Kill the sensor-logging tool in a clean way by sending a termination command over MQTT to both instances.
* Introduce more MQTT callbacks.
* Make it easy to spawn multiple sensor simulators.
* Build the app cross platform, not only for linux.  