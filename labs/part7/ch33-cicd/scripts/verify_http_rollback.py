from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

root = Path(__file__).parents[1]
port = 18765


def start(revision: str):
    env = os.environ | {"APP_REVISION": revision}
    process = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)], cwd=root, env=env
    )
    time.sleep(0.2)
    return process


def get(path: str):
    try:
        response = urllib.request.urlopen(f"http://127.0.0.1:{port}{path}")
        return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


observations = []
for revision in ("v1", "v2", "v1"):
    process = start(revision)
    try:
        observations.append(get("/health"))
    finally:
        process.terminate()
        process.wait(timeout=3)

for status, body in observations:
    print(status, body["revision"], body["status"])
assert observations[0][0] == 200
assert observations[1][0] == 503
assert observations[2][0] == 200 and observations[2][1]["revision"] == "v1"
