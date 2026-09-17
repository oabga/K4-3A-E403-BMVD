#!/usr/bin/env python3
"""Demo CP3: AI thật (trả lời) + MOCK fetch. Mở http://127.0.0.1:8777"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extend import answer_for, load_dotenv  # noqa: E402

HOST, PORT = "127.0.0.1", 8777
HTML = Path(__file__).resolve().parent / "static" / "index.html"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("CP3 demo %s\n" % (fmt % args))

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML.read_bytes(), "text/html; charset=utf-8")
            return
        if self.path == "/health":
            load_dotenv()
            import os

            ai = bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY"))
            payload = {"ai_that": ai, "fetch": "MOCK", "retry": "MOCK"}
            raw = json.dumps(payload).encode()
            self._send(200, raw, "application/json")
            return
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/ask":
            self._send(404, b"not found", "text/plain")
            return
        n = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        q = (data.get("question") or "").strip()
        policy = data.get("fetch_policy") or "allow_mock"
        if not q:
            self._send(400, b'{"error":"empty"}', "application/json")
            return
        result = answer_for(q, policy)
        raw = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self._send(200, raw, "application/json; charset=utf-8")


if __name__ == "__main__":
    load_dotenv()
    print(f"CP3 live http://{HOST}:{PORT}  — AI thật nếu có .env key; fetch=MOCK")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
