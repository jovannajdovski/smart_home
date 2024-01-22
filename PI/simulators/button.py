import time
import random
from datetime import datetime

def generate_values(probability=0.2):
    while True:
        if random.random() < probability:
            yield True
        else:
            yield False

def generate_values_pressing_five_seconds(probability=0.2):
    for i in range(25):
        if(i<7):
            yield True
        elif(i==13):
            yield True
        elif(i<19):
            yield False
        else:
            yield True
        time.sleep(1)


def run_button_simulator(settings, delay, last_released_time, callback, stop_event):
    # for button_pressed in generate_values():
    #     time.sleep(delay)
    #     if settings['id'] not in last_released_time:
    #         last_released_time[settings['id']]=datetime.now()
    #     if button_pressed:
    #         callback(settings)
    #     else:
    #         last_released_time[settings['id']]=datetime.now()
    #     if stop_event.is_set():
    #         break
    if settings['id'] not in last_released_time:
            last_released_time[settings['id']]=datetime.now()
    for button_pressed in generate_values_pressing_five_seconds():
        if button_pressed:
            callback(settings)
        else:
            last_released_time[settings['id']]=datetime.now()
        if stop_event.is_set():
            break

