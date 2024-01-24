import time
import random
# from pynput import keyboard

GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[47;30m"
BLUE = "\033[34m"
RESET = "\033[0m"


def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "r":
        callback(RED + "red" + RESET, settings)
    elif key == "b":
        callback(BLUE + "blue" + RESET, settings) 
    elif key == "g":
        callback(GREEN + "green" + RESET, settings) 
    elif key == "w":
        callback(WHITE + "white" + RESET, settings)
    elif key == "o":
        callback("off", settings)


def run_rgb_diode_simulator(settings, delay, callback, stop_event, rgb_power_on_event, red_event, green_event, blue_event):
    
    # listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    # listener.start()
    power_on = False
    while not stop_event.is_set():
        if rgb_power_on_event.is_set() and not power_on:
            callback("", settings, "RGB TURNED ON")
            power_on = True
        elif not rgb_power_on_event.is_set() and power_on:
            callback("", settings, "RGB TURNED OFF")
            power_on = False

        if red_event.is_set():
            if power_on:
                callback(RED + "red" + RESET, settings)
            red_event.clear()
        
        if green_event.is_set():
            if power_on:
                callback(GREEN + "green" + RESET, settings)
            green_event.clear()

        if blue_event.is_set():
            if power_on:
                callback(BLUE + "blue" + RESET, settings)
            blue_event.clear()
        time.sleep(delay)

    # listener.stop() 

