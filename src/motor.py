import logging

import board
from adafruit_pca9685 import PCA9685

log = logging.getLogger(__name__)

i2c = board.I2C()
pca = PCA9685(i2c)

MOTOR_FRONT_LEFT = (0, 1)
MOTOR_REAR_LEFT = (3, 2)
MOTOR_REAR_RIGHT = (4, 5)
MOTOR_FRONT_RIGHT = (7, 6)

PCA_PWM_FREQUENCY = 50
MAX_PWM_VALUE = 0xFFFF  # 65535 (16-Bit Auflösung des PCA9685)
MIN_SPEED_LIMIT = -100
MAX_SPEED_LIMIT = 100
TOTAL_CHANNELS = 16

def init():
    print("Initialisiere PCA9685...")
    pca.frequency = PCA_PWM_FREQUENCY
    stop_all()
    print("PCA9685 bereit.")


def stop_all():
    for ch in range(TOTAL_CHANNELS):
        pca.channels[ch].duty_cycle = 0


def _set_motor(channel_a: int, channel_b: int, speed: int):
    """Interne Funktion zur Ansteuerung eines einzelnen Motors."""
    if not (MIN_SPEED_LIMIT <= speed <= MAX_SPEED_LIMIT):
        log.error(
            f"Geschwindigkeit {speed} außerhalb des erlaubten Bereichs ({MIN_SPEED_LIMIT} bis {MAX_SPEED_LIMIT})"
        )
        return

    motor_speed = int((abs(speed) * MAX_PWM_VALUE) / 100)

    if speed >= 0:
        pca.channels[channel_a].duty_cycle = 0
        pca.channels[channel_b].duty_cycle = motor_speed
    else:
        pca.channels[channel_a].duty_cycle = motor_speed
        pca.channels[channel_b].duty_cycle = 0


def front_left(speed: int = 0):
    _set_motor(*MOTOR_FRONT_LEFT, speed)


def front_right(speed: int = 0):
    _set_motor(*MOTOR_FRONT_RIGHT, speed)


def rear_left(speed: int = 0):
    _set_motor(*MOTOR_REAR_LEFT, speed)


def rear_right(speed: int = 0):
    _set_motor(*MOTOR_REAR_RIGHT, speed)

def drive_forward(speed: int):
    front_left(speed)
    front_right(speed)
    rear_left(speed)
    rear_right(speed)

def steer(left_speed: int, right_speed: int):
    front_left(left_speed)
    rear_left(left_speed)
    front_right(right_speed)
    rear_right(right_speed)
