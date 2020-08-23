import subprocess


class SensorReader:
    size_plength = 4

    def __init__(self, simulator_command):
        self.process = subprocess.Popen(simulator_command, shell=False, stdout=subprocess.PIPE)
        self.running = True
        self.read_sensor()

    def read_sensor(self):
        while self.running:
            bin_plength = self.read_binary_data(self.size_plength)
            package_length = int.from_bytes(bin_plength, byteorder='big')
            bin_package = self.read_binary_data(package_length - self.size_plength)
            print('{} - {} | {}'.format(bin_plength, bin_package, package_length))

    def read_binary_data(self, read_size):
        while True:
            binary_data = self.process.stdout.read(read_size)
            if binary_data:
                return binary_data


if __name__ == '__main__':
    cmd = './sensor_data_simulator.x86_64-unknown-linux-gnu'
    arg = '--name=445t-e1'
    command = [cmd, arg]

    sensor_reader = SensorReader(command)
