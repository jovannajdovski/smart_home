import time
import random

def generate_values():
      commands = ["OK","1","2","3"]
      while True:
            command_idx = random.randint(0, 3)
            yield commands[command_idx]
    

def run_ir_receiver_simulator(settings, delay, callback, stop_event):
    for command in generate_values():
        time.sleep(delay)
        callback(command, settings)
        if stop_event.is_set():
            break
              