import time
import random
from pynput import keyboard

GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[47;30m"
BLUE = "\033[34m"
RESET = "\033[0m"


def on_press(key, callback, id):
    key = str(key).replace("'", "")
    if key == "r":
        callback(RED + "red" + RESET, id)
    # elif key == "b":
    #     callback(BLUE + "blue" + RESET, id) 
    elif key == "g":
        callback(GREEN + "green" + RESET, id) 
    elif key == "w":
        callback(WHITE + "white" + RESET, id)
    elif key == "o":
        callback("off", id)


def run_rgb_diode_simulator(id, delay, callback, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, id))
    listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    listener.stop() 

