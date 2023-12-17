import time
import random
from pynput import keyboard

def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "a":
        callback("ALARM", settings)
    elif key == "b":
        callback("BUZZ", settings)

def run_buzzer_simulator(settings, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 
