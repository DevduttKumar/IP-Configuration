from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import socket

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def parse_tcp_data(data):
    try:
        parsed = json.loads(data)
        print("[TCP] Parsed Data:", parsed)
        socketio.emit('update_data', parsed)  # ✅ SOCKET EMIT
        print("[WS] Emitted payload to clients:", parsed)
    except Exception as e:
        print("[Error] Parsing:", e)

@app.route('/')
def index():
    return "Server Running..."

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5037)