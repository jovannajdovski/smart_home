
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def lcd_callback(text, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"LCD ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"Text on LCD display: {text}"
                )


def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        from simulators.lcd import run_lcd_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        lcd_thread = threading.Thread(target = run_lcd_simulator, args=(settings['id'], 10, lcd_callback, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.lcd.LCD import LCD, run_lcd_loop
        print(f"\nStarting {settings['id']} loop\n")
        lcd = LCD(settings['id'], settings['pin_rs'], settings['pin_e'], settings['pin_db1'], settings['pin_db2'], settings['pin_db3'], settings['pin_db4'])
        lcd.setup_lcd()
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, 5, lcd_callback, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"\n{settings['id']} loop started\n")

