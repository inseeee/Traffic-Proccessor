import time
import json
import argparse
import threading
import socket
import netifaces 
from datetime import datetime
from scapy.all import sniff, TCP, UDP, ICMP, IP, Ether

class TrafficProcessor:
    def __init__(self, interface="any", output_file="data.txt"):
        self.interface = interface
        self.output_file = output_file
       
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
            print("[TP] Using 'any' interface – direction classification may be unreliable.")
        
        self.running = False
        self.writer_thread = None
        
        print(f"[TP] Output file: {output_file}")
    
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
            time.sleep(0.5)
    
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
    parser = argparse.ArgumentParser(description="Traffic Processor - MVP V1")
    parser.add_argument("-i", "--interface", default="any", help="Network interface to capture from (default: any)")
    parser.add_argument("-o", "--output", default="data.txt", help="Output file path (default: data.txt)")
    args = parser.parse_args()
    
    tp = TrafficProcessor(interface=args.interface, output_file=args.output)
    tp.start()

if __name__ == "__main__":
    main()
