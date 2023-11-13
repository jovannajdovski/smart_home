from simulators.buzzer import run_buzzer_simulator
import threading
import time
from utils.safe_print import safe_print  

def buzzer_callback(code, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"BUZZER ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"BUZZER: {code} activated"
                )


def run_buzzer(settings, threads, stop_event):
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            buzzer_thread = threading.Thread(target = run_buzzer_simulator, args=(settings['id'], 0.1, buzzer_callback, stop_event))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from actuators.buzzer import run_buzzer_loop, Buzzer
            print(f"\nStarting {settings['id']} loop\n")
            buzzer = Buzzer(settings['id'], settings['pin'], settings['pitch'])
            buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, 3, 0.5, buzzer_callback, stop_event))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"\n{settings['id']} loop started\n")