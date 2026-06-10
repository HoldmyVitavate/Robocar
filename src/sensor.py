import logging
import time
from typing import Optional, Tuple

from gpiozero import LineSensor

log = logging.getLogger(__name__)

PIN_SENSOR_LINKS = 14
PIN_SENSOR_MITTE = 15
PIN_SENSOR_RECHTS = 23

sensor_links: Optional[LineSensor] = None
sensor_mitte: Optional[LineSensor] = None
sensor_rechts: Optional[LineSensor] = None


def init():
    global sensor_links, sensor_mitte, sensor_rechts
    print("Initialisiere Linien-Sensoren...")
    sensor_links = LineSensor(PIN_SENSOR_LINKS)
    sensor_mitte = LineSensor(PIN_SENSOR_MITTE)
    sensor_rechts = LineSensor(PIN_SENSOR_RECHTS)
    print("Sensoren betriebsbereit.")


def read_sensors() -> Tuple[bool, bool, bool]:
    global sensor_links, sensor_mitte, sensor_rechts
    if sensor_links is None or sensor_mitte is None or sensor_rechts is None:
        init()
    assert sensor_links is not None
    assert sensor_mitte is not None
    assert sensor_rechts is not None

    links_erkannt = bool(sensor_links.value)
    mitte_erkannt = bool(sensor_mitte.value)
    rechts_erkannt = bool(sensor_rechts.value)

    return links_erkannt, mitte_erkannt, rechts_erkannt


def test_sensors():
    init()
    print("LINIENSENSOR-TEST... Strg+C zum Abbrechen.")
    try:
        while True:
            links, mitte, rechts = read_sensors()
            print(
                f"Sensoren ->  LINKS: [{links}]   MITTE: [{mitte}]   RECHTS: [{rechts}]",
                end="\r",
            )
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[INFO] Test erfolgreich beendet.")


if __name__ == "__main__":
    test_sensors()
