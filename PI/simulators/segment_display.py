import time
from datetime import datetime


def run_4segment_simulator(settings, delay, callback, stop_event):
    while not stop_event.is_set():
        current_time = datetime.now()

        current_hour = current_time.hour
        current_minute = current_time.minute

        digit1 = current_hour // 10
        digit2 = current_hour % 10

        digit3 = current_minute // 10
        digit4 = current_minute % 10

        callback(digit1, digit2, digit3, digit4, settings)
        time.sleep(delay)


