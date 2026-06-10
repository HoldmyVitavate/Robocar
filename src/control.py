import logging
import time

import motor
import sensor

log = logging.getLogger(__name__)

BASE_SPEED = 40
STEER_SPEED = 25

LINE_DETECTED = 1
LINE_NOT_DETECTED = 0

BREAK = 2
DELAY_CORRECTION = 0.005


def init_all():
    print("Initialisiere Steuerungssystem...")
    motor.init()
    sensor.init()
    print("Alle Systeme erfolgreich verknüpft.")


def run_automation():
    init_all()
    time.sleep(BREAK)

    last_direction = "mitte"

    try:
        while True:
            links, mitte, rechts = sensor.read_sensors()

            if (
                mitte == LINE_DETECTED
                and links == LINE_NOT_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.drive_forward(BASE_SPEED)
                last_direction = "mitte"

            elif (
                links == LINE_DETECTED
                and mitte == LINE_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.steer_left(STEER_SPEED)
                last_direction = "links"

            elif (
                links == LINE_DETECTED
                and mitte == LINE_NOT_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.spin_left(STEER_SPEED)
                last_direction = "links"

            elif (
                rechts == LINE_DETECTED
                and mitte == LINE_DETECTED
                and links == LINE_NOT_DETECTED
            ):
                motor.steer_right(STEER_SPEED)
                last_direction = "rechts"

            elif (
                rechts == LINE_DETECTED
                and mitte == LINE_NOT_DETECTED
                and links == LINE_NOT_DETECTED
            ):
                motor.spin_right(STEER_SPEED)
                last_direction = "rechts"

            elif (
                links == LINE_DETECTED
                and mitte == LINE_DETECTED
                and rechts == LINE_DETECTED
            ):
                motor.drive_forward(BASE_SPEED)

            elif (
                links == LINE_NOT_DETECTED
                and mitte == LINE_NOT_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                if last_direction == "links":
                    motor.spin_left(STEER_SPEED)
                elif last_direction == "rechts":
                    motor.spin_right(STEER_SPEED)
                else:
                    motor.drive_forward(BASE_SPEED - 5)

            time.sleep(DELAY_CORRECTION)

    except KeyboardInterrupt:
        motor.stop_all()


if __name__ == "__main__":
    run_automation()
