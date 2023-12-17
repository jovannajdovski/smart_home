from simulators.button import run_button_simulator
import threading
import time
import json
from utils.safe_print import safe_print  
from utils.mqtt import publish_message
from utils.counter import Counter

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 1
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start() 

def button_callback(settings):      
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"BUTTON ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"BUTTON PRESSED"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': 'PRESSED'
        }
    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()


def run_button(settings, threads, stop_event):
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        button_thread = threading.Thread(target = run_button_simulator, args=(settings, 1, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.button import run_button_loop, Button
        print(f"\nStarting {settings['id']} loop\n")
        button = Button(settings['id'], settings['pin'])
        button.setup_button()
        button_thread = threading.Thread(target=run_button_loop, args=(button, settings, 0.1, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"\n{settings['id']} loop started\n")