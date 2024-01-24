import RPi.GPIO as GPIO
import time
import random

GREEN = "\033[32m"
RED = "\033[31m"
WHITE = "\033[47;30m"
BLUE = "\033[34m"
RESET = "\033[0m"

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
    


def run_rgb_diode_loop(rgb_diode, settings, delay, callback, stop_event, rgb_power_on_event, red_event, green_event, blue_event):
    
    power_on = False
    while not stop_event.is_set():
        if rgb_power_on_event.is_set() and not power_on:
            rgb_diode.turn_red()
            callback("", settings, "RGB TURNED ON")
            power_on = True
        elif not rgb_power_on_event.is_set() and power_on:
            rgb_diode.turn_off()
            callback("", settings, "RGB TURNED OFF")
            power_on = False

        if red_event.is_set():
            if power_on:
                rgb_diode.turn_red()
                callback(RED + "red" + RESET, settings)
            red_event.clear()
        
        if green_event.is_set():
            if power_on:
                rgb_diode.turn_green()
                callback(GREEN + "green" + RESET, settings)
            green_event.clear()

        if blue_event.is_set():
            if power_on:
                rgb_diode.turn_blue()
                callback(BLUE + "blue" + RESET, settings)
            blue_event.clear()
        time.sleep(delay)
