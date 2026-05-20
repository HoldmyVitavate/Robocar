import logging
import time
from smbus2 import SMBus
from adafruit_pca9685 import PCA9685

log = logging.getLogger(__name__)

# ---------------------------------------------------------
# I2C FIX für Python 3.13 (statt board.I2C())
# ---------------------------------------------------------

bus = SMBus(1)  # /dev/i2c-1

class FakeI2C:
    def writeto(self, addr, buf):
        bus.write_i2c_block_data(addr, buf[0], list(buf[1:]))

    def readfrom_into(self, addr, buf):
        data = bus.read_i2c_block_data(addr, 0, len(buf))
        for i in range(len(buf)):
            buf[i] = data[i]

i2c = FakeI2C()
pca = PCA9685(i2c)

# ---------------------------------------------------------
# Motor-Variablen
# ---------------------------------------------------------

current_speed_front_left = 0
current_speed_front_right = 0
current_speed_rear_left = 0
current_speed_rear_right = 0

# Kanalbelegung
MOTOR_FL = (0, 1)   # front left
MOTOR_FR = (2, 3)   # front right
MOTOR_RL = (4, 5)   # rear left
MOTOR_RR = (6, 7)   # rear right

# ---------------------------------------------------------
# Funktionen
# ---------------------------------------------------------

def init():
    print("Initialisiere PCA9685…")
    pca.frequency = 50

    for ch in range(16):
        pca.channels[ch].duty_cycle = 0

    print("PCA9685 bereit.")


def stop_all():
    global current_speed_front_left, current_speed_front_right
    global current_speed_rear_left, current_speed_rear_right

    for ch in range(16):
        pca.channels[ch].duty_cycle = 0

    current_speed_front_left = 0
    current_speed_front_right = 0
    current_speed_rear_left = 0
    current_speed_rear_right = 0

    print("Alle Motoren gestoppt.")


def _set_motor(channel_a, channel_b, speed):
    """Hilfsfunktion für alle Motoren"""
    if abs(speed) > 100:
        log.error(f"speed {speed} outside of range 0-100")
        return

    motor_speed = int((abs(speed) * 0xFFFF) / 100)

    if speed >= 0:
        pca.channels[channel_a].duty_cycle = 0
        pca.channels[channel_b].duty_cycle = motor_speed
    else:
        pca.channels[channel_a].duty_cycle = motor_speed
        pca.channels[channel_b].duty_cycle = 0


def front_left(speed=0):
    global current_speed_front_left
    current_speed_front_left = speed
    _set_motor(*MOTOR_FL, speed)


def front_right(speed=0):
    global current_speed_front_right
    current_speed_front_right = speed
    _set_motor(*MOTOR_FR, speed)


def rear_left(speed=0):
    global current_speed_rear_left
    current_speed_rear_left = speed
    _set_motor(*MOTOR_RL, speed)


def rear_right(speed=0):
    global current_speed_rear_right
    current_speed_rear_right = speed
    _set_motor(*MOTOR_RR, speed)


# ---------------------------------------------------------
# TEST: Alle Räder nacheinander + gleichzeitig
# ---------------------------------------------------------

def test_all_motors():
    print("Starte Testlauf für alle Räder…")
    init()

    print("Vorderrad links: 50%")
    front_left(50)
    time.sleep(1)

    print("Vorderrad rechts: 50%")
    front_right(50)
    time.sleep(1)

    print("Hinterrad links: 50%")
    rear_left(50)
    time.sleep(1)

    print("Hinterrad rechts: 50%")
    rear_right(50)
    time.sleep(1)

    print("Alle Räder gleichzeitig: 60%")
    front_left(60)
    front_right(60)
    rear_left(60)
    rear_right(60)
    time.sleep(3)

    print("Stoppe alle Motoren…")
    stop_all()

    print("Test abgeschlossen.")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    test_all_motors()
