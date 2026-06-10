import logging
import control
import motor

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    try:
        control.run_automation()
    except KeyboardInterrupt:
        print("\nProgramm durch Benutzer abgebrochen.")
    except Exception as e:
        log.error(f"Unerwarteter Fehler: {e}")
    finally:
        motor.stop_all()
        print("Nothalt aktiviert. Programm sicher beendet.")


if __name__ == "__main__":
    main()
