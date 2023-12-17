from simulators.uds import run_uds_simulator
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def uds_callback(distance, id):
    if distance is not None:         
        t = time.localtime()
        safe_print("\n"+"="*20,
                   f"UDS ID: {id}",
                   f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                   f"Distance: {distance} cm"
                   )
    # else Measurement timed out


def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            uds_thread = threading.Thread(target = run_uds_simulator, args=(settings['id'], 1, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from sensors.uds import run_uds_loop, UDS
            print(f"\nStarting {settings['id']} loop\n")
            uds = UDS(settings['id'], settings['trig_pin'], settings['echo_pin'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 1, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print(f"\n{settings['id']} loop started\n")