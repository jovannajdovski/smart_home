import time
import random
from datetime import datetime

def generate_values(probability=0.2):
    while True:
        if random.random() < probability:
            yield True
        else:
            yield False


def run_button_simulator(settings, delay, last_released_time, callback, stop_event):
    for button_pressed in generate_values():
        time.sleep(delay)
        if button_pressed:
            callback(settings)
        else:
            last_released_time[settings['id']]=datetime.now()
        if stop_event.is_set():
            break

