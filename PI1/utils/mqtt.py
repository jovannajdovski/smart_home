import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def publish_message():
    pass