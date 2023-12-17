import time
import random
from pynput import keyboard

def beep():
    try:
        import winsound
    except ImportError:
        import os
        def _beep():
            os.system('beep')
    else:
        def _beep():
            winsound.Beep(1000, 1000)

    _beep()

def alarm():
    for _ in range(3):
        beep()
        time.sleep(1)

def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "a":
        alarm()
        callback("ALARM", settings)
    elif key == "z":
        beep()
        callback("BUZZ", settings)

def run_buzzer_simulator(settings, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 
