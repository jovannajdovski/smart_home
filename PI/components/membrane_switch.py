from simulators.membrane_switch import run_membrane_switch_simulator
import threading
import time
from datetime import timedelta, datetime
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter
from components.buzzer import check_password

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 5
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None
last_four=[None, None, None, None]
last_updated=None

def membrane_switch_callback(key, settings):      
    t = datetime.now()
    # safe_print("\n"+"="*20,
    #             f"MEMBRANE SWITCH ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"KEY PRESSED: {key}"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': key
        }
    global last_updated, last_four
    
    if last_updated is not None and t-last_updated>timedelta(seconds=10):
        last_four=[None,None,None,None]
    
    last_updated=t
    
    
    if None in last_four:
        last_four=last_four[1:] + [key]
    if None not in last_four:
        check_password(''.join(last_four))
        last_four=[None,None,None,None]
    
    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()



def run_membrane_switch(settings, _totalPersons, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        membrane_switch_thread = threading.Thread(target = run_membrane_switch_simulator, args=(settings, 1, membrane_switch_callback, stop_event))
        membrane_switch_thread.start()
        threads.append(membrane_switch_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.membrane_switch import run_membrane_switch_loop, MembraneSwitch
        print(f"\nStarting {settings['id']} loop\n")
        membrane_switch = MembraneSwitch(settings['id'], settings['r1_pin'], settings['r2_pin'], settings['r3_pin'], settings['r4_pin'],
                                          settings['c1_pin'], settings['c2_pin'] ,settings['c3_pin'], settings['c4_pin'])
        membrane_switch.setup_membrane_switch()
        membrane_switch_thread = threading.Thread(target=run_membrane_switch_loop, args=(membrane_switch, settings, 0.1, membrane_switch_callback, stop_event))
        membrane_switch_thread.start()
        threads.append(membrane_switch_thread)
        print(f"\n{settings['id']} loop started\n")