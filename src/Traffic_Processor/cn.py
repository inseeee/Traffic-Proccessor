"""CommunicationNode

Continuously reads json from a text file and sends batches to an HTTP endpoint.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from urllib import request, error

def read_json(path: str) -> dict:
    """Read and return JSON object from `path`."""
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e


def post_json(url: str, payload: dict, timeout: float = 5.0) -> tuple[int, str]:
	"""POST `payload` as JSON to `url`. Returns (status_code, response_body).
	Uses urllib from the standard library to avoid extra dependencies.
	"""
	data = json.dumps(payload).encode("utf-8")
	req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
	try:
		with request.urlopen(req, timeout=timeout) as resp:
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


def send_numbers_batch(file_path: str, url: str, retries: int = 3) -> None:
	payload = read_json(file_path)
	attempt = 0
	while True:
		attempt += 1
		try:
			status, body = post_json(url, payload)
		except Exception:
			status = None

		if status is not None and 200 <= status < 300:
			print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent batch -> {url} (status {status})")
			return
		else:
			print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send batch (attempt {attempt}): status={status}")
			if attempt >= retries:
				print(f"Giving up after {retries} attempts", file=sys.stderr)
				return
			wait = 0.5 * attempt
			print(f"Retrying in {wait} seconds...")
			time.sleep(wait)


def send_numbers_loop(file_path: str, url: str, delay: float = 1.0, retries: int = 3) -> None:
	"""Loops indefinitely, pausing `delay` seconds between reads.

	Sends each batch of numbers read from `file_path` to `url`.
	"""
	print(f"Starting continuous loop: reading {file_path} every {delay}s, sending to {url}")
	while True:
		try:
			send_numbers_batch(file_path, url, retries=retries)
		except Exception as exc:
			print(f"Error reading/sending batch: {exc}", file=sys.stderr)
		time.sleep(delay)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
	p = argparse.ArgumentParser(description="Continuously send numbers from a text file to an HTTP endpoint as JSON batch.")
	p.add_argument("--file", "-f", type=str, default="data.txt", help="Path to input json")
	p.add_argument("--url", "-u", type=str, default="http://localhost:8000", help="HTTP endpoint URL to POST batches to")
	p.add_argument("--delay", "-d", type=float, default=0.5, help="Delay in seconds between loop iterations (default 0.5)")
	p.add_argument("--retries", "-r", type=int, default=3, help="Retries per batch on failure (default 3)")
	return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
	args = _parse_args(argv)
	try:
		send_numbers_loop(args.file, args.url, delay=args.delay, retries=args.retries)
	except KeyboardInterrupt:
		print("\nShutting down...", file=sys.stderr)
		return 0
	except Exception as exc:
		print(f"Error: {exc}", file=sys.stderr)
		return 2
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
