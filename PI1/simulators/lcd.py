import time
from datetime import datetime


def run_lcd_simulator(settings, delay, callback, stop_event):

    while not stop_event.is_set():
        current_time = datetime.now()

        current_hour = current_time.hour
        current_minute = current_time.minute

        text = f"Current time : {current_hour}:{current_minute}"

        callback(text, settings)
        time.sleep(delay)