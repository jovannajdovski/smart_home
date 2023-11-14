import RPI.GPIO as GPIO
import time
import random

class RgbDiode(object):
    def __init__(self, id, red_pin, green_pin, blue_pin):
        self.id=id
        self.red_pin=red_pin
        self.green_pin=green_pin
        self.blue_pin=blue_pin
    
    def setup_rgb_diode(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red_pin,GPIO.OUT)
        GPIO.setup(self.green_pin,GPIO.OUT)
        GPIO.setup(self.blue_pin,GPIO.OUT)

    def turn_white(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)
    
    def turn_blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)
    
    def turn_red(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def turn_green(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)
    
    def turn_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
    


def run_rgb_diode_loop(rgb_diode, delay, callback, stop_event):
    
    while not stop_event.is_set():
        rnd = random.random()
        if rnd < 0.2:
            rgb_diode.turn_red()
            callback("red", rgb_diode.id)
        elif rnd < 0.4:
            rgb_diode.turn_blue()
            callback("blue", rgb_diode.id) 
        elif rnd < 0.6:
            rgb_diode.turn_green()
            callback("green", rgb_diode.id) 
        elif rnd < 0.8:
            rgb_diode.turn_white()
            callback("white", rgb_diode.id)
        else:
            rgb_diode.turn_off()
            callback("off", rgb_diode.id)
        time.sleep(delay)
