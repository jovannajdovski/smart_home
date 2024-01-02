import time
import random

def generate_values(probability=0.2):
    while True:
        if random.random() < probability:
            yield True
        else:
            yield False


def run_button_simulator(settings, delay, callback, stop_event):
    for button_pressed in generate_values():
        time.sleep(delay)
        if button_pressed:
            callback(settings)
        if stop_event.is_set():
            break

