from simulators.pir import run_pir_simulator
import threading
import time
from utils.safe_print import safe_print  

def pir_callback(motion_detected, id):
    if motion_detected:         
        t = time.localtime()
        safe_print("\n"+"="*20,
                   f"PIR ID: {id}",
                   f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                   "Motion detected"
                   )
    # else:
    #     t = time.localtime()
    #     safe_print("\n"+"="*20,
    #                f"PIR ID: {id}",
    #                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #                "No motion detected"
    #                )


def run_pir(settings, threads, stop_event):
        if settings['simulated']:
            print(f"\nStarting {settings['id']} sumilator\n")
            pir_thread = threading.Thread(target = run_pir_simulator, args=(settings['id'], 0.1, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print(f"\n{settings['id']} sumilator started\n")
        else:
            from sensors.pir import run_pir_loop, PIR
            print(f"\nStarting {settings['id']} loop\n")
            pir = PIR(settings['id'], settings['pin'])
            pir.setup_pir()
            pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 0.1, pir_callback, stop_event))
            pir_thread.start()
            threads.append(pir_thread)
            print(f"\n{settings['id']} loop started\n")