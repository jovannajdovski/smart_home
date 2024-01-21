import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from utils.counter import Counter

import threading

mqtt_client = mqtt.Client()
mqtt_lock=threading.Lock()
def connect():
    global mqtt_client
    mqtt_client.connect("10.1.121.64", 1883, 60)
    # mqtt_client.connect("10.1.121.102", 1883, 60)
    mqtt_client.loop_start()

def publish_message(event, batch, device_lock, counter):
    while True:
        event.wait()
        with device_lock:
            local_batch=batch.copy()
            counter.value=0
            batch.clear()
        with mqtt_lock:
            publish.multiple(local_batch, hostname="10.1.121.64", port=1883)
            # publish.multiple(local_batch, hostname="10.1.121.102", port=1883)
            
        event.clear()
