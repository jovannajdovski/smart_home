import time
import random

def generate_values(initial_distance = 0, stride = 10):   # 0.1m
    distance = initial_distance
    while True:
        distance = round(distance + round(random.uniform(-1, 1), 2) * stride, 2)
        if distance < 0:
            distance = 0
        if distance > 200:
            distance = 200
        yield distance

      
def run_uds_simulator(settings, delay, callback, stop_event):
    for distance in generate_values():
        time.sleep(delay)
        callback(distance, settings)
        if stop_event.is_set():
                break