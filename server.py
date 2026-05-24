from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, time
from collections import deque

app = Flask(__name__, static_folder='static')
CORS(app)

# SSE client queue - owner's browser listens here
clients = []
events = deque(maxlen=50)

OWNER_TOKEN = os.environ.get('OWNER_TOKEN', 'avarzed2024')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/owner')
def owner():
    return send_from_directory('static', 'owner.html')

@app.route('/ring', methods=['POST'])
def ring():
    data = request.json or {}
    name = data.get('name', 'Хүн')[:40]
    ts = int(time.time())
    event = {'name': name, 'ts': ts}
    events.appendleft(event)
    for q in list(clients):
        try:
            q.append(event)
        except:
            pass
    return jsonify({'ok': True})

@app.route('/reply', methods=['POST'])
def reply_route():
    data = request.json or {}
    ok = data.get('ok', False)
    name = data.get('name', 'Хүн')[:40]
    event = {'reply': True, 'ok': ok, 'name': name, 'ts': int(time.time())}
    events.appendleft(event)
    return jsonify({'ok': True})

@app.route('/stream')
def stream():
    token = request.args.get('token', '')
    if token != OWNER_TOKEN:
        return 'Unauthorized', 401

    from queue import Queue, Empty
    q = Queue()
    clients.append(q)

    def generate():
        try:
            yield 'data: {"ping":true}\n\n'
            while True:
                try:
                    event = q.get(timeout=25)
                    yield f'data: {json.dumps(event)}\n\n'
                except Empty:
                    yield 'data: {"ping":true}\n\n'
        finally:
            try:
                clients.remove(q)
            except:
                pass

    from flask import Response
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
