import logging
import time

import motor
import sensor

log = logging.getLogger(__name__)

BASE_SPEED = 40
STEER_SPEED = 25


def init_all():
    print("Initialisiere Steuerungssystem...")
    motor.init()
    sensor.init()
    print("Alle Systeme erfolgreich verknüpft.")


def run_automation():
    init_all()
    time.sleep(2)

    last_direction = "mitte"

    try:
        while True:
            links, mitte, rechts = sensor.read_sensors()

            if mitte == 1 and links == 0 and rechts == 0:
                motor.drive_forward(BASE_SPEED)
                last_direction = "mitte"

            elif links == 1 and mitte == 1 and rechts == 0:
                motor.steer_left(STEER_SPEED)
                last_direction = "links"

            elif links == 1 and mitte == 0 and rechts == 0:
                motor.spin_left(STEER_SPEED)
                last_direction = "links"

            elif rechts == 1 and mitte == 1 and links == 0:
                motor.steer_right(STEER_SPEED)
                last_direction = "rechts"

            elif rechts == 1 and mitte == 0 and links == 0:
                motor.spin_right(STEER_SPEED)
                last_direction = "rechts"

            elif links == 1 and mitte == 1 and rechts == 1:
                motor.drive_forward(BASE_SPEED)

            elif links == 0 and mitte == 0 and rechts == 0:
                if last_direction == "links":
                    motor.spin_left(STEER_SPEED)
                elif last_direction == "rechts":
                    motor.spin_right(STEER_SPEED)
                else:
                    motor.drive_forward(BASE_SPEED - 5)

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\n\n[INFO] Abbruch durch Nutzer.")
        motor.stop_all()


if __name__ == "__main__":
    run_automation()
