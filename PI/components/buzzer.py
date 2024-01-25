
import threading
import time
from datetime import datetime, timedelta
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
alarm_clock_event = None
buzzer_settings=[]
panic_stop_event=None
last_tried_pin=["",0]

def buzzer_callback(code, settings, reason):    
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"BUZZER ID: {settings['id']}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"BUZZER: {code} activated",
                f"REASON: {reason}"
                )
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
        batch.append((settings['type'], json.dumps(payload), 0, False))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()
    


def run_buzzer(settings, _totalPersons, _alarm, threads, _panic_stop_event, stop_event,  _alarm_clock_event=None):
    global totalPersons
    totalPersons=_totalPersons
    global panic_stop_event
    panic_stop_event=_panic_stop_event
    global alarm
    if alarm is None:
        alarm=_alarm
    threads.append(publisher_thread)

    global alarm_clock_event
    alarm_clock_event = _alarm_clock_event

    global buzzer_settings
    buzzer_settings.append(settings)

    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        buzzer_thread = threading.Thread(target = run_buzzer_simulator, args=(settings, 0.1, buzzer_callback, stop_event, alarm_clock_event))
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
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, settings, 3, 0.5, buzzer_callback, stop_event, alarm_clock_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"\n{settings['id']} loop started\n")

def invoke_alarm(reason):
    def alarm_thread_actuator(settings):
        buzzer_actuator.panic(10, 0.5, settings, buzzer_callback, reason)
        
    def alarm_thread_simulator(settings, panic_stop_event):
        panic(buzzer_callback,settings, reason, panic_stop_event)
        
        
    # Create a new thread and start it
    
    global panic_stop_event
    panic_stop_event.clear()
    if buzzer_actuator is not None:
        for settings in buzzer_settings:
            alarm_thread = threading.Thread(target=alarm_thread_actuator, args=(settings))
            alarm_thread.start()
        send_alarm_mqtt("PANIC")
    else:
        for settings in buzzer_settings:
            alarm_thread = threading.Thread(target=alarm_thread_simulator, args=(settings, panic_stop_event))
            alarm_thread.start()
        send_alarm_mqtt("PANIC")



def check_enter_house(time_now):
    time.sleep(10)
    if alarm.active and last_tried_pin[0]!=alarm.pin:
        invoke_alarm("WRONG PIN")
    elif last_tried_pin[1]-time_now>timedelta(seconds=10) or time_now-last_tried_pin[1]>timedelta(seconds=0):
        invoke_alarm("PIN NOT DETECTED")

def check_password(pin):
    print('check password: ', pin)
    global last_tried_pin
    last_tried_pin=[pin,datetime.now()]
    if alarm.active and pin==alarm.pin:
        alarm.active=False
        panic_stop_event.set()
        print('active->inactive')
        send_alarm_mqtt("Inactive")
    elif alarm.active and pin!=alarm.pin:
        pass
        # invoke_alarm("WRONG PIN")
    elif not alarm.active and pin==alarm.pin:
        panic_stop_event.set()
        time.sleep(10)
        print('inactive->active')
        alarm.active=True
        send_alarm_mqtt("Active")   

def send_alarm_mqtt(value):
    payload={
             'measurement': "ALARM",
             'value': value,
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        batch.append(("ALARM", json.dumps(payload), 0, False))
        publish_data_counter.increment()
    if publish_data_counter.value>=1:
        publish_event.set()