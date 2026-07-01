from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

MAIN_SERVER = "http://cnss:8080"

# Allow mode first: everyone can pass through the gate.
# Later we can add blocked IPs here.
BLOCKED_IPS = set()

# For block test later:
# BLOCKED_IPS = {
#     "10.241.1.122"
# }


class GateHandler(BaseHTTPRequestHandler):
    def send_access_denied(self, client_ip):
        body = f"""
        <h1>Access denied</h1>
        <p>Your IP is blocked or suspicious.</p>
        <p>Your IP: {client_ip}</p>
        <p>Path: {self.path}</p>
        """.encode("utf-8")

        self.send_response(403)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def proxy_request(self):
        client_ip = self.client_address[0]

        print(f"[GATE] IP = {client_ip}", flush=True)
        print(f"[GATE] PATH = {self.path}", flush=True)

        if client_ip in BLOCKED_IPS:
            print(f"[GATE] DENY {client_ip}", flush=True)
            self.send_access_denied(client_ip)
            return

        print(f"[GATE] ALLOW {client_ip}", flush=True)

        target_url = MAIN_SERVER + self.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in ["host", "content-length", "connection"]
        }

        try:
            response = requests.request(
                method=self.command,
                url=target_url,
                headers=headers,
                data=body,
                allow_redirects=False,
                timeout=10
            )

            self.send_response(response.status_code)

            for key, value in response.headers.items():
                if key.lower() not in [
                    "content-encoding",
                    "content-length",
                    "transfer-encoding",
                    "connection"
                ]:
                    self.send_header(key, value)

            self.send_header("Content-Length", str(len(response.content)))
            self.end_headers()
            self.wfile.write(response.content)

        except Exception as e:
            body = f"<h1>Gate error</h1><p>{e}</p>".encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def do_PUT(self):
        self.proxy_request()

    def do_DELETE(self):
        self.proxy_request()

    def do_PATCH(self):
        self.proxy_request()

    def do_OPTIONS(self):
        self.proxy_request()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), GateHandler)
    print("[GATE] Running on 0.0.0.0:8080", flush=True)
    server.serve_forever()
