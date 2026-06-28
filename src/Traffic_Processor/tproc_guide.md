# Traffic Processor – MVP V1

## Overview
This module is the **Traffic Processor (TP)** component of the network traffic processing platform.  
It captures live network packets on a specified interface, counts them by protocol (TCP/UDP/ICMP/other), and writes real‑time statistics to a text file (`data.txt` by default) every second.

---

## Dependencies
- Python 3.6+
- `scapy` – for packet capture and protocol detection

Install required packages:
```bash
pip install scapy
```

---

## Usage
The script must be run with **root privileges**  since it captures raw network packets.

```bash
sudo python3 tp_module.py [options]
```

### Command‑line options
| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interface` | Network interface to capture from (e.g., `eth0`, `wlan0`, `any`). | `any` |
| `-o, --output`   | Path to the output text file (written in JSON format). | `data.txt` |

---

## Expected Output
The output file is refreshed every second with a JSON object containing the following fields:

| Field | Description |
|-------|-------------|
| `timestamp`         | ISO‑formatted timestamp of the measurement |
| `total_packets`     | Cumulative packet count since start |
| `total_bytes`       | Cumulative byte count since start |
| `packets_per_second`| Packet rate (packets/sec) over the last second |
| `bytes_per_second`  | Byte rate (bytes/sec) over the last second |
| `tcp_packets`       | Cumulative count of TCP packets |
| `udp_packets`       | Cumulative count of UDP packets |
| `icmp_packets`      | Cumulative count of ICMP packets |
| `other_packets`     | Cumulative count of non‑TCP/UDP/ICMP packets |
| `status`            | Always `"online"` while running |

### Example content of `data.txt`
```json
{
  "timestamp": "2025-01-15T14:32:45.123456",
  "total_packets": 1234,
  "total_bytes": 987654,
  "packets_per_second": 45.67,
  "bytes_per_second": 12345.67,
  "tcp_packets": 890,
  "udp_packets": 234,
  "icmp_packets": 56,
  "other_packets": 54,
  "status": "online"
}
```

---

## Stopping the Processor
Press `Ctrl+C` in the terminal. The script will write the final statistics, clean up, and exit.

---
