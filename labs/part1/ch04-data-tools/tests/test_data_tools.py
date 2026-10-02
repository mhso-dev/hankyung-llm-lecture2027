from __future__ import annotations

import json
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx
import pytest
from data_tools import (
    fetch_articles,
    fetch_orders,
    find_customer_orders,
    parse_article_html,
)

DATA = Path(__file__).parents[1] / "data"


@pytest.fixture
def order_database(tmp_path: Path) -> Path:
    database = tmp_path / "orders.db"
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript("""
            CREATE TABLE customers(customer_id TEXT PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE orders(order_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL,
              status TEXT NOT NULL, amount INTEGER NOT NULL,
              FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
            INSERT INTO customers VALUES ('C001', '김하나'), ('C002', '이두리');
            INSERT INTO orders VALUES ('O101', 'C001', 'paid', 32000),
              ('O103', 'C001', 'paid', 27000), ('O102', 'C002', 'pending', 18000);
        """)
    return database


@pytest.fixture
def article_service():
    pages = {p["page"]: p for p in json.loads((DATA / "articles.json").read_text())["pages"]}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            page = int(self.path.split("page=")[-1])
            body = json.dumps(pages[page], ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join()


def test_fetch_orders_filters_status():
    assert [row["order_id"] for row in fetch_orders(DATA / "orders.csv", status="paid")] == ["O101", "O103"]


def test_find_customer_orders_joins_name_and_sorts(order_database: Path):
    rows = find_customer_orders(order_database, "C001")
    assert [(r["order_id"], r["customer_name"]) for r in rows] == [("O101", "김하나"), ("O103", "김하나")]


def test_find_customer_orders_uses_parameters(order_database: Path):
    assert find_customer_orders(order_database, "C001' OR 1=1 --") == []


def test_database_rejects_order_without_customer(order_database: Path):
    with sqlite3.connect(order_database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("INSERT INTO orders VALUES ('O999', 'C999', 'paid', 1000)")


def test_fetch_articles_follows_pages_and_filters(article_service: str):
    assert [r["id"] for r in fetch_articles(article_service, category="economy")] == ["A01", "A03"]


def test_fetch_articles_raises_for_http_error():
    transport = httpx.MockTransport(lambda request: httpx.Response(503, request=request))
    with httpx.Client(transport=transport) as client, pytest.raises(httpx.HTTPStatusError):
        fetch_articles("http://local.test", client=client)


def test_fetch_articles_propagates_timeout():
    def time_out(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("교육용 시간 제한", request=request)

    transport = httpx.MockTransport(time_out)
    with httpx.Client(transport=transport) as client, pytest.raises(httpx.ReadTimeout):
        fetch_articles("http://local.test", client=client)


def test_fetch_articles_rejects_repeated_page():
    def repeat_page(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, request=request, json={"items": [], "next_page": 1})

    transport = httpx.MockTransport(repeat_page)
    with httpx.Client(transport=transport) as client, pytest.raises(ValueError, match="반복된 페이지"):
        fetch_articles("http://local.test", client=client)


def test_article_handoff_matches_distributed_html():
    handoff = json.loads((DATA / "article-text.json").read_text(encoding="utf-8"))
    parsed = parse_article_html((DATA / "article.html").read_text(encoding="utf-8"))
    assert handoff["schema_version"] == "ch04-parsed-article-v1"
    assert handoff["source"] == "labs/part1/ch04-data-tools/data/article.html"
    assert handoff["record"] == parsed


def test_parse_article_rejects_missing_required_field():
    with pytest.raises(ValueError, match="필수 기사 필드"):
        parse_article_html('<article data-id="A10"><h1>제목</h1></article>')
