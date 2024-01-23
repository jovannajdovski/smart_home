
import threading
import time
from datetime import datetime
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.alarm import Alarm
from utils.counter import Counter
from simulators.buzzer import run_buzzer_simulator, panic

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 5
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None
alarm=None
buzzer_actuator=None

def buzzer_callback(code, settings):    
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"BUZZER ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"BUZZER: {code} activated"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': code,
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()
    


def run_buzzer(settings, _totalPersons, _alarm, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    global alarm
    if alarm is None:
        alarm=_alarm
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        buzzer_thread = threading.Thread(target = run_buzzer_simulator, args=(settings, 0.1, buzzer_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.buzzer import run_buzzer_loop, Buzzer
        print(f"\nStarting {settings['id']} loop\n")
        buzzer = Buzzer(settings['id'], settings['pin'], settings['pitch'])
        buzzer.setup_buzzer()
        global buzzer_actuator
        buzzer_actuator=buzzer
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, settings, 3, 0.5, buzzer_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"\n{settings['id']} loop started\n")

def invoke_alarm():
    def alarm_thread():
        if buzzer_actuator is not None:
            buzzer_actuator.panic(10, 0.5)
        else:
            panic()
        send_alarm_mqtt("PANIC")

    # Create a new thread and start it
    alarm_thread = threading.Thread(target=alarm_thread)
    alarm_thread.start()

def check_password(pin):
    print('check password: ', pin)
    if alarm.active and pin==alarm.pin:
        alarm.active=False
        send_alarm_mqtt("Inactive")
    elif alarm.active and pin!=alarm.pin:
        invoke_alarm()
    elif not alarm.active and pin==alarm.pin:
        time.sleep(10)
        alarm.active=True
        send_alarm_mqtt("Active")   

def send_alarm_mqtt(value):
    payload={
             'measurement': "ALARM",
             'value': value,
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        batch.append(("ALARM", json.dumps(payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=1:
        publish_event.set()