import logging
import os
from pathlib import Path

import psycopg
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("course-api")
app = FastAPI(title="Ch32 Docker API")


def read_secret(name: str) -> str:
    """Read a Compose secret file, with an environment fallback for local study."""
    file_path = os.getenv(f"{name}_FILE")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    return os.getenv(name, "")


def database_options() -> dict[str, str]:
    # 비밀번호의 특수 문자가 주소 구분자로 해석되지 않도록 인자를 분리합니다.
    return {"user": "course", "password": read_secret("DB_PASSWORD"),
            "host": os.getenv("DB_HOST", "localhost"), "dbname": "course"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    try:
        with psycopg.connect(**database_options(), connect_timeout=2) as connection:
            connection.execute("SELECT 1")
    except psycopg.Error as exc:
        logger.warning("database_not_ready error_type=%s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="database not ready") from exc
    return {"status": "ready"}


@app.get("/vector-count")
def vector_count() -> dict[str, int]:
    with psycopg.connect(**database_options()) as connection:
        count = connection.execute("SELECT count(*) FROM course_vectors").fetchone()[0]
    logger.info("vector_count=%s", count)
    return {"count": count}
