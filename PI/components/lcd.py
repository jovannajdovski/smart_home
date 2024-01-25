
import threading
import time
from datetime import datetime
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 1
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None

totalPersons=None
lcd_display = None

_settings = None

def lcd_callback(text, settings):    
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #             f"LCD ID: {settings['id']}",
    #             f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #             f"Text on LCD display: {text}"
    #             )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': text,
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, False))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()


def run_lcd(settings, _totalPersons, threads, stop_event):
    global totalPersons, _settings
    _settings = settings
    totalPersons=_totalPersons
    #print("jjj")
    threads.append(publisher_thread)
    if settings['simulated']:
        from simulators.lcd import run_lcd_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        lcd_thread = threading.Thread(target = run_lcd_simulator, args=(settings, 10, lcd_callback, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.lcd.LCD import LCD, run_lcd_loop
        print(f"\nStarting {settings['id']} loop\n")
        lcd = LCD(settings['id'], settings['pin_rs'], settings['pin_e'], settings['pin_db1'], settings['pin_db2'], settings['pin_db3'], settings['pin_db4'])
        lcd.setup_lcd()

        global lcd_display
        lcd_display = lcd

        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, settings, 5, lcd_callback, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"\n{settings['id']} loop started\n")


def display_condition(humidity, temperature):
    global _settings
    def display_thread():
        global lcd_display
        if lcd_display is not None:
            lcd_display.display_cond(humidity, temperature)
        else:
            text = "Temperature: {}\nHumidity: {}".format(temperature, humidity)
            lcd_callback(text, _settings)

    display_condition_thread = threading.Thread(target=display_thread)
    display_condition_thread.start()