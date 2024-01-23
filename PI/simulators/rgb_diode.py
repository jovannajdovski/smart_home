import time
import random
from pynput import keyboard

GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[47;30m"
BLUE = "\033[34m"
RESET = "\033[0m"


def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "r":
        callback("red", settings)
    elif key == "b":
        callback("blue", settings) 
    elif key == "g":
        callback("green", settings) 
    elif key == "w":
        callback("white", settings)
    elif key == "o":
        callback("off", settings)


def run_rgb_diode_simulator(settings, delay, callback, stop_event):
    
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 

