import time
import json
import argparse
import threading
import netifaces 
from datetime import datetime
from scapy.all import sniff, TCP, UDP, ICMP, IP, Ether
from urllib import request, error

class TrafficProcessor:
    def __init__(self, interface="any", output_url="http://localhost:8000", delay=0.5):
        self.interface = interface
        self.output_url = output_url
        self.delay = delay
       
        self.packet_cnt = 0
        self.bytes_cnt = 0
        self.tcp_cnt = 0
        self.udp_cnt = 0
        self.icmp_cnt = 0
        self.other_cnt = 0
        
        # Direction-specific statistics
        self.incoming_packets = 0
        self.outgoing_packets = 0
        self.incoming_bytes = 0
        self.outgoing_bytes = 0
        
        # Rate calculation helpers
        self.last_packet_cnt = 0
        self.last_bytes_cnt = 0
        self.last_update_time = time.time()
        
        self.local_ip = None
        self.local_mac = None
        if interface != "any":
            try:
                addrs = netifaces.ifaddresses(interface)
                ipv4 = addrs.get(netifaces.AF_INET, [])
                if ipv4:
                    self.local_ip = ipv4[0]['addr']
                mac = addrs.get(netifaces.AF_LINK, [])
                if mac:
                    self.local_mac = mac[0]['addr']
                print(f"[TP] Local IP: {self.local_ip}, MAC: {self.local_mac}")
            except Exception as e:
                print(f"[TP] Could not get interface info: {e}")
        else:
            print("[TP] Using 'any' interface - direction classification may be unreliable.")
        
        self.running = False
        self.sender_thread = None
        
        print(f"[TP] Output url: {output_url}")
    
    def packet_handler(self, packet):
        try:
            self.packet_cnt += 1
            self.bytes_cnt += len(packet)
        
            if packet.haslayer(TCP):
                self.tcp_cnt += 1
            elif packet.haslayer(UDP):
                self.udp_cnt += 1
            elif packet.haslayer(ICMP):
                self.icmp_cnt += 1
            else:
                self.other_cnt += 1
            
            if self.local_ip:
                if packet.haslayer(IP):
                    ip = packet[IP]
                    if ip.dst == self.local_ip:
                        self.incoming_packets += 1
                        self.incoming_bytes += len(packet)
                    elif ip.src == self.local_ip:
                        self.outgoing_packets += 1
                        self.outgoing_bytes += len(packet)
            elif self.local_mac and packet.haslayer(Ether):
                eth = packet[Ether]
                if eth.dst == self.local_mac:
                    self.incoming_packets += 1
                    self.incoming_bytes += len(packet)
                elif eth.src == self.local_mac:
                    self.outgoing_packets += 1
                    self.outgoing_bytes += len(packet)
            # If no direction info, counters stay unchanged
        except Exception as e:
            print(f"[TP] Error processing packet: {e}")
    
    def get_stats(self):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        pps = (self.packet_cnt - self.last_packet_cnt) / elapsed if elapsed > 0 else 0
        bps = (self.bytes_cnt - self.last_bytes_cnt) / elapsed if elapsed > 0 else 0
        self.last_packet_cnt = self.packet_cnt
        self.last_bytes_cnt = self.bytes_cnt
        self.last_update_time = current_time
        
        return {
            "timestamp": datetime.now().isoformat(),
            "incoming_packets": self.incoming_packets,
            "outgoing_packets": self.outgoing_packets,
            "incoming_bytes": self.incoming_bytes,
            "outgoing_bytes": self.outgoing_bytes,
            "packets_per_second": round(pps, 2),
            "bytes_per_second": round(bps, 2),
            "tcp_packets": self.tcp_cnt,
            "udp_packets": self.udp_cnt,
            "icmp_packets": self.icmp_cnt,
            "other_packets": self.other_cnt,
            "status": "online"
        }
    
    def post_json(self) -> tuple[int, str]:
        stats = self.get_stats()
        data = json.dumps(stats).encode("utf-8")
        req = request.Request(self.output_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with request.urlopen(req, timeout=0.5) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.getcode(), body
        except error.HTTPError as he:
            # HTTP error with response body
            try:
                body = he.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return he.code, body
        except Exception:
            raise
    
    def send_stats(self):
        try:
            status, body = self.post_json()
        except Exception:
            status = None
        if status is not None and 200 <= status < 300:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent batch (status {status})")
            return
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send batch: status={status}")
    
    def sender_loop(self):
        print("[TP] Sender thread started")
        while self.running:
            self.send_stats()
            time.sleep(self.delay)
    
    def start(self):
        if self.running:
            print("[TP] Already running")
            return
    
        self.running = True
        self.sender_thread = threading.Thread(target=self.sender_loop)
        self.sender_thread.daemon = True
        self.sender_thread.start()
        
        print(f"[TP] Starting packet capture on {self.interface}...")
        print("[TP] Press Ctrl+C to stop")
        try:
            sniff(iface=self.interface, prn=self.packet_handler, store=False)
        except KeyboardInterrupt:
            print("\n[TP] Stopping...")
        finally:
            self.stop()
    
    def stop(self):
        self.running = False
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=2)
        self.send_stats()
        print("[TP] Stopped")


def main():
    parser = argparse.ArgumentParser(description="Traffic Processor")
    parser.add_argument("-i", "--interface", type=str, default="any", help="Network interface to capture from (default: any), may affect direction tracking")
    parser.add_argument("-u", "--url", type=str, default="http://localhost:8000", help="HTTP endpoint URL to POST batches to")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay in seconds between loop iterations (default 0.5)")
    args = parser.parse_args()
    
    tp = TrafficProcessor(interface=args.interface, output_url=args.url, delay=args.delay)
    tp.start()

if __name__ == "__main__":
    main()
