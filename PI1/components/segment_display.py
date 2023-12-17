
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def segment_display_callback(digit1, digit2, digit3, digit4, id):      
    t = time.localtime()
    safe_print("\n"+"="*20,
                f"4SEGMENT DISPLAY ID: {id}",
                f"Timestamp: {time.strftime('%H:%M:%S', t)}",
                f"DISPLAY: {digit1}{digit2}:{digit3}{digit4}"
                )


def run_4segment_display(settings, threads, stop_event):
    if settings['simulated']:
        from simulators.segment_display import run_4segment_simulator
        print(f"\nStarting {settings['id']} simulator\n")
        segment_display_thread = threading.Thread(target = run_4segment_simulator, args=(settings['id'], 5, segment_display_callback, stop_event))
        segment_display_thread.start()
        threads.append(segment_display_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from actuators.segment_display import display_time_on_segment_display, SegmentDisplay
        print(f"\nStarting {settings['id']} loop\n")
        segment_display = SegmentDisplay(settings['id'], settings['seg_pin1'], settings['seg_pin2'], settings['seg_pin3'], settings['seg_pin4'],
                                          settings['seg_pin5'], settings['seg_pin6'], settings['seg_pin7'], settings['seg_pin8'],
                                          settings['dig_pin1'], settings['dig_pin2'], settings['dig_pin3'], settings['dig_pin4'],)

        segment_display_thread = threading.Thread(target=display_time_on_segment_display, args=(segment_display, 0.5, segment_display_callback, stop_event))
        segment_display_thread.start()
        threads.append(segment_display_thread)
        print(f"\n{settings['id']} loop started\n")