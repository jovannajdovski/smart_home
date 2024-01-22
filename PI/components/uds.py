from simulators.uds import run_uds_simulator
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
totalPersons=None
last_distances={}


def uds_callback(distance, settings):
    global batch, publish_data_counter, publish_data_limit, publish_event
    if distance is not None:         
        if settings['id'] in last_distances:
            last_distances[settings['id']][0]=last_distances[settings['id']][1]
            last_distances[settings['id']][1]=distance
        else:
            last_distances[settings['id']]=[None, distance]
            
        t = time.localtime()
        # safe_print("\n"+"="*20,
        #            f"UDS ID: {settings['id']}",
        #            f"Timestamp: {time.strftime('%H:%M:%S', t)}",
        #            f"Distance: {distance} cm"
        #            )
        payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': float(distance)
        }
        with counter_lock:
            batch.append((settings['type'], json.dumps(payload), 0, True))
            publish_data_counter.increment()
        if publish_data_counter.value>=publish_data_limit:
            
            publish_event.set()
    


def run_uds(settings, _totalPersons, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        uds_thread = threading.Thread(target = run_uds_simulator, args=(settings, 1, uds_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.uds import run_uds_loop, UDS
        print(f"\nStarting {settings['id']} loop\n")
        uds = UDS(settings['id'], settings['trig_pin'], settings['echo_pin'])
        uds_thread = threading.Thread(target=run_uds_loop, args=(uds, settings, 1, uds_callback, stop_event))
        uds_thread.start()
        threads.append(uds_thread)
        print(f"\n{settings['id']} loop started\n")