from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://Edtech:Kinetictile@cluster0.ojv0kad.mongodb.net/?appName=Cluster0")
db = client["esp8266_data"]            # Database name
collection = db["sensor_readings"]     # Collection name

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        # Add timestamp
        data["timestamp"] = datetime.utcnow()
        # Insert into MongoDB
        collection.insert_one(data)
        print("Data inserted:", data)
        return jsonify({"status": "success", "stored_data": data}), 200
    else:
        return jsonify({"status": "failed", "message": "No data received"}), 400

@app.route('/latest', methods=['GET'])
def latest_data():
    latest = collection.find().sort("timestamp", -1).limit(1)
    latest = list(latest)
    if latest:
        latest[0]["_id"] = str(latest[0]["_id"])  # Convert ObjectId to string
        return jsonify(latest[0]), 200
    return jsonify({"status": "no_data"}), 404

@app.route('/all', methods=['GET'])
def all_data():
    data = list(collection.find().sort("timestamp", -1))
    for item in data:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


