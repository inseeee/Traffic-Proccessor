import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from urllib import error
from datetime import datetime
import netifaces
from scapy.all import IP, TCP, UDP, ICMP, Ether

from tproc import TrafficProcessor


@pytest.fixture
def mock_interface_info():
    """Mock netifaces to return a fake IP and MAC for a specific interface."""
    with patch("netifaces.ifaddresses") as mock_ifaddrs:
        # Simulate interface 'eth0'
        mock_ifaddrs.return_value = {
            netifaces.AF_INET: [{"addr": "192.168.1.100"}],
            netifaces.AF_LINK: [{"addr": "aa:bb:cc:dd:ee:ff"}],
        }
        yield mock_ifaddrs


def test_initialization_with_interface(mock_interface_info):
    """Test that TrafficProcessor obtains local IP and MAC from netifaces."""
    tp = TrafficProcessor(interface="eth0", output_url="http://test", delay=0.5)

    assert tp.local_ip == "192.168.1.100"
    assert tp.local_mac == "aa:bb:cc:dd:ee:ff"
    assert tp.interface == "eth0"
    assert tp.output_url == "http://test"
    assert tp.delay == 0.5
    # Check that counters start at zero
    assert tp.packet_cnt == 0
    assert tp.incoming_packets == 0
    assert tp.outgoing_packets == 0


def test_packet_handler_statistics():
    """Test packet_handler increments counters and directions correctly."""
    tp = TrafficProcessor(interface="eth0", output_url="http://test")
    tp.local_ip = "192.168.1.100"
    tp.local_mac = "aa:bb:cc:dd:ee:ff"

    # Create a mock TCP packet from external to local
    from scapy.all import IP, TCP, Ether

    # Incoming TCP packet
    pkt_in = Ether(src="ff:ff:ff:ff:ff:ff", dst="aa:bb:cc:dd:ee:ff") / IP(src="10.0.0.1", dst="192.168.1.100") / TCP()
    # Outgoing UDP packet
    pkt_out = Ether(src="aa:bb:cc:dd:ee:ff", dst="ff:ff:ff:ff:ff:ff") / IP(src="192.168.1.100", dst="8.8.8.8") / UDP()
    # ICMP packet (direction unknown because local IP not set? but we have local IP so it works)
    pkt_icmp = IP(src="1.1.1.1", dst="192.168.1.100") / ICMP()

    tp.packet_handler(pkt_in)
    tp.packet_handler(pkt_out)
    tp.packet_handler(pkt_icmp)

    assert tp.packet_cnt == 3
    assert tp.bytes_cnt == len(pkt_in) + len(pkt_out) + len(pkt_icmp)
    assert tp.tcp_cnt == 1
    assert tp.udp_cnt == 1
    assert tp.icmp_cnt == 1
    assert tp.other_cnt == 0

    assert tp.incoming_packets == 2  # TCP and ICMP have dst==local_ip
    assert tp.outgoing_packets == 1
    assert tp.incoming_bytes == len(pkt_in) + len(pkt_icmp)
    assert tp.outgoing_bytes == len(pkt_out)


def test_post_json_success_and_failure():
    """Test post_json handles successful response and HTTP errors."""
    tp = TrafficProcessor(output_url="http://localhost:8000")
    # Mock the urlopen context manager
    with patch("urllib.request.urlopen") as mock_urlopen:
        # --- Success case ---
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b'{"status":"ok"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        status, body = tp.post_json()
        assert status == 200
        assert body == '{"status":"ok"}'

        # Verify request was called with correct data and headers
        args, kwargs = mock_urlopen.call_args
        request = args[0]  # The Request object
        assert request.get_method() == "POST"
        assert request.headers.get("Content-type") == "application/json"
        # The data should be a JSON encoded stats dict
        data = json.loads(request.data.decode())
        assert "timestamp" in data
        assert data["status"] == "online"

        # --- HTTP error case ---
        # Reset mock and raise HTTPError
        mock_urlopen.reset_mock()
        # HTTPError takes (url, code, msg, hdrs, fp)
        error_response = Mock()
        error_response.read.return_value = b'{"error":"bad request"}'
        mock_urlopen.side_effect = error.HTTPError(
            url="http://localhost:8000", code=400, msg="Bad Request", hdrs={}, fp=error_response
        )

        status, body = tp.post_json()
        assert status == 400
        assert body == '{"error":"bad request"}'

        # --- Non-HTTP exception ---
        mock_urlopen.reset_mock()
        mock_urlopen.side_effect = ConnectionError("Network unreachable")
        with pytest.raises(ConnectionError):
            tp.post_json()
