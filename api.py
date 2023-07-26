from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Ielādē sensoru datus no "sensors.json" faila
with open('sensors.json', 'r') as sensors_file:
    sensors_data = json.load(sensors_file)

# Ielādē metriku datus no "metrics.json" faila
with open('metrics.json', 'r') as metrics_file:
    metrics_data = json.load(metrics_file)

# Ielādē sensoru tipu datus no "sensorTypes.json" faila
with open('sensorTypes.json', 'r') as sensor_types_file:
    sensor_types_data = json.load(sensor_types_file)

# API punkts, kas atgriež sensoru datus
@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    return jsonify(sensors_data)

# API punkts, kas atgriež metriku datus
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    return jsonify(metrics_data)

# API punkts, kas atgriež sensoru tipu datus
@app.route('/api/sensorTypes', methods=['GET'])
def get_sensor_types():
    return jsonify(sensor_types_data)

if __name__ == '__main__':
    app.run()