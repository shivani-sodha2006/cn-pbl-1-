# cn-pbl-1

# Network Monitoring Tool

## Introduction

This project is a Python-based Network Monitoring Tool developed as part of our Computer Networks PBL project.

The main purpose of this tool is to monitor basic network activity, discover devices on the local network, check network latency, analyze network traffic, generate alerts, and store historical network measurements.

## Features

The tool contains the following modules:

- **C1 – Interface Traffic Monitor**
  - Displays upload and download traffic.
  - Monitors traffic on the selected network interface.

- **C2 – Local Subnet Host Discovery**
  - Finds active devices on the local network.
  - Displays IP address, MAC address, and hostname when available.
  - Uses ARP-based discovery.

- **C3 – Reachability & Latency Monitor**
  - Checks whether selected targets are reachable.
  - Measures minimum, average, and maximum latency.
  - Calculates jitter and packet loss.

- **C4 – Traffic Composition Analyzer**
  - Captures network packets for a selected time.
  - Shows protocol-wise packet and byte counts.
  - Displays top source and destination IP addresses.

- **E1 – Threshold Alerting**
  - Allows the user to set latency and packet-loss thresholds.
  - Generates an alert when a threshold is exceeded.

- **E3 – Historical Logging & Charting**
  - Records latency and packet-loss measurements.
  - Stores the results in a CSV file.
  - Generates a latency chart using Matplotlib.

## Technologies Used

- Python
- psutil
- Scapy
- Matplotlib
- socket
- ipaddress
- subprocess

## Project Structure

```text
cn pbl 1/
│
├── main.py
│
└── modules/
    ├── traffic_monitor.py
    ├── host_discovery.py
    ├── latency.py
    ├── traffic_analyzer.py
    ├── alerts.py
    └── index.py
