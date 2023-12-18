
import threading
import time
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter


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
             'value': text
        }


def run_lcd(settings, threads, stop_event):
    # threads.append(publisher_thread)
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
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, settings, 5, lcd_callback, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"\n{settings['id']} loop started\n")

