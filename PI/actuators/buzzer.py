import RPi.GPIO as GPIO
import time
import random
import threading
from actuators.music.notes import notes, load_song

song_stop_event = None

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
    
    def panic(self, buzz_duration, panic_duration, settings, callback, reason, panic_stop_event):
        # callback("PANIC", settings, reason)
        # for _ in range(panic_duration//(buzz_duration*2)):
        #     self.buzz(buzz_duration)
        # callback("STOPPED", settings, "STOP")

        callback("PANIC", settings, reason)
        while True:
            self.buzz(buzz_duration)
            if panic_stop_event.is_set():
                callback("STOPPED", settings, "STOP")
                break


    def turn_on(self):
        GPIO.output(self.pin, True)

    def turn_off(self):
        GPIO.output(self.pin, False)

    def buzz_note(self, pitch, duration):
        period = 1.0/pitch
        delay = period/2.0
        cycles = int(duration * pitch)

        for _ in range(cycles):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(delay)

def play_song(buzzer, song, song_stop_event, duration=1, pause=1):
    for note in song:
        if song_stop_event.is_set():
            break
        buzzer.buzz_note(notes[note['note']], note['duration'] * duration)
        if song_stop_event.is_set():
            break
        time.sleep(note['duration'] * duration*pause)

def run_buzzer_loop(buzzer, settings, delay, duration, callback, stop_event, alarm_clock_event):
    clock_alarm_started = False
    global song_stop_event
    song_stop_event = threading.Event()

    while True:
        if settings["id"] == "BB":
            if alarm_clock_event.is_set() and not clock_alarm_started:
                clock_alarm_started = True
                # buzzer.turn_on()
                song = load_song("zuta_kuca.json")
                song_stop_event.clear()
                song_thread = threading.Thread(target = play_song, args=(buzzer, song, song_stop_event))
                song_thread.start()

                callback("CLOCK ALARM STARTED", settings, "Na kraj sela zuta kuca")
            elif not alarm_clock_event.is_set() and clock_alarm_started:
                clock_alarm_started = False
                # buzzer.turn_off()
                song_stop_event.set()

                callback("CLOCK ALARM TURNED OFF", settings, "Gasi budilnik")
        if stop_event.is_set():
            buzzer.turn_off()
            GPIO.cleanup()
            break
        time.sleep(delay)