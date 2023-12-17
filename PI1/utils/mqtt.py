import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from utils.counter import Counter

import threading

mqtt_client = mqtt.Client()
mqtt_lock=threading.Lock()
def connect():
    global mqtt_client
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()

def publish_message(event, batch, device_lock, counter):
    while True:
        event.wait()
        with device_lock:
            local_batch=batch.copy()
            counter.value=0
            batch.clear()
        with mqtt_lock:
            publish.multiple(local_batch, hostname="localhost", port=1883)
        event.clear()
