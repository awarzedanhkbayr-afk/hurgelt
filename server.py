from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, time
from collections import deque

app = Flask(__name__, static_folder='static')
CORS(app, origins="*")

events = deque(maxlen=100)
replies = deque(maxlen=100)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/owner')
def owner():
    return send_from_directory('static', 'owner.html')

@app.route('/ring', methods=['POST', 'OPTIONS'])
def ring():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.json or {}
    name = data.get('name', 'Үйлчлүүлэгч')[:40]
    ts = int(time.time() * 1000)
    events.appendleft({'name': name, 'ts': ts})
    return jsonify({'ok': True})

@app.route('/poll', methods=['GET', 'OPTIONS'])
def poll():
    if request.method == 'OPTIONS':
        return '', 204
    since = int(request.args.get('since', 0))
    new_events = [e for e in events if e['ts'] > since]
    return jsonify({'events': new_events, 'time': int(time.time() * 1000)})

@app.route('/reply', methods=['POST', 'OPTIONS'])
def reply_route():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.json or {}
    ok = data.get('ok', False)
    name = data.get('name', 'Үйлчлүүлэгч')[:40]
    ts = int(time.time() * 1000)
    replies.appendleft({'ok': ok, 'name': name, 'ts': ts})
    return jsonify({'ok': True})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
