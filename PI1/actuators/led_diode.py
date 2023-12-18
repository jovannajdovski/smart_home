import RPi.GPIO as GPIO
import time
import random

class LedDiode(object):
    def __init__(self, id, pin):
        self.id=id
        self.pin = pin
    
    def setup_led_diode(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
    
    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)


def run_led_diode_loop(led_diode, settings, delay, callback, stop_event):
    
    while not stop_event.is_set():
        rnd = random.random()
        if rnd < 0.2:
            led_diode.turn_on()
            callback("on", settings)
        else:
            led_diode.turn_off()
            callback("off", settings)
        time.sleep(delay)
