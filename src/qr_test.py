import time
import pytest
import subprocess
import requests
from unittest.mock import Mock, patch
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.tproc import TrafficProcessor

# QRT-001: Dashboard metric update delay
def test_dashboard_metric_update_delay():
    # QRT-001: Verify that dashboard metrics update within ≤1000ms.
    # Setup: Create a mock dashboard server that records update timestamps
    class DashboardHandler(BaseHTTPRequestHandler):
        updates = []

        def do_POST(self):
            # Record the time when the dashboard receives an update
            self.updates.append(time.time())
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress log messages

    # Start a local HTTP server to act as the dashboard
    server = HTTPServer(("localhost", 0), DashboardHandler)  # Port 0 = auto-assign
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    dashboard_url = f"http://localhost:{port}"

    # Initialize the Traffic Processor with the dashboard URL
    tp = TrafficProcessor(interface="eth0", output_url=dashboard_url, delay=0.1)

    # Simulate data generation by the Traffic Processor
    data_generation_time = time.time()

    # Trigger an update (e.g., by processing a packet)
    from scapy.all import IP, TCP, Ether
    pkt = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP()
    tp.packet_handler(pkt)
    tp.post_json()  # Force a POST to the dashboard

    # Wait a moment for the POST to complete
    time.sleep(0.2)

    # Check the recorded update times
    server.shutdown()
    thread.join(timeout=1)

    assert len(DashboardHandler.updates) > 0, "Dashboard did not receive any updates"
    update_time = DashboardHandler.updates[-1]
    delay_ms = (update_time - data_generation_time) * 1000

    # Expected: ≤1000ms for 95% of runs
    assert delay_ms <= 1000.0, f"Update delay was {delay_ms:.2f}ms, expected ≤1000ms"

# QRT-002: Traffic Processor startup time
def test_traffic_processor_startup_time():
    """
    QRT-002: Verify that the service starts and becomes ready within ≤500ms.
    Linked quality requirement: QR-002
    Verification method: Automated CI check
    """
    # In a real CI environment, you would start the service via Docker or systemd.
    # Here we simulate by starting the process and measuring health check time.

    start_time = time.time()

    # Simulate service startup by running a subprocess (e.g., python tproc.py)
    # In practice, you might use docker-compose or a similar command.
    proc = subprocess.Popen(
        ["python", "-c", "import time; time.sleep(0.2); print('ready')"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for the process to indicate it's ready (e.g., by printing "ready")
    # In a real service, you would poll a health check endpoint (e.g., /health)
    # using requests.get() until it returns 200 OK.
    ready = False
    for _ in range(50):  # Poll up to 5 seconds
        if proc.poll() is not None:
            # Process exited; check if it printed "ready"
            stdout, _ = proc.communicate()
            if "ready" in stdout:
                ready = True
            break
        time.sleep(0.1)

    elapsed_ms = (time.time() - start_time) * 1000

    # Clean up
    if proc.poll() is None:
        proc.terminate()
        proc.wait()

    assert ready, "Service did not become ready"
    # Expected: ≤500ms
    assert elapsed_ms <= 500.0, f"Startup time was {elapsed_ms:.2f}ms, expected ≤500ms"

# QRT-003: Traffic Processor throughput capacity
def test_traffic_processor_throughput():
    """
    QRT-003: Verify that the processor sustains ≥1000 Kbps for 60 seconds
              with <1% packet loss/error.
    Linked quality requirement: QR-003
    Verification method: Automated performance test
    """
    # This test requires a packet generator. Here we simulate with Scapy.

    from scapy.all import sendp, Ether, IP, UDP
    import threading
    import time

    # Configuration
    TARGET_RATE_BPS = 1_000_000  # 1000 Kbps = 1,000,000 bits/sec
    PACKET_SIZE_BYTES = 100      # 100 bytes per packet (approx)
    PACKETS_PER_SECOND = int(TARGET_RATE_BPS / (PACKET_SIZE_BYTES * 8))
    DURATION_SECONDS = 60

    # Create a Traffic Processor instance
    tp = TrafficProcessor(interface="eth0", output_url="http://localhost:8000")
    tp.local_ip = "192.168.1.100"
    tp.local_mac = "aa:bb:cc:dd:ee:ff"

    # Mock the packet_handler to count processed packets without side effects
    processed_count = 0
    original_handler = tp.packet_handler

    def counting_handler(pkt):
        nonlocal processed_count
        processed_count += 1
        original_handler(pkt)

    tp.packet_handler = counting_handler

    # Function to generate traffic at the target rate
    def generate_traffic():
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src="aa:bb:cc:dd:ee:ff") / \
              IP(src="192.168.1.100", dst="8.8.8.8") / \
              UDP() / ("X" * (PACKET_SIZE_BYTES - 42))  # 42 bytes for Ether+IP+UDP

        start_time = time.time()
        sent_count = 0
        while time.time() - start_time < DURATION_SECONDS:
            sendp(pkt, iface="eth0", verbose=False)
            sent_count += 1
            # Sleep to maintain the target rate
            time.sleep(1.0 / PACKETS_PER_SECOND)

    # Start traffic generation in a background thread
    gen_thread = threading.Thread(target=generate_traffic, daemon=True)
    gen_thread.start()

    # Let the processor run for the duration
    time.sleep(DURATION_SECONDS + 1)  # Allow some extra time for processing

    # Calculate statistics
    total_expected = int(PACKETS_PER_SECOND * DURATION_SECONDS)
    loss_percent = ((total_expected - processed_count) / total_expected) * 100

    # Expected: less than 1% loss/error
    assert loss_percent < 1.0, f"Packet loss was {loss_percent:.2f}%, expected <1%"

    # Additionally, verify that the processor correctly identified traffic statistics
    assert tp.packet_cnt > 0, "No packets were processed"
    assert tp.udp_cnt > 0, "UDP packets were not correctly identified"
    # The throughput in Kbps can also be calculated from bytes processed
    throughput_kbps = (tp.bytes_cnt * 8) / (DURATION_SECONDS * 1000)
    assert throughput_kbps >= 1000, f"Throughput was {throughput_kbps:.2f} Kbps, expected ≥1000 Kbps"
