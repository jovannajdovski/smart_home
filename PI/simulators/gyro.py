import time
import random

RAW_MIN=-32768
RAW_MAX=32767

CONV_ACCEL_MIN=-1.0
CONV_ACCEL_MAX=1.0

CONV_GYRO_MIN=-250.0
CONV_GYRO_MAX=250.0

def generate_values(initial_raw_accel = 1, initial_raw_gyro=1):
      accel_raw = []
      accel_raw.append(initial_raw_accel)   # x
      accel_raw.append(initial_raw_accel)   # y
      accel_raw.append(initial_raw_accel)   # z

      gyro_raw = []
      gyro_raw.append(initial_raw_gyro)     # x
      gyro_raw.append(initial_raw_gyro)     # y
      gyro_raw.append(initial_raw_gyro)     # z

      while True:
            
        for i in range(3):
            accel_raw[i] += random.randint(-5000, 5000)

            if accel_raw[i] < RAW_MIN:
                accel_raw[i] = RAW_MIN
            if accel_raw[i] > RAW_MAX:
                accel_raw[i] = RAW_MAX

        for i in range(3):
            gyro_raw[i] += random.randint(-5000, 5000)

            if gyro_raw[i] < RAW_MIN:
                gyro_raw[i] = RAW_MIN
            if gyro_raw[i] > RAW_MAX:
                gyro_raw[i] = RAW_MAX

        yield (
            round(accel_raw[0]/16384.0, 2),
            round(accel_raw[1]/16384.0, 2),
            round(accel_raw[2]/16384.0, 2),
            round(gyro_raw[0]/131.0, 2),
            round(gyro_raw[1]/131.0, 2),
            round(gyro_raw[2]/131.0, 2)
        )

      

def run_gyro_simulator(settings, delay, callback, stop_event):
        for accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z in generate_values():
            time.sleep(delay)
            callback(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, settings)
            if stop_event.is_set():
                  break
              