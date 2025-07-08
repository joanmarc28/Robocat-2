import serial
import time
#import config
import smbus2
import math
from telemetria_shared import telemetria_data

I2C_ADDR = 0x0D  # Adreça habitual del QMC5883L

class ModulGPS:
    """Classe per gestionar el GPS i Compas"""
    def __init__(self):
        # --- GPS Setup (UART) ---
        self.gps_serial = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

        # --- Compass Setup (QMC5883L via I2C) ---
        self.i2c_bus = smbus2.SMBus(5)  # Utilitza el bus I2C configurat

        # Inicialitza el compàs
        # Mode: Continuous, Output Data Rate: 10Hz, Full Scale: 2G, Over Sample Ratio: 512
        self.i2c_bus.write_byte_data(I2C_ADDR, 0x0B, 0x01)  # Reset
        self.i2c_bus.write_byte_data(I2C_ADDR, 0x09, 0b00011101)

    def parse_coord(self, coord, direction):
        """Converteix coordenades NMEA a decimal"""
        degrees = float(coord[:2 if direction in ['N', 'S'] else 3])
        minutes = float(coord[2 if direction in ['N', 'S'] else 3:])
        decimal = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal *= -1
        return decimal

    def read_gps(self, timeout=10):
        """Llegeix coordenades durant màxim `timeout` segons"""
        start = time.time()
        while time.time() - start < timeout:
            line = self.gps_serial.readline().decode('ascii', errors='replace').strip()
            #print(f"[DEBUG] NMEA: {line}")

            if line.startswith(("$GPGGA", "$GNGGA", "$GNRMC")):
                parts = line.split(',')

                if line.startswith(("$GPGGA", "$GNGGA")) and len(parts) > 6:
                    if parts[2] and parts[4] and parts[6] != "0":
                        lat = self.parse_coord(parts[2], parts[3])
                        lon = self.parse_coord(parts[4], parts[5])
                        return lat, lon

                elif line.startswith("$GNRMC") and len(parts) > 6:
                    if parts[2] == "A":  # 'A' means valid data
                        lat = self.parse_coord(parts[3], parts[4])
                        lon = self.parse_coord(parts[5], parts[6])
                        return lat, lon

        return None, None
    
        
    def read_heading(self):
        """Llegeix i calcula l'angle del compàs (en graus)"""
        data = self.i2c_bus.read_i2c_block_data(I2C_ADDR, 0x00, 6)
        x = data[1] << 8 | data[0]
        y = data[3] << 8 | data[2]

        # Corregeix valors signed
        x = x - 65536 if x > 32767 else x
        y = y - 65536 if y > 32767 else y

        heading = math.atan2(y, x) * (180 / math.pi)
        if heading < 0:
            heading += 360
        return heading

    def read_gps_info(self):
        while True:
            try:
                print("🔍 Llegint GPS i brúixola...")
                lat, lon = self.read_gps(timeout=10)
                heading = self.read_heading()

                if lat is not None and lon is not None:
                    print(f"📍 Latitud: {lat:.6f}, Longitud: {lon:.6f}, Heading: {heading:.1f}°")
                else:
                    print("❗️ Sense fix GPS actualment")

                time.sleep(1)

            except KeyboardInterrupt:
                print("🛑 Sortint per teclat...")
                break

            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(0.5)

    def thread_gps(self):
        while True:
            """print("🔍 Llegint GPS ...")"""
            lat, lon = self.read_gps(timeout=10)

            if lat is not None and lon is not None:
                """print(f"📍 Latitud: {lat:.6f}, Longitud: {lon:.6f}")"""
                telemetria_data["lat"] = lat
                telemetria_data["lon"] = lon
            """else:
                print("❗️ Sense fix GPS actualment")"""
            time.sleep(1)

    def thread_heading(self):
        while True:
            """print("🔍 Llegint brúixola...")"""
            heading = self.read_heading()
            telemetria_data["heading"] = heading
            """print(f"Bruixola: {heading:.1f}°")"""
            time.sleep(1)
