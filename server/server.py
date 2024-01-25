#from wsgiref.simple_server import WSGIServer
# from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from datetime import datetime
import json
import os



app = Flask(__name__)
CORS(app)

# InfluxDB Configuration
token = "qHBkZB-YWpO0OqRrPd9VMDBv-EaTMZBGahrrkxVVB6OjCa4k3cztG5snU5AiWUBucjie1KKFsMCw3yqtVckRvg=="
# token="DO-FFdev8G24pNFMFT7QDv4XYU3iijl__DnNmqaG6H7nCqom_CbxIRopPfcHzmKzLU2an-dyMvI9CZPuuwbBYg=="
org = "FTN"
url = "http://localhost:8087"
bucket = "iot_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe("BUTTON")
    client.subscribe("LIGHT") #actuator
    client.subscribe("US")
    client.subscribe("BUZZER") #actuator
    client.subscribe("PIR")
    client.subscribe("MS")
    client.subscribe("DHT")
    client.subscribe("GYRO")
    client.subscribe("LCD") #actuator
    client.subscribe("4DD") #actuator
    client.subscribe("RGB-LIGHT") #actuator
    client.subscribe("ALARM")


def on_message(client, userdata, msg):
    #print(f"Rec. TOPIC \t: {msg.topic}")
    
    data = json.loads(msg.payload.decode('utf-8'))
    if msg.topic=="ALARM":
        save_alarm_to_db(data)
    else:
        save_to_db(data)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def save_alarm_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    point = (
        Point(data["measurement"])
        .field("measurement", data["value"])
        .time(data['time'])
    )
    try:
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print("Exception when writing to InfluxDB: %s\n" % e)
        print("Response body:", e.body)
        print("Response headers:", e.headers)

def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["connectedToPi"])
        .tag("name", data["name"])
        .tag("id",data['id'])
        .time(data['time'])
    )
    measurement=data["measurement"]
    value=data["value"]
    gyro_column_names=['_x','_y','_z']
    if isinstance(value, list):
        for i, element in enumerate(value):
            field_name = measurement+gyro_column_names[i]  # Adjust the field name as needed
            point = point.field(field_name, element)
    else:
        # If 'value' is not a list, add a single field
        point = point.field("measurement", value)
    try:
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print("Exception when writing to InfluxDB: %s\n" % e)
        print("Response body:", e.body)
        print("Response headers:", e.headers)

@app.route('/send_pin', methods=['POST'])
def send_pin():
    data = request.get_json()

    pin = data.get('pin')

    if pin is not None:
        publish.multiple([('pin', json.dumps(data), 0, False)], hostname="localhost", port=1883)
        return jsonify({'result': 'Success'}), 200 
    else:
        return jsonify({'error': 'Invalid request'}), 400
    
@app.route('/send_rgb_command', methods=['POST'])
def send_rgb_command():
    data = request.get_json()
    print(data)
    command = data.get('command')

    if command is not None:
        publish.multiple([('rgb-command', json.dumps(data), 0, False)], hostname="localhost", port=1883)
        return jsonify({'result': 'Success'}), 200 
    else:
        return jsonify({'error': 'Invalid request'}), 400 
    

@app.route('/send_clock_command', methods=['POST'])
def send_clock_command():
    data = request.get_json()
    print(data)
    command = data.get('command')

    if command is not None:
        publish.multiple([('clock-command', json.dumps(data), 0, False)], hostname="localhost", port=1883)
        return jsonify({'result': 'Success'}), 200 
    else:
        return jsonify({'error': 'Invalid request'}), 400 

def generate_query(measurement):
    query = f'from(bucket: "iot_db") |> range(start: 0, stop: now()) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> yield(name: "last")'
    return query.format(bucket)

def generate_query_with_id(measurement, id):
    query = f'from(bucket: "iot_db") |> range(start: 0, stop: now()) |> filter(fn: (r) => r["id"] == "{id}") |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> yield(name: "last")'
    return query.format(bucket)

