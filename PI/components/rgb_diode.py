
import threading
import json
import time
from datetime import datetime
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 5
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None

def rgb_diode_callback(color, settings, action = "Current color"):      
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"RGB DIODE ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"RGB DIODE: {action} {color}"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': color,
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, False))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()
    


def run_rgb_diode(settings, _totalPersons, threads, stop_event, rgb_power_on_event, red_event, green_event, blue_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)
    if settings['simulated']:
        from simulators.rgb_diode import run_rgb_diode_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        rgb_diode_thread = threading.Thread(target = run_rgb_diode_simulator, args=(settings, 0.5, rgb_diode_callback, stop_event, rgb_power_on_event, red_event, green_event, blue_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.rgb_diode import run_rgb_diode_loop, RgbDiode
        print(f"\nStarting {settings['id']} loop\n")
        rgb_diode = RgbDiode(settings['id'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        rgb_diode.setup_rgb_diode()
        rgb_diode_thread = threading.Thread(target=run_rgb_diode_loop, args=(rgb_diode, settings, 0.5, rgb_diode_callback, stop_event, rgb_power_on_event, red_event, green_event, blue_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} loop started\n")