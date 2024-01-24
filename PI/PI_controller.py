
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.button import run_button
from components.rgb_diode import run_rgb_diode
from components.membrane_switch import run_membrane_switch
from components.gyro import run_gyro
from components.segment_display import run_4segment_display
from components.lcd import run_lcd
from components.led_diode import run_led_diode
from components.ir_receiver import run_ir_receiver
import time
from utils.mqtt import connect
from utils.alarm import Alarm
from utils.clock_alarm import run_clock_alarm

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

totalPersons=None

def run_pi1(settings, totalPersons, alarm, threads, stop_event):
    rdht1_settings = settings['RDHT1']
    rdht2_settings = settings['RDHT2']
    dus1_settings = settings['DUS1']
    dpir1_settings = settings['DPIR1']
    rpir1_settings = settings['RPIR1']
    rpir2_settings = settings['RPIR2']
    db_settings = settings['DB']
    ds1_settings = settings['DS1']
    dl_settings = settings['DL']
    dms_settings = settings['DMS']

    run_led_diode(dl_settings, totalPersons, threads, stop_event)
    run_dht(rdht1_settings, totalPersons, threads, stop_event)
    run_dht(rdht2_settings, totalPersons, threads, stop_event)
    run_uds(dus1_settings, totalPersons, threads, stop_event)
    run_pir(dpir1_settings, totalPersons, threads, stop_event)
    run_pir(rpir1_settings, totalPersons, threads, stop_event)
    run_pir(rpir2_settings, totalPersons, threads, stop_event)
    run_buzzer(db_settings, totalPersons, alarm, threads, stop_event)
    run_button(ds1_settings, totalPersons, threads, stop_event)
    run_membrane_switch(dms_settings, totalPersons, threads, stop_event)

def run_pi2(settings, totalPersons, threads, stop_event):
    ds2_settings = settings['DS2']
    dus2_settings = settings['DUS2']
    dpir2_settings = settings['DPIR2']
    gdht_settings = settings['GDHT']
    gsg_settings = settings['GSG']
    glcd_settings = settings['GLCD']
    rpir3_settings = settings['RPIR3']
    rdht3_settings = settings['RDHT3']

    run_button(ds2_settings, totalPersons, threads, stop_event)
    run_uds(dus2_settings, totalPersons, threads, stop_event)
    run_pir(dpir2_settings, totalPersons, threads, stop_event)
    run_dht(gdht_settings, totalPersons, threads, stop_event)
    run_gyro(gsg_settings, totalPersons, threads, stop_event)
    run_lcd(glcd_settings, totalPersons, threads, stop_event)
    run_pir(rpir3_settings, totalPersons, threads, stop_event)
    run_dht(rdht3_settings, totalPersons, threads, stop_event) 

def run_pi3(settings, totalPersons, alarm, threads, stop_event):

    clock_alarm_settings = settings["clockAlarm"]
    _alarm_clock_event = threading.Event()
    run_clock_alarm(clock_alarm_settings, threads, stop_event, _alarm_clock_event)

    rpir4_settings = settings['RPIR4']
    rdht4_settings = settings['RDHT4']
    b4sd_settings = settings['B4SD']
    brgb_settings = settings['BRGB']
    bb_settings = settings['BB']
    ir_receiver_settings = settings['BIR']

    rgb_power_on_event = threading.Event()
    red_event = threading.Event()
    green_event = threading.Event()
    blue_event = threading.Event()

    run_pir(rpir4_settings, totalPersons, threads, stop_event)
    run_dht(rdht4_settings, totalPersons, threads, stop_event) 
    run_4segment_display(b4sd_settings, totalPersons, threads, stop_event, _alarm_clock_event)
    run_rgb_diode(brgb_settings, totalPersons, threads, stop_event, rgb_power_on_event, red_event, green_event, blue_event)
    run_buzzer(bb_settings, totalPersons, alarm, threads, stop_event, _alarm_clock_event)
    run_ir_receiver(ir_receiver_settings, totalPersons, threads, stop_event, rgb_power_on_event, red_event, green_event, blue_event)

if __name__ == "__main__":
    settings = load_settings()
    stop_threads = []
    stop_event = threading.Event()
    totalPersons={'value':settings["totalPersons"], 'lock': threading.Lock()}

    try:
        alarm = Alarm(pin="0123", active=False)
        if settings["PI1"]["running"]:
            run_pi1(settings, totalPersons, alarm, stop_threads, stop_event)
        if settings["PI2"]["running"]:
            run_pi2(settings, totalPersons, stop_threads, stop_event)
        if settings["PI3"]["running"]:
            run_pi3(settings, totalPersons, alarm, stop_threads, stop_event)
        
        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\nStopping PI1 controller\n')
        stop_event.set()
        # for t in stop_threads:
            
        #     t.join()
            
