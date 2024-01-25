import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

class Button(object):
    def __init__(self, id, pin):
        self.id=id
        self.pin=pin
    
    def setup_button(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def run_button_loop(button, settings, delay, last_released_time, callback, panic_stop_event, stop_event):
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback=lambda x: callback(settings), bouncetime = 100)
    
    while not stop_event.is_set():
        if GPIO.input(button.pin) != GPIO.HIGH:
            time_now=datetime.now()
            if time_now-last_released_time[settings['id']]>timedelta(seconds=5):
                panic_stop_event.set()
            last_released_time[settings['id']] = datetime.now()
            print('setovo zadnje vreme')
        else:
            print('nije setovo vreme')
        time.sleep(delay)
    
    GPIO.cleanup()