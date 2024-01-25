import time
import random
# from pynput import keyboard

def beep():
    try:
        import winsound
    except ImportError:
        import os
        def _beep():
            pass
            # os.system('beep')
    else:
        def _beep():
            winsound.Beep(1000, 1000)

    _beep()

def alarm():
    for _ in range(3):
        beep()
        time.sleep(1)
    
    
def panic(callback, settings, reason, panic_stop_event):
    callback("PANIC", settings, reason)
    while True:
        if panic_stop_event.is_set():
            break
        beep()

def on_press(key, callback, settings):
    key = str(key).replace("'", "")
    if key == "a":
        alarm()
        callback("ALARM", settings, "Alarm")
    elif key == "z":
        beep()
        callback("BUZZ", settings, "Buzz")

def run_buzzer_simulator(settings, delay, callback, stop_event, alarm_clock_event):
    # listener = keyboard.Listener(on_press=lambda key: on_press(key, callback, settings))
    # listener.start()

    clock_alarm_started = False
    while not stop_event.is_set():
        if settings["id"] == "BB":
            if alarm_clock_event.is_set() and not clock_alarm_started:
                callback("CLOCK ALARM STARTED", settings)
                clock_alarm_started = True
            elif not alarm_clock_event.is_set() and clock_alarm_started:
                callback("CLOCK ALARM TURNED OFF", settings)
                clock_alarm_started = False
        time.sleep(delay)

    # listener.stop() 
