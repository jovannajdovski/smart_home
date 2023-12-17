from simulators.button import run_button_simulator
import threading
import time
from utils.safe_print import safe_print  
from utils.mqtt import publish_message 

def button_callback(id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"MEMBRANE SWITCH ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"BUTTON PRESSED"
                )


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        button_thread = threading.Thread(target = run_button_simulator, args=(settings['id'], 1, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.button import run_button_loop, Button
        print(f"\nStarting {settings['id']} loop\n")
        button = Button(settings['id'], settings['pin'])
        button.setup_button()
        button_thread = threading.Thread(target=run_button_loop, args=(button, 0.1, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"\n{settings['id']} loop started\n")