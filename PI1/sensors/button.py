import RPi.GPIO as GPIO
import time

class Button(object):
    def __init__(self, id, pin):
        self.id=id
        self.pin=pin
    
    def setup_button(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def run_button_loop(button, delay, callback, stop_event):
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback = callback, bouncetime = 100)
    
    while not stop_event.is_set():
        time.sleep(delay)
    
    GPIO.cleanup()