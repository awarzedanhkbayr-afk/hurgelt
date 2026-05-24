from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, time
from collections import deque

app = Flask(__name__, static_folder='static')
CORS(app)

events = deque(maxlen=100)
replies = deque(maxlen=100)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/owner')
def owner():
    return send_from_directory('static', 'owner.html')

@app.route('/ring', methods=['POST'])
def ring():
    data = request.json or {}
    name = data.get('name', 'Үйлчлүүлэгч')[:40]
    ts = int(time.time() * 1000)
    events.appendleft({'name': name, 'ts': ts, 'id': ts})
    return jsonify({'ok': True})

@app.route('/poll')
def poll():
    since = int(request.args.get('since', 0))
    new_events = [e for e in events if e['ts'] > since]
    return jsonify({'events': new_events, 'time': int(time.time() * 1000)})

@app.route('/reply', methods=['POST'])
def reply_route():
    data = request.json or {}
    ok = data.get('ok', False)
    name = data.get('name', 'Үйлчлүүлэгч')[:40]
    ts = int(time.time() * 1000)
    replies.appendleft({'ok': ok, 'name': name, 'ts': ts})
    return jsonify({'ok': True})

@app.route('/replies')
def get_replies():
    since = int(request.args.get('since', 0))
    new_replies = [r for r in replies if r['ts'] > since]
    return jsonify({'replies': new_replies, 'time': int(time.time() * 1000)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
