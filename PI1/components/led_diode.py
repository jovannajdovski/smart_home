
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def led_diode_callback(state, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"LED DIODE ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"LED DIODE: {state}"
                )


def run_led_diode(settings, threads, stop_event):
    if settings['simulated']:
        from simulators.led_diode import run_led_diode_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        led_diode_thread = threading.Thread(target = run_led_diode_simulator, args=(settings['id'], 5, led_diode_callback, stop_event))
        led_diode_thread.start()
        threads.append(led_diode_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.led_diode import run_led_diode_loop, LedDiode
        print(f"\nStarting {settings['id']} loop\n")
        led_diode = LedDiode(settings['id'], settings['pin'])
        led_diode.setup_rgb_diode()
        led_diode_thread = threading.Thread(target=run_led_diode_loop, args=(led_diode, 5, led_diode_callback, stop_event))
        led_diode_thread.start()
        threads.append(led_diode_thread)
        print(f"\n{settings['id']} loop started\n")