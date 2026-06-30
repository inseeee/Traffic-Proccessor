from flask import Flask, request, Response
import requests

app = Flask(__name__, static_url_path="/_gate_static")

MAIN_SERVER = "http://cnss:8080"

BLOCKED_IPS = set()


# BLOCKED_IPS = {
#     "10.241.1.122"
# }


def proxy_request(target_server):
    url = target_server + request.full_path

    if url.endswith("?"):
        url = url[:-1]

    response = requests.request(
        method=request.method,
        url=url,
        headers={
            key: value
            for key, value in request.headers
            if key.lower() != "host"
        },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    ]

    headers = [
        (name, value)
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(response.content, response.status_code, headers)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def gate(path):
    client_ip = request.remote_addr

    print(f"[GATE] IP = {client_ip}", flush=True)
    print(f"[GATE] PATH = {request.path}", flush=True)

    if client_ip in BLOCKED_IPS:
        print(f"[GATE] DENY {client_ip}", flush=True)
        return Response(
            f"""
            <h1>Access denied</h1>
            <p>Your IP is blocked or suspicious.</p>
            <p>Your IP: {client_ip}</p>
            <p>Path: {request.path}</p>
            """,
            status=403,
            content_type="text/html"
        )

    print(f"[GATE] ALLOW {client_ip}", flush=True)
    return proxy_request(MAIN_SERVER)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
