import time
import json
import argparse
import threading
from datetime import datetime
from scapy.all import sniff, TCP, UDP, ICMP

class TrafficProcessor:
    def __init__(self, interface="any", output_file="data.txt"):
        self.interface = interface
        self.output_file = output_file
        
        #Statistics
        self.packet_cnt = 0
        self.bytes_cnt = 0
        self.tcp_cnt = 0
        self.udp_cnt = 0
        self.icmp_cnt = 0
        self.other_cnt = 0
        self.last_packet_cnt = 0
        self.last_bytes_cnt = 0
        self.last_update_time = time.time()
        
        #States
        self.running = False
        self.writer_thread = None
        
        print(f"[TP] Initialized on interface: {interface}")
        print(f"[TP] Output file: {output_file}")
    
    def packet_handler(self, packet):
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
            "total_packets": self.packet_cnt,
            "total_bytes": self.bytes_cnt,
            "packets_per_second": round(pps, 2),
            "bytes_per_second": round(bps, 2),
            "tcp_packets": self.tcp_cnt,
            "udp_packets": self.udp_cnt,
            "icmp_packets": self.icmp_cnt,
            "other_packets": self.other_cnt,
            "status": "online"
        }
    
    def write_stats(self):
        stats = self.get_stats()
        try:
            with open(self.output_file, 'w') as f:
                json.dump(stats, f)
                f.write('\n')
        except Exception as e:
            print(f"[TP] Error writing to file: {e}")
    
    def writer_loop(self):
        print("[TP] Writer thread started")
        while self.running:
            self.write_stats()
            time.sleep(1)  #Update every second
    
    def start(self):
        if self.running:
            print("[TP] Already running")
            return
    
        self.running = True
        self.writer_thread = threading.Thread(target=self.writer_loop)
        self.writer_thread.daemon = True
        self.writer_thread.start()
        
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
        if self.writer_thread and self.writer_thread.is_alive():
            self.writer_thread.join(timeout=2)
        self.write_stats()
        print("[TP] Stopped")


def main():
    parser = argparse.ArgumentParser(description="Simple Traffic Processor - MVP V1")
    parser.add_argument("-i", "--interface", default="any", help="Network interface to capture from (default: any)")
    parser.add_argument("-o", "--output", default="data.txt", help="Output file path (default: data.txt)")
    args = parser.parse_args()
    
    tp = TrafficProcessor(interface=args.interface, output_file=args.output)
    tp.start()

if __name__ == "__main__":
    main()


