
import threading
import time
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter



def led_diode_callback(state, settings):      
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"LED DIODE ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"LED DIODE: {state}"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': state
        }
    


def run_led_diode(settings, threads, stop_event):
    # threads.append(publisher_thread)
    if settings['simulated']:
        from simulators.led_diode import run_led_diode_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        led_diode_thread = threading.Thread(target = run_led_diode_simulator, args=(settings, 5, led_diode_callback, stop_event))
        led_diode_thread.start()
        threads.append(led_diode_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.led_diode import run_led_diode_loop, LedDiode
        print(f"\nStarting {settings['id']} loop\n")
        led_diode = LedDiode(settings['id'], settings['pin'])
        led_diode.setup_rgb_diode()
        led_diode_thread = threading.Thread(target=run_led_diode_loop, args=(led_diode, settings, 5, led_diode_callback, stop_event))
        led_diode_thread.start()
        threads.append(led_diode_thread)
        print(f"\n{settings['id']} loop started\n")