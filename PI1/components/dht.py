

from simulators.dht import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code, id):
    t = time.localtime()
    print("="*20)
    print(f"DHT ID: {id}")
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print(f"Starting {settings['id']} sumilator")
            dht_thread = threading.Thread(target = run_dht_simulator, args=(settings['id'], 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"{settings['id']} sumilator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print(f"Starting {settings['id']} loop")
            dht = DHT(settings['id'], settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"{settings['id']} loop started")
