import RPi.GPIO as GPIO
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
    
    def panic(self, buzz_duration, panic_duration):
        for _ in range(panic_duration//(buzz_duration*2)):
            self.buzz(buzz_duration)

    def turn_on(self):
        GPIO.output(self.pin, True)

    def turn_off(self):
        GPIO.output(self.pin, False)

def run_buzzer_loop(buzzer, settings, delay, duration, callback, stop_event, alarm_clock_event):
    clock_alarm_started = False
    while True:
        if settings["id"] == "BB":
            if alarm_clock_event.is_set() and not clock_alarm_started:
                clock_alarm_started = True
                buzzer.turn_on()
                callback("CLOCK ALARM STARTED", settings)
            elif not alarm_clock_event.is_set() and clock_alarm_started:
                clock_alarm_started = False
                buzzer.turn_off()
                callback("CLOCK ALARM TURNED OFF", settings)
        if stop_event.is_set():
            buzzer.turn_off()
            GPIO.cleanup()
            break
        time.sleep(delay)