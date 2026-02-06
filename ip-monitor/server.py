from flask import Flask, jsonify, request, send_from_directory
import subprocess
import os
import threading
import time

app = Flask(__name__)

# ────── 文件路径 ──────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IP_FILE = os.path.join(BASE_DIR, "ips.txt")

# 自动生成默认 IP 文件
if not os.path.exists(IP_FILE):
    with open(IP_FILE, "w") as f:
        f.write("8.8.8.8\n1.1.1.1\n223.5.5.5\n")

# ────── IP 工具函数 ──────
def get_ips():
    with open(IP_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def save_ips(ips):
    with open(IP_FILE, "w") as f:
        for ip in ips:
            f.write(ip + "\n")

# ping 函数返回状态和延迟
def ping(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return {"status": "down", "time": "-"}
        
        for line in result.stdout.split("\n"):
            if "time=" in line:
                time_ms = line.split("time=")[1].split(" ")[0]
                return {"status": "up", "time": f"{time_ms} ms"}
        return {"status": "up", "time": "-"}
    except:
        return {"status": "down", "time": "-"}

# ────── 状态缓存 ──────
status_cache = {}

def refresh_status():
    while True:
        ips = get_ips()
        for ip in ips:
            status_cache[ip] = ping(ip)
        time.sleep(3)

threading.Thread(target=refresh_status, daemon=True).start()

# ────── API 接口 ──────
@app.route("/status")
def status():
    return jsonify(status_cache)

@app.route("/add_ip", methods=["POST"])
def add_ip():
    new_ip = request.json.get("ip", "").strip()
    if not new_ip:
        return jsonify({"error": "IP不能为空"}), 400
    ips = get_ips()
    if new_ip in ips:
        return jsonify({"error": "IP已存在"}), 400
    ips.append(new_ip)
    save_ips(ips)
    return jsonify({"success": True})

@app.route("/delete_ip", methods=["POST"])
def delete_ip():
    del_ip = request.json.get("ip", "").strip()
    ips = get_ips()
    if del_ip not in ips:
        return jsonify({"error": "IP不存在"}), 400
    ips.remove(del_ip)
    save_ips(ips)
    return jsonify({"success": True})

# ────── 前端页面 ──────
@app.route("/")
def home():
    return send_from_directory(os.path.join(BASE_DIR, "templates"), "index.html")

# ────── 启动服务 ──────
app.run(host="0.0.0.0", port=5000)
