from dataclasses import dataclass


class Decoder:
    @dataclass
    class Sizes:
        name: int
        time: int = 8
        nlen: int = 1
        temp: int = 3
        humi: int = 2

    @dataclass
    class Offsets:
        mandatory_fields: int
        time: int = 0
        nlen: int = 8
        name: int = 9

    @staticmethod
    def decode_binary_data(data, start_pos, end_pos, numerical):
        bin_slice = data[start_pos:end_pos]
        if numerical:
            return int.from_bytes(bin_slice, byteorder='big')
        else:
            return bin_slice.decode('UTF-8')

    def decode_log_data(self, bin_data):
        log_man_fields = self.decode_mandatory_fields(bin_data)
        log_opt_fields = self.decode_optional_fields(bin_data)
        return {**log_man_fields, **log_opt_fields}

    def decode_mandatory_fields(self, data):
        self.Sizes.name = self.decode_binary_data(data, start_pos=self.Offsets.nlen, numerical=True,
                                                  end_pos=self.Offsets.nlen + self.Sizes.nlen)
        timestamp = self.decode_binary_data(data, start_pos=self.Offsets.time, numerical=True,
                                            end_pos=self.Offsets.time + self.Sizes.time)
        name = self.decode_binary_data(data, start_pos=self.Offsets.name, numerical=False,
                                       end_pos=self.Offsets.name + self.Sizes.name)
        return {'timestamp': timestamp, 'name': name}

    def decode_optional_fields(self, data):
        self.Offsets.mandatory_fields = self.Offsets.name + self.Sizes.name
        size_optional_fields = len(data) - self.Offsets.mandatory_fields
        if size_optional_fields == self.Sizes.temp:
            return {'temp': self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                                    end_pos=self.Offsets.mandatory_fields + self.Sizes.temp)}
        elif size_optional_fields == self.Sizes.humi:
            return {'humi': self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                                    end_pos=self.Offsets.mandatory_fields + self.Sizes.humi)}
        elif size_optional_fields == self.Sizes.temp + self.Sizes.humi:
            temp = self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields, numerical=True,
                                           end_pos=self.Offsets.mandatory_fields + self.Sizes.temp)
            humi = self.decode_binary_data(data, start_pos=self.Offsets.mandatory_fields + self.Sizes.temp,
                                           end_pos=self.Offsets.mandatory_fields + self.Sizes.temp + self.Sizes.humi,
                                           numerical=True)
            return {'temp': temp, 'humi': humi}
        else:
            return {}
