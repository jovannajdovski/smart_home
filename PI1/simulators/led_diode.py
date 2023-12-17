import time
import random
from pynput import keyboard

RED = "\033[31m"
RESET = "\033[0m"

def on_press(key, callback, id):
    key = str(key).replace("'", "")
    if key == "1":
        callback("on", id)
    elif key == "0":
        callback("off", id)


def run_led_diode_simulator(id, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, id))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 

