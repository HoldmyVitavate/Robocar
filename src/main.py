import logging

import control
import motor

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():

    try:
        control.run_automation()

    except KeyboardInterrupt:
        print("\n\n[INFO] Programm durch Benutzer abgebrochen (Strg+C).")
    except Exception as e:
        log.error(f"Unerwarteter Fehler im Hauptprogramm: {e}")
    finally:
        print("[INFO] Nothalt: Stelle Motoren ab...")
        motor.stop_all()
        print("Programm sicher beendet.\n")


if __name__ == "__main__":
    main()
