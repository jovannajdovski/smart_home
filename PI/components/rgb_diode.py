
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter

totalPersons=None

def rgb_diode_callback(color, settings):      
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"RGB DIODE ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"RGB DIODE: Current color {color}"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': color
        }
    


def run_rgb_diode(settings, _totalPersons, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    # threads.append(publisher_thread)
    if settings['simulated']:
        from simulators.rgb_diode import run_rgb_diode_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        rgb_diode_thread = threading.Thread(target = run_rgb_diode_simulator, args=(settings, 0.5, rgb_diode_callback, stop_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.rgb_diode import run_rgb_diode_loop, RgbDiode
        print(f"\nStarting {settings['id']} loop\n")
        rgb_diode = RgbDiode(settings['id'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        rgb_diode.setup_rgb_diode()
        rgb_diode_thread = threading.Thread(target=run_rgb_diode_loop, args=(rgb_diode, settings, 0.5, rgb_diode_callback, stop_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} loop started\n")