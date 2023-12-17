
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
import time
from utils.mqtt import connect

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def run_pi1(settings, threads, stop_event):
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
    
    run_dht(rdht1_settings, threads, stop_event)
    run_dht(rdht2_settings, threads, stop_event)
    run_uds(dus1_settings, threads, stop_event)
    run_pir(dpir1_settings, threads, stop_event)
    run_pir(rpir1_settings, threads, stop_event)
    run_pir(rpir2_settings, threads, stop_event)
    run_buzzer(db_settings, threads, stop_event)
    run_button(ds1_settings, threads, stop_event)
    run_led_diode(dl_settings, threads, stop_event)
    run_membrane_switch(dms_settings, threads, stop_event)

def run_pi2(settings, threads, stop_event):
    gsg_settings = settings['GSG']
    run_gyro(gsg_settings, threads, stop_event)
    glcd_settings = settings['GLCD']
    run_lcd(glcd_settings, threads, stop_event)

def run_pi3(settings, threads, stop_event):
    b4sd_settings = settings['B4SD']
    run_4segment_display(b4sd_settings, threads, stop_event)
    brgb_settings = settings['BRGB']
    run_rgb_diode(brgb_settings, threads, stop_event)


if __name__ == "__main__":
    settings = load_settings()
    stop_threads = []
    stop_event = threading.Event()
    
    # connect()
    try:
        if settings["PI1_running"]:
            run_pi1(settings, stop_threads, stop_event)
        if settings["PI2_running"]:
            run_pi2(settings, stop_threads, stop_event)
        if settings["PI3_running"]:
            run_pi3(settings, stop_threads, stop_event)
        
       
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\nStopping PI1 controller\n')
        stop_event.set()
        # for t in stop_threads:
            
        #     t.join()
            
