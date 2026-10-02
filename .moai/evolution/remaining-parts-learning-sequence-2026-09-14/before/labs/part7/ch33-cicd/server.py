from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REVISION = os.getenv("APP_REVISION", "v1")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        healthy = REVISION == "v1"
        status = 200 if self.path == "/answer" or healthy else 503
        body = {"revision": REVISION, "status": "ok" if healthy else "regressed"}
        if self.path == "/answer":
            body["answer"] = "근거를 확인했습니다." if healthy else "근거 없이 생성했습니다."
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode())

    def log_message(self, format, *args):  # noqa: A002
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
