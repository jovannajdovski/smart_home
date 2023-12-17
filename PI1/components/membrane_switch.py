from simulators.membrane_switch import run_membrane_switch_simulator
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def membrane_switch_callback(key, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"MEMBRANE SWITCH ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"KEY PRESSED: {key}"
                )
    


def run_membrane_switch(settings, threads, stop_event):
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        membrane_switch_thread = threading.Thread(target = run_membrane_switch_simulator, args=(settings['id'], 1, membrane_switch_callback, stop_event))
        membrane_switch_thread.start()
        threads.append(membrane_switch_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.membrane_switch import run_membrane_switch_loop, MembraneSwitch
        print(f"\nStarting {settings['id']} loop\n")
        membrane_switch = MembraneSwitch(settings['id'], settings['r1_pin'], settings['r2_pin'], settings['r3_pin'], settings['r4_pin'],
                                          settings['c1_pin'], settings['c2_pin'] ,settings['c3_pin'], settings['c4_pin'])
        membrane_switch.setup_membrane_switch()
        membrane_switch_thread = threading.Thread(target=run_membrane_switch_loop, args=(membrane_switch, 0.1, membrane_switch_callback, stop_event))
        membrane_switch_thread.start()
        threads.append(membrane_switch_thread)
        print(f"\n{settings['id']} loop started\n")