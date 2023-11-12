import time
import random

def generate_values(probability=0.05):
    # counter = 0

    while True:
        # if counter > 0:
        #     counter -= 1
        #     yield True
        if random.random() < probability:
            # counter = random.randint(1, 5)   # motion detected for a certain period of time
            yield True
        else:
            yield False

      
def run_pir_simulator(id, delay, callback, stop_event):
    for motion_detected in generate_values():
        time.sleep(delay)
        callback(motion_detected, id)
        if stop_event.is_set():
                break