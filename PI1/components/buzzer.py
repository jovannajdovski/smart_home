
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def buzzer_callback(code, settings):      
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"BUZZER ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"BUZZER: {code} activated"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': code
        }
    


def run_buzzer(settings, threads, stop_event):
        # threads.append(publisher_thread)
        if settings['simulated']:
            from simulators.buzzer import run_buzzer_simulator
            print(f"\nStarting {settings['id']} simulator\n")
            buzzer_thread = threading.Thread(target = run_buzzer_simulator, args=(settings, 0.1, buzzer_callback, stop_event))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from actuators.buzzer import run_buzzer_loop, Buzzer
            print(f"\nStarting {settings['id']} loop\n")
            buzzer = Buzzer(settings['id'], settings['pin'], settings['pitch'])
            buzzer.setup_buzzer()
            buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, settings, 3, 0.5, buzzer_callback, stop_event))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"\n{settings['id']} loop started\n")