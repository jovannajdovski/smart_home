
import threading
from settings import load_settings
from components.dht import run_dht
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting PI1 controller')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        rdht1_settings = settings['RDHT1']
        rdht2_settings = settings['RDHT2']
        run_dht(rdht1_settings, threads, stop_event)
        run_dht(rdht2_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping PI1 controller')
        for t in threads:
            stop_event.set()
