from simulators.pir import run_pir_simulator
import threading
import time
import json
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

def pir_callback(motion_detected, settings):
    if motion_detected:         
        t = time.localtime()
        safe_print("\n"+"="*20,
                   f"PIR ID: {settings['id']}",
                   f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                   "Motion detected"
                   )
        payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': 'DETECTED'
        }
        with counter_lock:
            batch.append((settings['type'], json.dumps(payload), 0, True))
            publish_data_counter.increment()
        if publish_data_counter.value>=publish_data_limit:
            
            publish_event.set()


def run_pir(settings, threads, stop_event):
        print(settings['simulated'])
        threads.append(publisher_thread)
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            pir_thread = threading.Thread(target = run_pir_simulator, args=(settings, 0.1, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from sensors.pir import run_pir_loop, PIR
            print(f"\nStarting {settings['id']} loop\n")
            pir = PIR(settings['id'], settings['pin'])
            pir.setup_pir()
            pir_thread = threading.Thread(target=run_pir_loop, args=(pir, settings, 0.1, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print(f"\n{settings['id']} loop started\n")