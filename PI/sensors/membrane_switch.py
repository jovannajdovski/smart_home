import RPi.GPIO as GPIO
import time

class MembraneSwitch(object):
    def __init__(self, id, r1_pin, r2_pin, r3_pin, r4_pin, c1_pin, c2_pin, c3_pin, c4_pin):
        self.id=id
        self.r1_pin=r1_pin
        self.r2_pin=r2_pin
        self.r3_pin=r3_pin
        self.r4_pin=r4_pin
        self.c1_pin=c1_pin
        self.c2_pin=c2_pin
        self.c3_pin=c3_pin
        self.c4_pin=c4_pin

    def setup_membrane_switch(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.r1_pin, GPIO.OUT)
        GPIO.setup(self.r2_pin, GPIO.OUT)
        GPIO.setup(self.r3_pin, GPIO.OUT)
        GPIO.setup(self.r4_pin, GPIO.OUT)
        GPIO.setup(self.c1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c4_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def detect_line_press(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.c1_pin) == 1):
            return characters[0]
        if(GPIO.input(self.c2_pin) == 1):
            return characters[1]
        if(GPIO.input(self.c3_pin) == 1):
            return characters[2]
        if(GPIO.input(self.c4_pin) == 1):
            return characters[3]
        GPIO.output(line, GPIO.LOW)


def run_membrane_switch_loop(membrane_switch, settings, delay, callback, stop_event):
    while True:
        pressed_key = membrane_switch.detect_line_press(membrane_switch.r1_pin, ["1","2","3","A"])
        if pressed_key: 
            callback(pressed_key, settings,0)
        pressed_key = membrane_switch.detect_line_press(membrane_switch.r2_pin, ["4","5","6","B"])
        if pressed_key: 
            callback(pressed_key,settings,0)
        pressed_key = membrane_switch.detect_line_press(membrane_switch.r3_pin, ["7","8","9","C"])
        if pressed_key: 
            callback(pressed_key,settings,0)
        pressed_key = membrane_switch.detect_line_press(membrane_switch.r4_pin, ["*","0","#","D"])
        if pressed_key: 
            callback(pressed_key,settings,0)

        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)