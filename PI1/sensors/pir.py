import RPi.GPIO as GPIO
import time

class PIR(object):
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin

    def setup_pir(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        # GPIO.add_event_detect(self.pin, GPIO.RISING, callback=motion_detected)
        # GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=no_motion)

    def detect_motion(self):
        motion_detected = GPIO.input(self.pin)
        return motion_detected

def run_pir_loop(pir, delay, callback, stop_event):
    while True:
        motion_detected = pir.detect_motion()
        callback(motion_detected, pir.id)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)