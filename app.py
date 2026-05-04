from flask import Flask, jsonify, request, render_template
import csv
import os
import threading
import time
import random
from datetime import datetime

# Fix: always use the folder this file lives in — no matter where you run it from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# ── State ──────────────────────────────────────────────────────────────────────
monitoring_active = False
packets = []          # all captured/loaded packets
monitor_thread = None
packet_lock = threading.Lock()

PORT_SERVICES = {
    80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH",
    21: "FTP", 25: "SMTP", 110: "POP3", 3306: "MySQL",
    8080: "HTTP-Alt", 3389: "RDP", 67: "DHCP", 123: "NTP", 0: "ICMP Echo"
}

SRC_IPS = ["192.168.1.5","192.168.1.10","192.168.1.20","10.0.0.5",
           "10.0.0.12","172.16.0.3","192.168.0.50","192.168.1.100"]
DST_IPS = ["8.8.8.8","1.1.1.1","142.250.80.46","151.101.1.140",
           "104.16.123.96","13.107.42.16","52.96.0.22","192.168.1.1"]

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_csv():
    path = os.path.join(BASE_DIR, "traffic_data.csv")
    records = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["packet_size"] = int(row["packet_size"])
            row["src_port"] = int(row["src_port"])
            row["dst_port"] = int(row["dst_port"])
            records.append(row)
    return records

def make_simulated_packet():
    proto = random.choice(["TCP", "UDP", "ICMP"])
    dst_port = random.choice(list(PORT_SERVICES.keys())) if proto != "ICMP" else 0
    src_port = random.randint(49152, 65535) if proto != "ICMP" else 0
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "src_ip": random.choice(SRC_IPS),
        "dst_ip": random.choice(DST_IPS),
        "protocol": proto,
        "packet_size": random.randint(64, 1500),
        "src_port": src_port,
        "dst_port": dst_port,
        "service": PORT_SERVICES.get(dst_port, "Unknown")
    }

def monitor_loop():
    global monitoring_active, packets
    while monitoring_active:
        pkt = make_simulated_packet()
        with packet_lock:
            packets.append(pkt)
        time.sleep(0.8)

def compute_stats(data):
    if not data:
        return {"total": 0, "tcp": 0, "udp": 0, "icmp": 0, "avg_size": 0}
    total = len(data)
    return {
        "total": total,
        "tcp": sum(1 for p in data if p["protocol"] == "TCP"),
        "udp": sum(1 for p in data if p["protocol"] == "UDP"),
        "icmp": sum(1 for p in data if p["protocol"] == "ICMP"),
        "avg_size": round(sum(p["packet_size"] for p in data) / total, 1)
    }

def apply_filters(data, proto, src, dst):
    result = data
    if proto and proto != "ALL":
        result = [p for p in result if p["protocol"] == proto]
    if src:
        result = [p for p in result if src in p["src_ip"]]
    if dst:
        result = [p for p in result if dst in p["dst_ip"]]
    return result

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_monitoring():
    global monitoring_active, packets, monitor_thread
    if not monitoring_active:
        with packet_lock:
            packets = load_csv()   # preload CSV data
        monitoring_active = True
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    return jsonify({"status": "started"})

@app.route("/api/stop", methods=["POST"])
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    return jsonify({"status": "stopped"})

@app.route("/api/packets")
def get_packets():
    proto = request.args.get("protocol", "ALL")
    src   = request.args.get("src_ip", "").strip()
    dst   = request.args.get("dst_ip", "").strip()
    with packet_lock:
        data = list(packets)
    filtered = apply_filters(data, proto, src, dst)
    return jsonify({
        "packets": filtered[-200:],   # last 200 for display
        "stats": compute_stats(filtered),
        "monitoring": monitoring_active
    })

@app.route("/api/clear", methods=["POST"])
def clear_packets():
    global packets
    with packet_lock:
        packets = []
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
