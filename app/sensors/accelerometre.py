import smbus2
import time
from math import atan2, sqrt, degrees
from telemetria_shared import telemetria_data

class ModulAccelerometer:
    def __init__(self, bus_num=6, address=0x68):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        self.bus.write_byte_data(self.address, 0x6B, 0)  # Wake up

    def _read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        if value > 32767:
            value -= 65536
        return value

    def get_accel(self):
        x = self._read_raw_data(0x3B) / 16384.0
        y = self._read_raw_data(0x3D) / 16384.0
        z = self._read_raw_data(0x3F) / 16384.0
        return {'x': x, 'y': y, 'z': z}

    def get_gyro(self):
        x = self._read_raw_data(0x43) / 131.0
        y = self._read_raw_data(0x45) / 131.0
        z = self._read_raw_data(0x47) / 131.0
        return {'x': x, 'y': y, 'z': z}

    def get_temp(self):
        raw_temp = self._read_raw_data(0x41)
        temp_c = (raw_temp / 340.0) + 36.53
        return round(temp_c, 2)

    def get_pitch_roll(self):
        a = self.get_accel()
        pitch = degrees(atan2(a['y'], sqrt(a['x']**2 + a['z']**2)))
        roll = degrees(atan2(-a['x'], a['z']))
        return {'pitch': round(pitch, 2), 'roll': round(roll, 2)}

    def read_data(self):
        return {
            'accel': self.get_accel(),
            'gyro': self.get_gyro(),
            'temp': self.get_temp(),
            'angle': self.get_pitch_roll()
        }

    def print_data(self):
        data = self.read_data()
        print(f"📈 Accel: {data['accel']}")
        print(f"🌀 Gyro: {data['gyro']}")
        print(f"🌡️ Temp: {data['temp']} ºC")
        print(f"🎯 Pitch/Roll: {data['angle']}")
        
    def thread(self):
        while True:
            telemetria_data["accel"] = self.get_accel()
            telemetria_data["gyro"] = self.get_gyro()
            telemetria_data["gyro_temp"] = self.get_temp()
            telemetria_data["angle"] = self.get_pitch_roll()
            time.sleep(0.5)
