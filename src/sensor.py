import logging
import time
from typing import Optional, Tuple

from gpiozero import LineSensor

log = logging.getLogger(__name__)

PIN_SENSOR_LINKS = 14
PIN_SENSOR_MITTE = 15
PIN_SENSOR_RECHTS = 23

SENSOR_DETECTED = 1
SENSOR_NOT_DETECTED = 0
TEST_DELAY = 0.1

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


def read_sensors() -> Tuple[int, int, int]:
    global sensor_links, sensor_mitte, sensor_rechts
    if sensor_links is None or sensor_mitte is None or sensor_rechts is None:
        init()

    assert sensor_links is not None
    assert sensor_mitte is not None
    assert sensor_rechts is not None

    links_erkannt = SENSOR_DETECTED if sensor_links.value else SENSOR_NOT_DETECTED
    mitte_erkannt = SENSOR_DETECTED if sensor_mitte.value else SENSOR_NOT_DETECTED
    rechts_erkannt = SENSOR_DETECTED if sensor_rechts.value else SENSOR_NOT_DETECTED

    return links_erkannt, mitte_erkannt, rechts_erkannt


def test_sensors():
    init()
    print("LINIENSENSOR-TEST...")
    print("Bewege ein schwarzes Objekt unter die Sensoren. Beenden mit Strg+C.")

    try:
        while True:
            links, mitte, rechts = read_sensors()
            print(
                f"Sensoren ->  LINKS: [{links}]   MITTE: [{mitte}]   RECHTS: [{rechts}]",
                end="\r",
            )
            time.sleep(TEST_DELAY)
    except KeyboardInterrupt:
        print("\n\n[INFO] Test erfolgreich beendet.")


if __name__ == "__main__":
    test_sensors()
