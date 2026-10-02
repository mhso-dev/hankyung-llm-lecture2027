"""Exercise real PostgreSQL authentication with URL-reserved password characters."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
NAME = "ch32-special-secret-check"
PASSWORD = "lesson@:/%password"


def run(*args):
    return subprocess.run(
        args, check=True, capture_output=True, text=True
    ).stdout.strip()


def main():
    run(
        "docker",
        "run",
        "-d",
        "--rm",
        "--name",
        NAME,
        "-e",
        f"POSTGRES_PASSWORD={PASSWORD}",
        "-e",
        "POSTGRES_USER=course",
        "-e",
        "POSTGRES_DB=course",
        "-p",
        "127.0.0.1::5432",
        "pgvector/pgvector:0.8.6-pg17-bookworm",
    )
    try:
        for _ in range(30):
            ready = subprocess.run(
                ["docker", "exec", NAME, "pg_isready", "-U", "course"],
                capture_output=True,
            )
            if ready.returncode == 0:
                break
            time.sleep(1)
        port = int(run("docker", "port", NAME, "5432/tcp").rsplit(":", 1)[1])
        os.environ["DB_HOST"] = "127.0.0.1"
        os.environ["DB_PASSWORD"] = PASSWORD
        os.environ.pop("DB_PASSWORD_FILE", None)
        spec = importlib.util.spec_from_file_location(
            "ch32_app", ROOT / "labs/part7/ch32-docker/app.py"
        )
        app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        with app.psycopg.connect(**app.database_options(), port=port) as connection:
            actual = connection.execute("SELECT 1").fetchone()[0]
        assert actual == 1
        record = {
            "reserved_characters": "@:/%",
            "actual_database_authentication": True,
            "query_result": actual,
        }
        (ROOT / "textbook/part7/qa/ch32-special-secret.json").write_text(
            json.dumps(record, indent=2)
        )
        print("PASS PostgreSQL authentication with reserved password characters")
    finally:
        run("docker", "stop", NAME)


if __name__ == "__main__":
    main()
