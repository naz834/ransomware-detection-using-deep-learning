from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import joblib
import numpy as np
import time
from threading import Thread

model = joblib.load("ransomware_detection_model.pkl")
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)
socketio = SocketIO(app)

base_sample = {
    "Machine": 34800,
    "DebugSize": 104,
    "DebugRVA": 20480,
    "MajorImageVersion": 6,
    "MajorOSVersion": 6,
    "ExportRVA": 23000,
    "ExportSize": 350,
    "IatVRA": 19000,
    "MajorLinkerVersion": 11,
    "MinorLinkerVersion": 20,
    "NumberOfSections": 7,
    "SizeOfStackReserve": 524288,
    "DllCharacteristics": 32768,
    "ResourceSize": 4000,
    "BitcoinAddresses": 1
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        features = np.array([list(data.values())]).reshape(1, -1)
        scaled = scaler.transform(features)
        pred = model.predict(scaled)[0]
        status = "✅ Benign File" if pred == 1 else "🚨 Ransomware Detected!"
        result = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "status": status}
        socketio.emit("new_detection", result)
        return jsonify({"prediction": status})
    except Exception as e:
        return jsonify({"error": str(e)})

def simulate():
    time.sleep(1)
    count = 0
    while True:
        time.sleep(5)
        sample = base_sample.copy()
        if count < 2:
            status = "🚨 Ransomware Detected!"
        else:
            sample["BitcoinAddresses"] = np.random.randint(0, 2)
            features = np.array([list(sample.values())]).reshape(1, -1)
            scaled = scaler.transform(features)
            pred = model.predict(scaled)[0]
            status = "✅ Benign File" if pred == 1 else "🚨 Ransomware Detected!"
        result = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "status": status}
        socketio.emit("new_detection", result)
        count += 1

Thread(target=simulate, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

