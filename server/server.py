from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)


# InfluxDB Configuration
token = "DO-FFdev8G24pNFMFT7QDv4XYU3iijl__DnNmqaG6H7nCqom_CbxIRopPfcHzmKzLU2an-dyMvI9CZPuuwbBYg=="
org = "FTN"
url = "http://localhost:8087"
bucket = "iot_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("BUTTON")
    client.subscribe("LIGHT")
    client.subscribe("US")
    client.subscribe("BUZZER")
    client.subscribe("PIR")
    client.subscribe("MS")
    client.subscribe("DHT")
    client.subscribe("GYRO")
    client.subscribe("LCD")
    client.subscribe("4DD")


def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    data = json.loads(msg.payload.decode('utf-8'))
    print(data)
    print('\n')
    # save_to_db(data)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        save_to_db(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = ""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = ""
    return handle_influx_query(query)

@app.route('/test', methods=['GET'])
def test_endpoint():
    return "rerna"

if __name__ == '__main__':
    app.run(debug=False)
