# sensor-logging

## to ask
- what is the location of the device, for the timestamp
- should temperature be in degrees celcius or kelvin, the data contradicts itself. 

## Setup 

### Prerequsit
Have a version of python >= 3.7.0

###

Install an MQTT broker, E.Q. Mosquitto, and verify it is running 
'''
sudo apt-get install mosquitto
systemctl status mosquitto
'''
add the following to /etc/mosquitto/conf.d/myconfig.conf. Make sure to have a newline at the end of the file
'''
persistence false

# mqtt
listener 1883
protocol mqtt

'''
Restart the MQTT broker and you're good to go
'''
sudo service mosquitto restart
mosquitto -v
'''
(Make sure port TCP:1883 is open on your firewall)

Install python3 dependancies