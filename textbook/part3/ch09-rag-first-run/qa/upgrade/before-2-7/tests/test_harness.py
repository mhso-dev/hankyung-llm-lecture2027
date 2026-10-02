"""06절 하네스 검증 — 설정 덮어쓰기·색인 키·질의셋 필터. API 호출 없음."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import ROOT, index_key, load_config, load_queries


def test_set_overrides_nested_value_with_type() -> None:
    cfg = load_config(ROOT / "config.yaml", ["split.chunk_size=1000", "corpus.tiers=[easy]"])
    assert cfg["split"]["chunk_size"] == 1000  # 문자열이 아니라 정수
    assert cfg["corpus"]["tiers"] == ["easy"]


def test_index_key_ignores_generation_settings() -> None:
    base = load_config(ROOT / "config.yaml", [])
    only_k = load_config(ROOT / "config.yaml", ["retrieval.k=8", "generation.prompt=helpful"])
    other_chunk = load_config(ROOT / "config.yaml", ["split.chunk_size=1000"])
    assert index_key(base) == index_key(only_k)  # k·프롬프트는 색인과 무관
    assert index_key(base) != index_key(other_chunk)


def test_load_queries_filters_and_limits() -> None:
    cfg = load_config(ROOT / "config.yaml", ["queries.limit=2", "queries.types=[unanswerable]"])
    rows = load_queries(cfg)
    assert len(rows) == 2
    assert all(r["type"] == "unanswerable" and r["tier"] == "easy" for r in rows)