@app.route('/get_all', methods=['GET'])
def get_all():
    settings=load_settings()
    response_list=[]
    measurements_pairs = [("ALARM","ALARM"), ("4DD","B4SD"),("LIGHT", "DL"),("RGB-LIGHT", "BRGB"), ("Acceleration","GSG"), ("LCD","GLCD"), ("Rotation","GSG")]
    measurements_pairs_with_id=[("PIR", "DPIR1"),("PIR", "DPIR2"),("PIR", "RPIR1"),("PIR", "RPIR2"),("PIR", "RPIR3"),("PIR", "RPIR4"),
            ("BUTTON","DS1"), ("BUTTON","DS2"),("BUZZER","DB"), ("BUZZER","BB"),
            ("US", "DUS1"),("US", "DUS2"), 
            ("Temperature", "GDHT"),("Humidity", "GDHT"),("Temperature", "RDHT1"),("Humidity", "RDHT1"),
            ("Temperature", "RDHT2"),("Humidity", "RDHT2"),("Temperature", "RDHT3"),("Humidity", "RDHT3"),
            ("Temperature", "RDHT4"),("Humidity", "RDHT4") ]
    last_acceleration_values=[]
    for measurement, id in measurements_pairs:
        result = influxdb_client.query_api().query(org=org, query=generate_query(measurement))
        if measurement =='ALARM':
            if len(result)>0 and len(result[0].records)>0:
                record=result[0].records[-1]
                response_list.append({'measurement': record.get_measurement(), 'time': record.get_time(), 'value': record.get_value(), 'id': id, 'pi':-1})
            else:
                response_list.append({'measurement': measurement, 'time': None, 'value': None, 'id': id, 'pi':-1})
        elif measurement == 'Acceleration':
            time=None
            values=[]
            field=None
            if len(result)>0 and len(result[0].records)>0:
                for table in result:
                    record=table.records[-1]
                    field=record.get_measurement()
                    time=record.get_time()
                    last_acceleration_values.append(record.get_value())
        elif measurement == 'Rotation':
            time=None
            values=[]
            field=None
            if len(result)>0 and len(result[0].records)>0:
                for table in result:
                    record=table.records[-1]
                    field=record.get_measurement()
                    time=record.get_time()
                    values.append(record.get_value())
                response_list.append({'measurement': field, 'time': time, 'value': [last_acceleration_values,values], 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            else:
                response_list.append({'measurement': measurement, 'time': None, 'value':[last_acceleration_values, []], 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            last_acceleration_values=[]
        else:
            if len(result)>0 and len(result[0].records)>0:
                record=result[0].records[-1]
                response_list.append({'measurement': record.get_measurement(), 'time': record.get_time(), 'value': record.get_value(), 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            else:
                response_list.append({'measurement': measurement, 'time': None, 'value': None, 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
    last_temperature_value=None
    for measurement, id in measurements_pairs_with_id:
        result = influxdb_client.query_api().query(org=org, query=generate_query_with_id(measurement, id))
        if measurement=='Temperature':
            if len(result)>0 and len(result[0].records)>0:
                last_temperature_value=result[0].records[-1].get_value()
        elif measurement=='Humidity':
            if len(result)>0 and len(result[0].records)>0:
                record=result[0].records[-1]
                response_list.append({'measurement': 'DHT', 'time': record.get_time(), 'value': [last_temperature_value,record.get_value()], 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            else:
                response_list.append({'measurement': 'DHT', 'time': None, 'value': [last_temperature_value,None], 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            last_temperature_value=None
        else:
            if len(result)>0 and len(result[0].records)>0:
                record=result[0].records[-1]
                response_list.append({'measurement': record.get_measurement(), 'time': record.get_time(), 'value': record.get_value(), 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
            else:
                response_list.append({'measurement': measurement, 'time': None, 'value': None, 'id': id, 'area': settings[id]['area'], 'type': settings[id]['type'], 'pi': settings[id]['connectedToPi']})
           
        # print(f"Result for {measurement}: {result}")

    response_list.append({'id': settings["DMS"]["id"], 'type': settings["DMS"]['type'], 'name': settings["DMS"]["name"], 'area':settings["DMS"]["area"], 'code':"0123", 'pi':1})
    
    response_list.append({'id': settings["BIR"]["id"], 'type': settings["BIR"]['type'], 'name': settings["BIR"]["name"], 'area':settings["BIR"]["area"], 'active':False, 'color':"red", 'pi':3})
    return jsonify(response_list)

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


def load_settings(filePath='../config/settings.json'):
    script_dir = os.path.dirname(__file__)
    
    # Create the absolute path to the settings.json file
    absolute_path = os.path.join(script_dir, filePath)
    
    with open(absolute_path, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
    app.run(debug=False)


