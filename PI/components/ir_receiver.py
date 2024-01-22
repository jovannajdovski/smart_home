
from simulators.ir_receiver import run_ir_receiver_simulator
import threading
import time
import json
from utils.safe_print import safe_print
from utils.mqtt import publish_message 
from utils.counter import Counter

batch = []
publish_data_counter = Counter(0)
publish_data_limit = 5
publish_event=threading.Event()
counter_lock = threading.Lock()
publisher_thread = threading.Thread(target=publish_message, args=(publish_event, batch, counter_lock, publish_data_counter ))
publisher_thread.daemon = True
publisher_thread.start()
totalPersons=None

def ir_receiver_callback(command, settings):
    t = time.localtime()

    safe_print("\n"+"="*20,
            f"IR RECEIVER ID: {settings['id']}",
            f"Timestamp: {time.strftime('%H:%M:%S', t)}",
            f"Command: {command}",
            )

    command_payload={
             'measurement': 'Receiver_Command',
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': command
        }

    with counter_lock:       
        batch.append((settings['type'], json.dumps(command_payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        publish_event.set()


def run_ir_receiver(settings, _totalPersons, threads, stop_event):
    global totalPersons
    totalPersons=_totalPersons
    threads.append(publisher_thread)
    if settings['simulated']:
        print(f"\nStarting {settings['id']} simulator\n")
        ir_receiver_thread = threading.Thread(target = run_ir_receiver_simulator, args=(settings, 5, ir_receiver_callback, stop_event))
        ir_receiver_thread.start()
        threads.append(ir_receiver_thread)
        print(f"\n{settings['id']} simulator started\n")
    else:
        from sensors.ir_receiver import run_ir_receiver_loop, IrReceiver
        print(f"\nStarting {settings['id']} loop\n")
        ir_receiver = IrReceiver(settings['id'], settings['pin'])
        ir_receiver_thread = threading.Thread(target=run_ir_receiver_loop, args=(ir_receiver, settings, ir_receiver_callback, stop_event))
        ir_receiver_thread.start()
        threads.append(ir_receiver_thread)
        print(f"\n{settings['id']} loop started\n")
