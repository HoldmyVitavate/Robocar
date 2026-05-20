import logging
import time
from typing import Optional

from gpiozero import LineSensor

log = logging.getLogger(__name__)

# PIN BELEGUNG
PIN_LINKS = 14
PIN_MITTE = 15
PIN_RECHTS = 23

sensor_l: Optional[LineSensor] = None
sensor_m: Optional[LineSensor] = None
sensor_r: Optional[LineSensor] = None


def init():
    global sensor_l, sensor_m, sensor_r
    print("Initialisiere Linien-Sensoren...")
    sensor_l = LineSensor(PIN_LINKS)
    sensor_m = LineSensor(PIN_MITTE)
    sensor_r = LineSensor(PIN_RECHTS)

    print("Sensoren funktionieren.")


def read_sensors():
    global sensor_l, sensor_m, sensor_r

    if sensor_l is None or sensor_m is None or sensor_r is None:
        init()

    assert sensor_l is not None
    assert sensor_m is not None
    assert sensor_r is not None

    links_erkannt = 1 if sensor_l.value else 0
    mitte_erkannt = 1 if sensor_m.value else 0
    rechts_erkannt = 1 if sensor_r.value else 0

    return links_erkannt, mitte_erkannt, rechts_erkannt


def test_sensors():
    init()
    print("LINIENSENSOR-TEST...")
    print("Bewege ein schwarzes Objekt unter die Sensoren.")

    try:
        while True:
            links, mitte, rechts = read_sensors()
            print(
                f"Sensoren ->  LINKS: [{links}]   MITTE: [{mitte}]   RECHTS: [{rechts}]",
                end="\r",
            )
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[INFO] Test erfolgreich.")


if __name__ == "__main__":
    test_sensors()
