import RPI.GPIO as GPIO
import time
import random


class Buzzer(object):
    def __init__(self, id, pin, pitch):
        self.id = id
        self.pin = pin
        self.pitch = pitch

    def setup_buzzer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz(self, duration):
        period = 1.0 / self.pitch
        delay = period / 2
        cycles = int(duration * self.pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

    def alarm(self, buzz_duration, alarm_duration):
        for _ in range(alarm_duration//(buzz_duration*2)):
            self.buzz(buzz_duration)
            time.sleep(buzz_duration)

def run_buzzer_loop(buzzer, delay, duration, callback, stop_event):
    while True:
        # :TODO add some logic
        rnd = random.random()
        if rnd < 0.05:
            buzzer.alarm(duration, 60*duration)
            callback("ALARM", buzzer.id)
        elif rnd < 0.1:
            buzzer.buzz(duration)
            callback("BUZZ", buzzer.id)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)