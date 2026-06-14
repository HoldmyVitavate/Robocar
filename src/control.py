import json
import logging
import time

import motor
import sensor

log = logging.getLogger(__name__)

BASE_SPEED = 40
STEER_SPEED = 25
BREAK_DELAY = 2.0
DELAY_CORRECTION = 0.005
STRAIGHT_REDUCTION = 5

LINE_DETECTED = 1
LINE_NOT_DETECTED = 0

DIRECTION_MITTE = "mitte"
DIRECTION_LINKS = "links"
DIRECTION_RECHTS = "rechts"


def load_config():
    global BASE_SPEED, STEER_SPEED, BREAK_DELAY, DELAY_CORRECTION, STRAIGHT_REDUCTION
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        BASE_SPEED = config.get("BASE_SPEED", BASE_SPEED)
        STEER_SPEED = config.get("STEER_SPEED", STEER_SPEED)
        BREAK_DELAY = config.get("BREAK_DELAY", BREAK_DELAY)
        DELAY_CORRECTION = config.get("DELAY_CORRECTION", DELAY_CORRECTION)
        STRAIGHT_REDUCTION = config.get("STRAIGHT_REDUCTION", STRAIGHT_REDUCTION)
        print("Konfiguration erfolgreich aus JSON geladen.")
    except Exception as e:
        log.warning(f"Fehler beim Laden der config.json, nutze Standardwerte: {e}")


def init_all():
    print("Initialisiere Steuerungssystem...")
    load_config()
    motor.init()
    sensor.init()
    print("Alle Systeme erfolgreich verknüpft.")


def run_automation():
    init_all()
    time.sleep(BREAK_DELAY)
    last_direction = DIRECTION_MITTE

    try:
        while True:
            links, mitte, rechts = sensor.read_sensors()

            if (
                mitte == LINE_DETECTED
                and links == LINE_NOT_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.drive_forward(BASE_SPEED)
                last_direction = DIRECTION_MITTE

            elif (
                links == LINE_DETECTED
                and mitte == LINE_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.steer_left(STEER_SPEED)
                last_direction = DIRECTION_LINKS

            elif (
                links == LINE_DETECTED
                and mitte == LINE_NOT_DETECTED
                and rechts == LINE_NOT_DETECTED
            ):
                motor.spin_left(STEER_SPEED)
                last_direction = DIRECTION_LINKS

            elif (
                rechts == LINE_DETECTED
                and mitte == LINE_DETECTED
                and links == LINE_NOT_DETECTED
            ):
                motor.steer_right(STEER_SPEED)
                last_direction = DIRECTION_RECHTS

            elif (
                rechts == LINE_DETECTED
                and mitte == LINE_NOT_DETECTED
                and links == LINE_NOT_DETECTED
            ):
                motor.spin_right(STEER_SPEED)
                last_direction = DIRECTION_RECHTS

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
                if last_direction == DIRECTION_LINKS:
                    motor.spin_left(STEER_SPEED)
                elif last_direction == DIRECTION_RECHTS:
                    motor.spin_right(STEER_SPEED)
                else:
                    motor.drive_forward(BASE_SPEED - STRAIGHT_REDUCTION)

            time.sleep(DELAY_CORRECTION)

    except KeyboardInterrupt:
        motor.stop_all()


if __name__ == "__main__":
    run_automation()
