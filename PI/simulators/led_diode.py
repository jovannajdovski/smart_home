import time
import random
# from pynput import keyboard

def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "1":
        callback("on", settings)
    elif key == "0":
        callback("off", settings)


def run_led_diode_simulator(settings, delay, callback, stop_event):
    # listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    # listener.start()

    while not stop_event.is_set():
        time.sleep(delay)

    # listener.stop() 

