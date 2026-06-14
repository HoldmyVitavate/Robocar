import json
import logging

import board
from adafruit_pca9685 import PCA9685

log = logging.getLogger(__name__)

MOTOR_FRONT_LEFT = (0, 1)
MOTOR_REAR_LEFT = (3, 2)
MOTOR_REAR_RIGHT = (4, 5)
MOTOR_FRONT_RIGHT = (7, 6)

PWM_MAX_VALUE = 0xFFFF
MAX_SPEED_PERCENT = 100
PCA_FREQUENCY = 50
TOTAL_CHANNELS = 16

try:
    with open("config.json", "r") as f:
        config = json.load(f)
    FACTOR_STEER_INNER = config.get("FACTOR_STEER_INNER", 0.4)
    FACTOR_STEER_OUTER = config.get("FACTOR_STEER_OUTER", 1.2)
    FACTOR_SPIN = config.get("FACTOR_SPIN", 1.2)
except Exception as e:
    log.warning(f"Fehler beim Laden der config.json in Motor.py, nutze Defaults: {e}")
    FACTOR_STEER_INNER = 0.4
    FACTOR_STEER_OUTER = 1.2
    FACTOR_SPIN = 1.2

i2c = board.I2C()
pca = PCA9685(i2c)


def init():
    print("Initialisiere PCA9685...")
    pca.frequency = PCA_FREQUENCY
    stop_all()
    print("PCA9685 bereit.")


def stop_all():
    for ch in range(TOTAL_CHANNELS):
        pca.channels[ch].duty_cycle = 0


def _set_motor(channel_a, channel_b, speed):
    if abs(speed) > MAX_SPEED_PERCENT:
        log.error(f"Geschwindigkeit {speed} außerhalb des Bereichs -100 bis 100")
        return

    motor_speed = int((abs(speed) * PWM_MAX_VALUE) / MAX_SPEED_PERCENT)

    if speed >= 0:
        pca.channels[channel_a].duty_cycle = 0
        pca.channels[channel_b].duty_cycle = motor_speed
    else:
        pca.channels[channel_a].duty_cycle = motor_speed
        pca.channels[channel_b].duty_cycle = 0


def front_left(speed=0):
    _set_motor(*MOTOR_FRONT_LEFT, speed)


def front_right(speed=0):
    _set_motor(*MOTOR_FRONT_RIGHT, speed)


def rear_left(speed=0):
    _set_motor(*MOTOR_REAR_LEFT, speed)


def rear_right(speed=0):
    _set_motor(*MOTOR_REAR_RIGHT, speed)


def drive_forward(speed):
    front_left(speed)
    front_right(speed)
    rear_left(speed)
    rear_right(speed)


def steer_left(base_speed):
    front_left(int(base_speed * FACTOR_STEER_INNER))
    rear_left(int(base_speed * FACTOR_STEER_INNER))
    front_right(int(base_speed * FACTOR_STEER_OUTER))
    rear_right(int(base_speed * FACTOR_STEER_OUTER))


def steer_right(base_speed):
    front_left(int(base_speed * FACTOR_STEER_OUTER))
    rear_left(int(base_speed * FACTOR_STEER_OUTER))
    front_right(int(base_speed * FACTOR_STEER_INNER))
    rear_right(int(base_speed * FACTOR_STEER_INNER))


def spin_left(base_speed):
    speed = int(base_speed * FACTOR_SPIN)
    front_left(-speed)
    rear_left(-speed)
    front_right(speed)
    rear_right(speed)


def spin_right(base_speed):
    speed = int(base_speed * FACTOR_SPIN)
    front_left(speed)
    rear_left(speed)
    front_right(-speed)
    rear_right(-speed)
