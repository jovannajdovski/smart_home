import time
import random
from pynput import keyboard

def on_press(key, callback, id):
    key = str(key).replace("'", "")
    if key == "a":
        callback("ALARM", id)
    elif key == "b":
        callback("BUZZ", id)

def run_buzzer_simulator(id, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, id))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 
