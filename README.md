# CN_Project_BCSF24A021

# PULSAR — Network Traffic Monitor

> A web-based network traffic monitoring and analysis platform built with Python (Flask) and HTML/CSS/JavaScript.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey?style=flat-square)
![HTML5](https://img.shields.io/badge/HTML5%2FCSS3%2FJS-Frontend-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## About

PULSAR was designed and built by **Abdullah Sadiq** (BCSF24A021) as a Computer Networks course project. The goal was to create a functional, well-structured network traffic monitoring tool that demonstrates core networking concepts — protocol identification, port-to-service mapping, packet statistics, and traffic filtering — in an accessible web interface.

The name **PULSAR** reflects the idea of a system that continuously listens, pulses, and reports on network activity — much like a pulsar star emits regular, detectable signals.

The project is built entirely with beginner-friendly technologies (Python + Flask for the backend, plain HTML/CSS/JS for the frontend) and requires no external dependencies beyond Flask itself. It is designed to be easy to run locally, easy to understand, and easy to extend.

---

## Overview

**PULSAR** is a real-time network traffic monitoring platform that captures, displays, filters, and analyses network packet data through a clean, terminal-style web interface.

The system loads a simulated dataset of 200 traffic records on startup and continuously generates new packets during monitoring. All filtering, statistics, and display features update live every second.

---

## Features

- **Start / Stop monitoring** with a single click
- **Live packet table** showing Time, Source IP, Source Port, Destination IP, Destination Port, Protocol, Service, and Packet Size
- **Protocol identification** — TCP, UDP, and ICMP, color-coded in the UI
- **Port-to-service mapping** for 12 common ports (HTTP, HTTPS, DNS, SSH, FTP, SMTP, POP3, MySQL, HTTP-Alt, RDP, DHCP, NTP)
- **Live statistics** — Total packets, TCP / UDP / ICMP counts, and average packet size
- **Filtering** by Protocol (dropdown), Source IP, and Destination IP (partial match supported)
- **System log** with timestamped monitoring events
- **REST API** backend with clean JSON endpoints
- **Real-time simulation** — new packet generated every 0.8 seconds

---

## Project Structure

```
pulsar/
├── app.py               # Flask backend — API endpoints, simulation logic
├── traffic_data.csv     # Simulated dataset (200 records)
└── templates/
    └── index.html       # Frontend — HTML, CSS, and JavaScript
```

---

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/pulsar.git
cd pulsar

# 2. Install dependencies
pip install flask

# 3. Run the server
python app.py
```

### Usage

1. Open your browser and go to `http://localhost:5000`
2. Click **START MONITORING** to load the dataset and begin simulation
3. Use the filter panel to narrow traffic by Protocol, Source IP, or Destination IP
4. Click **STOP** to pause monitoring (data remains visible)
5. Click **CLEAR DATA** to reset

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the main HTML interface |
| `/api/start` | POST | Loads CSV data and starts simulation thread |
| `/api/stop` | POST | Stops the simulation thread |
| `/api/packets` | GET | Returns filtered packets and statistics (JSON) |
| `/api/clear` | POST | Clears all packets from memory |

### Query Parameters for `/api/packets`

| Parameter | Values | Description |
|---|---|---|
| `protocol` | `ALL`, `TCP`, `UDP`, `ICMP` | Filter by protocol type |
| `src_ip` | any string | Partial match on source IP |
| `dst_ip` | any string | Partial match on destination IP |

---

## Dataset

The CSV dataset (`traffic_data.csv`) contains 200 simulated network traffic records with the following fields:

| Field | Example | Description |
|---|---|---|
| `time` | `10:35:21` | Packet timestamp |
| `src_ip` | `192.168.1.5` | Source IP address |
| `dst_ip` | `8.8.8.8` | Destination IP address |
| `protocol` | `TCP` | Protocol type (TCP / UDP / ICMP) |
| `packet_size` | `512` | Size in bytes (range: 64–1500) |
| `src_port` | `52341` | Ephemeral source port |
| `dst_port` | `80` | Destination port |
| `service` | `HTTP` | Derived from port-to-service mapping |

---

## Port-to-Service Mapping

| Port | Service | Port | Service |
|---|---|---|---|
| 80 | HTTP | 443 | HTTPS |
| 53 | DNS | 22 | SSH |
| 21 | FTP | 25 | SMTP |
| 110 | POP3 | 3306 | MySQL |
| 8080 | HTTP-Alt | 3389 | RDP |
| 67 | DHCP | 123 | NTP |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3, Flask |
| Dataset | CSV (200 records) |
| Fonts | JetBrains Mono, Syne (via Google Fonts) |

---

## Academic Context

This project was developed as part of the **Computer Networks** course at university, under the supervision of **Dr. Madeeha Aman**.

- **Student:** Abdullah Sadiq
- **Roll Number:** BCSF24A021
- **Submitted:** May 4, 2026

---

## License

This project is for educational purposes. Feel free to use or adapt the code with attribution.
