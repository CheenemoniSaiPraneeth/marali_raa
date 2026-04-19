from flask import Flask, jsonify, request, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"entries": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    data = load_data()
    return jsonify(data['entries'])

@app.route('/api/entries', methods=['POST'])
def save_entry():
    data = load_data()
    entry = request.json
    # Check if entry for this date already exists, update it
    existing = next((e for e in data['entries'] if e['date'] == entry['date']), None)
    if existing:
        data['entries'] = [entry if e['date'] == entry['date'] else e for e in data['entries']]
    else:
        data['entries'].append(entry)
    # Sort by date
    data['entries'].sort(key=lambda x: x['date'])
    save_data(data)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
