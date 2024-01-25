
import threading
import time
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter
import datetime

alarm_clock_event = None
alarm_time = ""

def stop_clock_alarm():
    global alarm_clock_event
    alarm_clock_event.clear()

def change_clock_alarm(h,m):
    global alarm_time
    alarm_time = str(h) + ":" + str(m)

# def start_clock_alarm():
#     global alarm_clock_event
#     alarm_clock_event.set()

def run_clock_alarm(settings, threads, stop_event, _alarm_clock_event):

    global alarm_clock_event, alarm_time
    alarm_clock_event = _alarm_clock_event
    alarm_time = settings["time"]

    clock_alarm_thread = threading.Thread(target = run_clock_alarm_cron, args=(0.1, stop_event, alarm_clock_event))
    clock_alarm_thread.start()
    threads.append(clock_alarm_thread)
    print(f"\nClock alarm set\n")


def run_clock_alarm_cron(delay, stop_event, alarm_clock_event):
    global alarm_time
    while not stop_event.is_set():
        ntime = time.ctime()[11:13] + ":" + time.ctime()[14:16]
        # current_time = datetime.now()

        # current_hour = current_time.hour
        # current_minute = current_time.minute

        if alarm_time == ntime:
            alarm_clock_event.set()
            time.sleep(60)
        time.sleep(delay)