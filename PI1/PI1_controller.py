
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('\nStarting PI1 controller\n')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        rdht1_settings = settings['RDHT1']
        rdht2_settings = settings['RDHT2']
        dus1_settings = settings['DUS1']
        run_dht(rdht1_settings, threads, stop_event)
        run_dht(rdht2_settings, threads, stop_event)
        run_uds(dus1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\nStopping PI1 controller\n')
        for t in threads:
            stop_event.set()
