
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
alarm_clock_event = None

def segment_display_callback(digit1, digit2, digit3, digit4, settings, blink):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"4SEGMENT DISPLAY ID: {settings['id']}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"DISPLAY: {digit1}{digit2}:{digit3}{digit4}",
                f"CLOCK ALARM: {str(blink)}"
                )
    payload={
             'measurement': settings['type'],
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': f"{digit1}{digit2}:{digit3}{digit4}",
             'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    with counter_lock:
        batch.append((settings['type'], json.dumps(payload), 0, False))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()
    



def run_4segment_display(settings, _totalPersons, threads, stop_event, _alarm_clock_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)

    global alarm_clock_event
    alarm_clock_event = _alarm_clock_event

    threads.append(publisher_thread)
    if settings['simulated']:
        from simulators.segment_display import run_4segment_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        segment_display_thread = threading.Thread(target = run_4segment_simulator, args=(settings, 1, segment_display_callback, stop_event, alarm_clock_event))
        segment_display_thread.start()
        threads.append(segment_display_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.segment_display import display_time_on_segment_display, SegmentDisplay
        print(f"\nStarting {settings['id']} loop\n")
        segment_display = SegmentDisplay(settings['id'], settings['seg_pin1'], settings['seg_pin2'], settings['seg_pin3'], settings['seg_pin4'],
                                          settings['seg_pin5'], settings['seg_pin6'], settings['seg_pin7'], settings['seg_pin8'],
                                          settings['dig_pin1'], settings['dig_pin2'], settings['dig_pin3'], settings['dig_pin4'],)

        segment_display_thread = threading.Thread(target=display_time_on_segment_display, args=(segment_display, settings, 1, segment_display_callback, stop_event, alarm_clock_event))
        segment_display_thread.start()
        threads.append(segment_display_thread)
        print(f"\n{settings['id']} loop started\n")