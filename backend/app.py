import socket
import threading
import platform
import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

TCP_IP = "0.0.0.0"
TCP_PORT = 9100

WINDOWS_ADAPTER = "Wi-Fi"
LINUX_ADAPTER = "enp2s0"

hercules_data = {"ip": "", "subnet": "", "gateway": ""}


def change_ip(adapter, ip, subnet, gateway):
    system = platform.system()
    try:
        if system == "Windows":
            cmd = f'netsh interface ip set address name="{adapter}" static {ip} {subnet} {gateway}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr or result.stdout or "Unknown error")
        elif system == "Linux":
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", adapter], check=True)
            subprocess.run(["sudo", "ip", "addr", "add", f"{ip}/24", "dev", adapter], check=True)
            subprocess.run(["sudo", "ip", "route", "add", "default", "via", gateway], check=True)
        else:
            raise Exception(f"Unsupported OS: {system}")
    except Exception as e:
        raise Exception(f"IP change failed: {e}")


@app.route("/api/change-ip", methods=["POST"])
def change_ip_route():
    try:
        data = request.get_json()
        ip = data.get("ip")
        subnet = data.get("subnet")
        gateway = data.get("gateway")

        adapter = WINDOWS_ADAPTER if platform.system() == "Windows" else LINUX_ADAPTER
        change_ip(adapter, ip, subnet, gateway)
        return jsonify({"status": "success", "message": "IP changed successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def start_tcp_server():
    global hercules_data
    print(f"[TCP] Listening for Hercules on {TCP_IP}:{TCP_PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(1)

    while True:
        conn, addr = server_socket.accept()
        print(f"[TCP] Connected from {addr}")
        buffer = ""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            decoded = chunk.decode("utf-8").strip()
            buffer += decoded + "\n"
            lines = [x.strip() for x in buffer.splitlines() if x.strip()]
            if len(lines) >= 3:
                hercules_data = {
                    "ip": lines[0],
                    "subnet": lines[1],
                    "gateway": lines[2],
                }
                print(f"[PARSED] {hercules_data}")
                socketio.emit("hercules_data", hercules_data)
                buffer = ""
        conn.close()
        print("[TCP] Connection closed")


@socketio.on("connect")
def handle_connect():
    print("[SOCKET] Frontend connected")
    emit("hercules_data", hercules_data)


if __name__ == "__main__":
    print("🚀 Starting backend (Windows + Linux Compatible)")
    threading.Thread(target=start_tcp_server, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5050)
