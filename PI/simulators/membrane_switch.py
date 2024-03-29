import time
import random

def generate_values(probability=0.2):
    keys=['0','1','2','3','4','5','6','7','8','9','*','0','#','A','B','C','D']
    while True:
        r=random.random()
        if r < probability:
            yield keys[round(len(keys)*r/probability)-1]
        else:
            yield None

def generate_values_password(probability=0.2):
    keys1=['3','0','1','2','3','4','1','2','3','4']
    delayes=[20,3,3,3,3,15,3,3,3,3]
    for item1, item2 in zip(keys1, delayes):
        yield item1
        time.sleep(item2)

def run_membrane_switch_simulator(settings, delay, callback, stop_event):
    
    # for pressed_key in generate_values():
    #     time.sleep(delay)
    #     if pressed_key is not None:
    #         callback(pressed_key, settings)
    #     if stop_event.is_set():
    #         break
    while True:
        #for pressed_key in generate_values_password():
            # print('pressed key ', pressed_key)
            # if pressed_key is not None:
            #     callback(pressed_key, settings)
        if stop_event.is_set():
            break