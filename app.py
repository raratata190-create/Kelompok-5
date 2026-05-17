from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# =========================
# REALTIME SENSOR DATA
# =========================

sensor_data = {
    "soil": 0,
    "water": 0,
    "distance": 0
}

# =========================
# HISTORY DATA
# =========================

history_data = []

# penanda jam terakhir disimpan
last_saved_hour = -1

# =========================
# DASHBOARD
# =========================

@app.route('/')
def home():
    return render_template('dashboard.html')

# =========================
# API REALTIME
# =========================

@app.route('/api/live')
def live_data():

    return jsonify(sensor_data)

# =========================
# API HISTORY
# =========================

@app.route('/api/history')
def history():

    return jsonify(history_data)

# =========================
# UPDATE FROM ESP32
# =========================

@app.route('/update', methods=['POST'])
def update_data():

    global sensor_data
    global history_data
    global last_saved_hour

    data = request.json

    # realtime
    sensor_data['soil'] = data['soil']
    sensor_data['water'] = data['water']
    sensor_data['distance'] = data['distance']

    now = datetime.now()

    # simpan history hanya setiap pergantian jam
    if now.hour != last_saved_hour:

        history_data.insert(0, {
            "time": now.strftime("%H:%M:%S"),
            "avg_soil": data['soil'],
            "avg_water": data['water'],
            "avg_distance": data['distance']
        })

        last_saved_hour = now.hour

    # maksimal 24 data
    if len(history_data) > 24:
        history_data.pop()

    return jsonify({
        "status": "success"
    })

# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )