"""Ch 4에서 만들고 Ch 19 도구로 감쌀 수 있는 데이터 조회 함수."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
from bs4 import BeautifulSoup


def fetch_orders(csv_path: str | Path, *, status: str | None = None) -> list[dict[str, Any]]:
    """CSV 주문을 읽고 선택한 상태의 행을 사전 목록으로 반환합니다."""
    orders = pd.read_csv(csv_path, dtype={"order_id": "string", "customer_id": "string"})
    if status is not None:
        orders = orders.loc[orders["status"] == status]
    return orders.to_dict(orient="records")


def find_customer_orders(database: str | Path, customer_id: str) -> list[dict[str, Any]]:
    """매개변수 SQL로 한 고객의 주문을 금액 내림차순 조회합니다."""
    query = """
        SELECT o.order_id, c.name AS customer_name, o.status, o.amount
        FROM orders AS o JOIN customers AS c ON c.customer_id = o.customer_id
        WHERE c.customer_id = ? ORDER BY o.amount DESC, o.order_id
    """
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(query, (customer_id,))]


def fetch_articles(base_url: str, *, category: str | None = None, timeout: float = 2.0,
                   client: httpx.Client | None = None) -> list[dict[str, Any]]:
    """next_page가 없어질 때까지 로컬 REST 학습 서비스의 기사를 조회합니다."""
    owns_client = client is None
    active_client = client or httpx.Client(timeout=timeout)
    page: int | None = 1
    seen_pages: set[int] = set()
    articles: list[dict[str, Any]] = []
    try:
        while page is not None:
            if page in seen_pages:
                raise ValueError(f"반복된 페이지: {page}")
            seen_pages.add(page)
            response = active_client.get(f"{base_url.rstrip('/')}/articles", params={"page": page})
            response.raise_for_status()
            payload = response.json()
            articles.extend(payload["items"])
            page = payload.get("next_page")
    finally:
        if owns_client:
            active_client.close()
    if category is not None:
        articles = [article for article in articles if article.get("category") == category]
    return articles


def parse_article_html(html: str) -> dict[str, str]:
    """HTML 기사의 ID·제목·요약·발행일과 모델 입력 텍스트를 반환합니다."""
    article = BeautifulSoup(html, "lxml").select_one("article")
    if article is None or article.h1 is None:
        raise ValueError("필수 기사 요소가 없습니다.")
    summary = article.select_one(".summary")
    published = article.time.get("datetime") if article.time else None
    article_id = article.get("data-id")
    if not article_id or summary is None or not published:
        raise ValueError("필수 기사 필드가 없습니다.")
    title = article.h1.get_text(strip=True)
    summary_text = summary.get_text(strip=True)
    return {
        "id": article_id,
        "title": title,
        "summary": summary_text,
        "published": published,
        "text": f"{title}\n{summary_text}",
    }
