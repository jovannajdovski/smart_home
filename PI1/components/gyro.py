
from simulators.gyro import run_gyro_simulator
import threading
import time
from utils.safe_print import safe_print
from utils.mqtt import publish_message 

def gyro_callback(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, id):
    t = time.localtime()
    safe_print("\n"+"="*20,
               f"GYRO ID: {id}",
               f"Timestamp: {time.strftime('%H:%M:%S', t)}",
               f"Acceleration: x = {accel_x}, y = {accel_y}, z = {accel_z}",
               f"Rotation: x = {gyro_x}, y = {gyro_y}, z = {gyro_z}"
               )


def run_gyro(settings, threads, stop_event):
        if settings['simulated']:
            print(f"\nStarting {settings['id']} simulator\n")
            gyro_thread = threading.Thread(target = run_gyro_simulator, args=(settings['id'], 2, gyro_callback, stop_event))
            gyro_thread.start()
            threads.append(gyro_thread)
            print(f"\n{settings['id']} simulator started\n")
        else:
            from sensors.gyro import MPU6050
            from sensors.gyro.gyro import run_gyro_loop
            print(f"\nStarting {settings['id']} loop\n")
            mpu = MPU6050.MPU6050()
            mpu.dmp_initialize()
            gyro_thread = threading.Thread(target=run_gyro_loop, args=(mpu, 2, gyro_callback, stop_event, settings['id']))
            gyro_thread.start()
            threads.append(gyro_thread)
            print(f"\n{settings['id']} loop started\n")
