const statusDiode = document.getElementById("status-diode");
const primaryLabel = document.getElementById("primary-label");
const primaryValue = document.getElementById("primary-value");
const rateValue = document.getElementById("rate-value");
const packetTypes = document.getElementById("packet-types");
const modeButton = document.getElementById("mode-button");
const packetNodes = {
  tcp_packets: document.getElementById("tcp-packets"),
  udp_packets: document.getElementById("udp-packets"),
  icmp_packets: document.getElementById("icmp-packets"),
  other_packets: document.getElementById("other-packets"),
};

const params = new URLSearchParams(window.location.search);
const defaultSocketUrl =
  window.location.protocol === "file:"
    ? "ws://localhost:8080/ws"
    : `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws`;
const socketUrl = params.get("ws") || defaultSocketUrl;

const stats = {
  status: "offline",
  total_packets: 0,
  total_bytes: 0,
  packets_per_second: 0,
  bytes_per_second: 0,
  tcp_packets: 0,
  udp_packets: 0,
  icmp_packets: 0,
  other_packets: 0,
};

let socket;
let reconnectTimer;
let bytesOnly = false;

function formatNumber(value) {
  return Number(value || 0).toLocaleString();
}

function render() {
  statusDiode.classList.toggle("offline", stats.status !== "online");
  packetTypes.hidden = bytesOnly;
  modeButton.textContent = bytesOnly ? "Show packets" : "Bytes only";

  primaryLabel.textContent = bytesOnly ? "Total bytes" : "Total packets";
  primaryValue.textContent = formatNumber(bytesOnly ? stats.total_bytes : stats.total_packets);
  rateValue.textContent = bytesOnly
    ? `${formatNumber(stats.bytes_per_second)} bytes/s`
    : `${formatNumber(stats.packets_per_second)} packets/s`;

  Object.entries(packetNodes).forEach(([key, node]) => {
    node.textContent = formatNumber(stats[key]);
  });
}

function readPayload(data) {
  if (typeof data !== "string") {
    return;
  }

  try {
    const payload = JSON.parse(data);
    Object.assign(stats, payload);
    render();
  } catch {
    return;
  }
}

function connect() {
  socket = new WebSocket(socketUrl);

  socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ type: "get_stats" }));
  });


  socket.addEventListener("message", (event) => {
    readPayload(event.data);
  });

  socket.addEventListener("close", () => {
    stats.status = "offline";
    render();
    reconnectTimer = window.setTimeout(connect, 1000);
  });

  socket.addEventListener("error", () => {
    socket.close();
  });
}

window.addEventListener("beforeunload", () => {
  window.clearTimeout(reconnectTimer);
  socket?.close();
});

modeButton.addEventListener("click", () => {
  bytesOnly = !bytesOnly;
  render();
});

render();
connect();
