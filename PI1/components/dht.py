
from simulators.dht import run_dht_simulator
import threading
import time
from utils.safe_print import safe_print   

def dht_callback(humidity, temperature, code, id):
    t = time.localtime()
    safe_print("\n"+"="*20,
               f"DHT ID: {id}",
               f"Timestamp: {time.strftime('%H:%M:%S', t)}",
               f"Code: {code}",
               f"Humidity: {humidity}%",
               f"Temperature: {temperature}°C"
               )


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            dht_thread = threading.Thread(target = run_dht_simulator, args=(settings['id'], 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from sensors.dht import run_dht_loop, DHT
            print(f"\nStarting {settings['id']} loop\n")
            dht = DHT(settings['id'], settings['pin'])
            dht_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
            dht_thread.start()
            threads.append(dht_thread)
            print(f"\n{settings['id']} loop started\n")
