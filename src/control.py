import json
import logging
import time
import motor
import sensor

log = logging.getLogger(__name__)

def run_automation():
    motor.init()
    sensor.init()

    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
    except Exception as e:
        log.error(f"Fehler beim Laden der config.json: {e}")
        return

    base_speed = config["BASE_SPEED"]
    steer_speed = config["STEER_SPEED"]
    spin_speed = config["SPIN_SPEED"]
    inner_factor = config["SMOOTH_STEER_FACTOR_INNER"]
    outer_factor = config["SMOOTH_STEER_FACTOR_OUTER"]
    spin_factor = config["SHARP_SPIN_FACTOR"]
    correction_factor = config["CORRECTION_FACTOR"]

    time.sleep(config["START_DELAY_SECONDS"])
    last_direction = "mitte"

    try:
        while True:
            links, mitte, rechts = sensor.read_sensors()

            if (mitte and not links and not rechts) or (links and mitte and rechts):
                motor.drive_forward(base_speed)
                last_direction = "mitte"

            elif links and mitte and not rechts:
                motor.steer(
                    int(steer_speed * inner_factor), int(steer_speed * outer_factor)
                )
                last_direction = "links"

            elif links and not mitte and not rechts:
                motor.steer(
                    -int(spin_speed * spin_factor), int(spin_speed * spin_factor)
                )
                last_direction = "links"

            elif rechts and mitte and not links:
                motor.steer(
                    int(steer_speed * outer_factor), int(steer_speed * inner_factor)
                )
                last_direction = "rechts"

            elif rechts and not mitte and not links:
                motor.steer(
                    int(spin_speed * spin_factor), -int(spin_speed * spin_factor)
                )
                last_direction = "rechts"

            elif not links and not mitte and not rechts:
                if last_direction == "links":
                    motor.steer(-spin_speed, spin_speed)
                elif last_direction == "rechts":
                    motor.steer(spin_speed, -spin_speed)
                else:
                    motor.drive_forward(base_speed - correction_factor)

            time.sleep(config["LOOP_DELAY_SECONDS"])

    except KeyboardInterrupt:
        motor.stop_all()
