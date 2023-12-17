
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.button import run_button
from components.rgb_diode import run_rgb_diode
from components.membrane_switch import run_membrane_switch
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def run_pi1():
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
    run_rgb_diode(dl_settings, threads, stop_event)
    run_membrane_switch(dms_settings, threads, stop_event)

def run_pi2():
    pass

def run_pi3():
    pass


if __name__ == "__main__":
    print('\nStarting PI1 controller\n')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        if settings["PI1_running"]:
            run_pi1(settings, threads, stop_event)
        if settings["PI2_running"]:
            run_pi2(settings, threads, stop_event)
        if settings["PI3_running"]:
            run_pi3(settings, threads, stop_event)
        
       
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\nStopping PI1 controller\n')
        for t in threads:
            stop_event.set()
