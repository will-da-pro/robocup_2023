import time
from smbus2 import SMBus

def checkDistance(i2c_bus=1, i2c_address=0x52):
    try:
        bus = SMBus(i2c_bus)
        bus.write_byte(i2c_address, 0)
        time.sleep(0.01)
        value = bus.read_byte(i2c_address) << 8 | bus.read_byte(i2c_address)
        bus.close()
        return value
    except OSError as e:
        print(f"Error reading range: {e}")
        return None

if __name__ == "__main__":
    while True:
        distance = checkDistance()
        if distance is not None:
            print(f"Distance: {distance} mm")
        else:
            print("Error, retrying")
        time.sleep(0.1)

