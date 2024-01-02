
from simulators.gyro import run_gyro_simulator
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



def gyro_callback(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, settings):
    t = time.localtime()
    # safe_print("\n"+"="*20,
    #            f"GYRO ID: {settings['id']}",
    #            f"Timestamp: {time.strftime('%H:%M:%S', t)}",
    #            f"Acceleration: x = {accel_x}, y = {accel_y}, z = {accel_z}",
    #            f"Rotation: x = {gyro_x}, y = {gyro_y}, z = {gyro_z}"
    #            )
    acceleration_payload={
             'measurement': 'Acceleration',
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': [float(accel_x),float(accel_y),float(accel_z)]
        }
    rotation_payload={
             'measurement': 'Rotation',
             'simulated': settings['simulated'],
             'connectedToPi': settings['connectedToPi'],
             'name': settings['name'],
             'id': settings['id'],
             'value': [float(gyro_x), float(gyro_y), float(gyro_z)]
        }
    with counter_lock:
        batch.append((settings['type'], json.dumps(acceleration_payload), 0, True))
        batch.append((settings['type'], json.dumps(rotation_payload), 0, True))
        publish_data_counter.increment()
    if publish_data_counter.value>=publish_data_limit:
        
        publish_event.set()
    


def run_gyro(settings, threads, stop_event):
        threads.append(publisher_thread)
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            gyro_thread = threading.Thread(target = run_gyro_simulator, args=(settings, 2, gyro_callback, stop_event))
            gyro_thread.start()
            threads.append(gyro_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from sensors.gyro import MPU6050
            from sensors.gyro.gyro import run_gyro_loop
            print(f"\nStarting {settings['id']} loop\n")
            mpu = MPU6050.MPU6050()
            mpu.dmp_initialize()
            gyro_thread = threading.Thread(target=run_gyro_loop, args=(mpu, settings, 2, gyro_callback, stop_event))
            gyro_thread.start()
            threads.append(gyro_thread)
            print(f"\n{settings['id']} loop started\n")
