import time
import random
from pynput import keyboard

def on_press(key, callback, id):
    key = str(key).replace("'", "")
    if key == "r":
        callback("red", id)
    elif key == "b":
        callback("blue", id) 
    elif key == "g":
        callback("green", id) 
    elif key == "w":
        callback("white", id)
    elif key == "o":
        callback("off", id)


def run_rgb_diode_simulator(id, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, id))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 

