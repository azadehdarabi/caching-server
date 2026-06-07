from http.server import BaseHTTPRequestHandler

import requests

from .cache_manager import CacheManager

_HOP_BY_HOP = {"transfer-encoding", "connection", "keep-alive", "te", "trailers", "upgrade"}


def _safe_headers(headers: dict) -> dict:
    return {k: v for k, v in headers.items() if k.lower() not in _HOP_BY_HOP}


class ProxyServer(BaseHTTPRequestHandler):

    def __init__(self, origin, cache: CacheManager, *args, **kwargs):
        self.origin = origin
        self.cache = cache
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url = self.origin + self.path

        cached_body, cached_header = self.cache.get(url)
        if cached_body:
            self.send_response(200)
            for key, value in cached_header.items():
                self.send_header(key, value)
            self.send_header("X-Cache", "HIT")
            self.end_headers()
            self.wfile.write(cached_body)
            return

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            body = response.content
            headers = _safe_headers(dict(response.headers))
            self.cache.set(url, body, headers)

            self.send_response(response.status_code)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("X-Cache", "MISS")
            self.end_headers()
            self.wfile.write(body)

        except requests.exceptions.ConnectionError:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(b"Bad gateway: could not connect to origin")

        except requests.exceptions.Timeout:
            self.send_response(504)
            self.end_headers()
            self.wfile.write(b"Gateway timeout: origin took too long to respond")

        except requests.exceptions.RequestException as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Bad gateway: {str(e)}".encode())
