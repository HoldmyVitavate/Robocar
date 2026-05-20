import board
from adafruit_pca9685 import PCA9685
import logging
import time

log = logging.getLogger(__name__)

# create I2C bus interface
i2c = board.I2C()
# create PCA9685 instance
pca = PCA9685(i2c)

# current motor speeds
current_speed_front_left = 0
current_speed_front_right = 0
current_speed_rear_left = 0
current_speed_rear_right = 0

# Kanalbelegung
MOTOR_FL = (0, 1)   # front left
MOTOR_FR = (3, 2)   # front right
MOTOR_RL = (4, 5)   # rear left
MOTOR_RR = (7, 6)   # rear right


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


# TEST: Jeder Reifen einzeln vorwärts, rückwärts, dann alle

def test_all_tires():
    init()
    sleep = 3

 # --- Einzeltests vorwärts ---
    print("Vorderrad links : vorwärts")
    front_left(50)
    time.sleep(sleep)
    stop_all()

    print("Vorderrad rechts : vorwärts")
    front_right(50)
    time.sleep(sleep)
    stop_all()

    print("Hinterrad links : vorwärts")
    rear_left(50)
    time.sleep(sleep)
    stop_all()

    print("Hinterrad rechts : vorwärts")
    rear_right(50)
    time.sleep(sleep)
    stop_all()

    # --- Einzeltests rückwärts ---
    print("Vorderrad links : rückwärts")
    front_left(-50)
    time.sleep(sleep)
    stop_all()

    print("Vorderrad rechts : rückwärts")
    front_right(-50)
    time.sleep(sleep)
    stop_all()

    print("Hinterrad links : rückwärts")
    rear_left(-50)
    time.sleep(sleep)
    stop_all()

    print("Hinterrad rechts : rückwärts")
    rear_right(-50)
    time.sleep(sleep)
    stop_all()

    # --- Alle vorwärts ---
    print("Alle Reifen : vorwärts")
    front_left(30)
    front_right(30)
    rear_left(30)
    rear_right(30)
    time.sleep(sleep)
    stop_all()
    
        # --- Im Kreis ---
    print("Alle Reifen : vorwärts")
    front_left(30)
    front_right(-30)
    rear_left(-30)
    rear_right(30)
    time.sleep(sleep)
    stop_all()

    print("Test abgeschlossen.")


if __name__ == "__main__":
    test_all_tires()
