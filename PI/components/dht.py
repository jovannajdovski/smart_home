
from simulators.dht import run_dht_simulator
import threading
import time
from datetime import datetime
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter
from components.lcd import display_condition

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 5
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None

def dht_callback(humidity, temperature, code, settings):
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #            f"DHT ID: {settings['id']}",
    #            f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #            f"Code: {code}",
    #            f"Humidity: {humidity}%",
    #            f"Temperature: {temperature}°C"
    #            )

    display_condition_on_LCD(settings, humidity, temperature)

    humidity_payload={
             'measurement': 'Humidity',
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': float(humidity),
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    temperature_payload={
             'measurement': 'Temperature',
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': float(temperature),
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        
        batch.append((settings['type'], json.dumps(humidity_payload), 0, True))
        batch.append((settings['type'], json.dumps(temperature_payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()


def run_dht(settings, _totalPersons, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        dht_thread = threading.Thread(target = run_dht_simulator, args=(settings, 2, dht_callback, stop_event))
        dht_thread.start()
        threads.append(dht_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.dht import run_dht_loop, DHT
        print(f"\nStarting {settings['id']} loop\n")
        dht = DHT(settings['id'], settings['pin'])
        dht_thread = threading.Thread(target=run_dht_loop, args=(dht, settings, 2, dht_callback, stop_event))
        dht_thread.start()
        threads.append(dht_thread)
        print(f"\n{settings['id']} loop started\n")

def display_condition_on_LCD(settings, humidity, temperature):
    if settings['id'] == 'GDHT':
        display_condition(humidity, temperature, settings)