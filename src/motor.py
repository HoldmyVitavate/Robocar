import logging
import time

import board
from adafruit_pca9685 import PCA9685

log = logging.getLogger(__name__)

i2c = board.I2C()
pca = PCA9685(i2c)

MOTOR_FL = (0, 1)  # front left
MOTOR_RL = (3, 2)  # rear left
MOTOR_RR = (4, 5)  # rear right
MOTOR_FR = (7, 6)  # front right


def init():
    print("Initialisiere PCA9685...")
    pca.frequency = 50
    for ch in range(16):
        pca.channels[ch].duty_cycle = 0
    print("PCA9685 bereit.")


def stop_all():
    for ch in range(16):
        pca.channels[ch].duty_cycle = 0


def _set_motor(channel_a, channel_b, speed):
    if abs(speed) > 100:
        log.error(f"speed {speed} outside of range -100 to 100")
        return

    motor_speed = int((abs(speed) * 0xFFFF) / 100)

    if speed >= 0:
        pca.channels[channel_a].duty_cycle = 0
        pca.channels[channel_b].duty_cycle = motor_speed
    else:
        pca.channels[channel_a].duty_cycle = motor_speed
        pca.channels[channel_b].duty_cycle = 0


def front_left(speed=0):
    _set_motor(*MOTOR_FL, speed)


def front_right(speed=0):
    _set_motor(*MOTOR_FR, speed)


def rear_left(speed=0):
    _set_motor(*MOTOR_RL, speed)


def rear_right(speed=0):
    _set_motor(*MOTOR_RR, speed)


def drive_forward(speed):
    front_left(speed)
    front_right(speed)
    rear_left(speed)
    rear_right(speed)


def steer_left(base_speed):
    front_left(int(base_speed * 0.1))
    rear_left(int(base_speed * 0.1))
    front_right(int(base_speed * 1.3))
    rear_right(int(base_speed * 1.3))


def steer_right(base_speed):
    front_left(int(base_speed * 1.3))
    rear_left(int(base_speed * 1.3))
    front_right(int(base_speed * 0.1))
    rear_right(int(base_speed * 0.1))


def spin_left(base_speed):
    front_left(-int(base_speed * 1.2))
    rear_left(-int(base_speed * 1.2))
    front_right(int(base_speed * 1.2))
    rear_right(int(base_speed * 1.2))


def spin_right(base_speed):
    front_left(int(base_speed * 1.2))
    rear_left(int(base_speed * 1.2))
    front_right(-int(base_speed * 1.2))
    rear_right(-int(base_speed * 1.2))
