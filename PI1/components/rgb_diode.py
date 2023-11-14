from simulators.rgb_diode import run_rgb_diode_simulator
import threading
import time
from utils.safe_print import safe_print  

def rgb_diode_callback(color, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"RGB DIODE ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"RGB DIODE: Current color {color}"
                )


def run_rgb_diode(settings, threads, stop_event):
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        rgb_diode_thread = threading.Thread(target = run_rgb_diode_simulator, args=(settings['id'], 0.5, rgb_diode_callback, stop_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.rgb_diode import run_rgb_diode_loop, RgbDiode
        print(f"\nStarting {settings['id']} loop\n")
        rgb_diode = RgbDiode(settings['id'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        rgb_diode.setup_rgb_diode()
        rgb_diode_thread = threading.Thread(target=run_rgb_diode_loop, args=(rgb_diode, 0.5, rgb_diode_callback, stop_event))
        rgb_diode_thread.start()
        threads.append(rgb_diode_thread)
        print(f"\n{settings['id']} loop started\n")