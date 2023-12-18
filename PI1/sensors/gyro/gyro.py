
import time
import os
        
def run_gyro_loop(mpu, settings, delay, callback, stop_event):

    accel = [0]*3
    gyro = [0]*3

    while True:
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()
        os.system('clear')

        accel = [round(value / 16384.0, 2) for value in accel]
        gyro = [round(value / 131.0, 2) for value in gyro]

        callback(accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2], settings)

        if stop_event.is_set():
                break
        time.sleep(delay)  # Delay between readings

