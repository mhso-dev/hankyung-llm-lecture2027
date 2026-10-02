"""Ch 9 실험 하네스 — 설정 바꾸기 → 실행 → 결과 한 줄 기록, 이것을 한 명령으로.

사용법:
    uv run python harness.py                              # config.yaml 그대로
    uv run python harness.py --set split.chunk_size=1000  # 값 하나만 바꿔서
    uv run python harness.py --set retrieval.k=8 --set name=k8

결과:
    runs/runs.jsonl          — 실행 1회 = 1행 (설정·규모·시간·토큰·비용)
    runs/{run_id}.jsonl      — 질문별 상세 (검색 결과·답변)
Ch 11에서 만드는 지표는 "metrics" 칸에 들어온다. 지금은 비어 있다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from prompts import PROMPTS
from rag import DATA_DIR, build_index, corpus_paths, generate, load_pdfs, search, split_docs

ROOT = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"
CACHE_DIR = ROOT / ".cache"


# ---------------------------------------------------------------- 설정
def load_config(path: Path, overrides: list[str]) -> dict[str, Any]:
    """YAML을 읽고 --set a.b=c 형태의 덮어쓰기를 적용한다."""
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    for item in overrides:
        key, _, raw = item.partition("=")
        node = cfg
        parts = key.split(".")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = yaml.safe_load(raw)  # "1000" → 1000, "[a,b]" → list
    return cfg


def index_key(cfg: dict[str, Any]) -> str:
    """색인 결과를 좌우하는 설정만 골라 해시 — 같은 설정이면 색인을 다시 만들지 않는다."""
    part = {"corpus": cfg["corpus"], "split": cfg["split"], "embedding": cfg["embedding"]}
    return hashlib.sha1(json.dumps(part, sort_keys=True).encode()).hexdigest()[:10]


# ---------------------------------------------------------------- 색인
def get_index(cfg: dict[str, Any]) -> tuple[InMemoryVectorStore, dict[str, Any]]:
    key = index_key(cfg)
    path = CACHE_DIR / f"index-{key}.json"
    meta_path = CACHE_DIR / f"index-{key}.meta.json"
    emb = OpenAIEmbeddings(model=cfg["embedding"]["model"])
    if path.exists():
        return InMemoryVectorStore.load(str(path), emb), json.loads(meta_path.read_text())

    t = time.perf_counter()
    docs = load_pdfs(corpus_paths(cfg["corpus"]["tiers"]))
    chunks = split_docs(docs, **cfg["split"])
    store = build_index(chunks, cfg["embedding"]["model"])
    meta = {
        "n_pages": len(docs),
        "n_chunks": len(chunks),
        "embed_chars": sum(len(c.page_content) for c in chunks),
        "index_seconds": round(time.perf_counter() - t, 2),
    }
    CACHE_DIR.mkdir(exist_ok=True)
    store.dump(str(path))
    meta_path.write_text(json.dumps(meta, ensure_ascii=False))
    return store, meta


# ---------------------------------------------------------------- 질의셋
def load_queries(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    q = cfg["queries"]
    path = (ROOT / q["file"]).resolve() if not Path(q["file"]).is_absolute() else Path(q["file"])
    if not path.exists():
        path = DATA_DIR / "queries.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if q.get("tiers"):
        rows = [r for r in rows if r["tier"] in q["tiers"]]
    if q.get("types"):
        rows = [r for r in rows if r["type"] in q["types"]]
    return rows[: q.get("limit") or len(rows)]


# ---------------------------------------------------------------- 실행
def run(cfg: dict[str, Any]) -> dict[str, Any]:
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S") + "-" + cfg["name"]
    store, index_meta = get_index(cfg)
    queries = load_queries(cfg)
    prompt = PROMPTS[cfg["generation"]["prompt"]]
    k = cfg["retrieval"]["k"]

    details: list[dict[str, Any]] = []
    in_tok = out_tok = 0
    latencies: list[float] = []
    for row in queries:
        t = time.perf_counter()
        hits = search(store, row["question"], k=k)
        res = generate(row["question"], hits, cfg["generation"]["model"], prompt)
        latencies.append(time.perf_counter() - t)
        in_tok += res.input_tokens
        out_tok += res.output_tokens
        details.append(
            {
                "qid": row["qid"],
                "question": row["question"],
                "gold_doc_id": row["doc_id"],  # Ch 11 지표 계산의 정답 — 지금은 기록만
                "retrieved": [
                    {
                        "doc_id": d.metadata["doc_id"],
                        "page": d.metadata["page"],
                        "chunk_id": d.metadata["chunk_id"],  # 쪽만 적으면 청크 단위 실패가 숨는다
                        "score": round(s, 3),
                    }
                    for d, s in hits
                ],
                "answer": res.text,
                "input_tokens": res.input_tokens,
                "output_tokens": res.output_tokens,
            }
        )

    prices = cfg.get("prices", {})
    gen_price = prices.get(cfg["generation"]["model"], {"input": 0, "output": 0})
    emb_price = prices.get(cfg["embedding"]["model"], {"input": 0, "output": 0})
    # 임베딩 토큰은 글자 수 / 1.2로 어림한다 (02절: 한국어 약 500자 ≈ 430 토큰)
    embed_tokens_est = index_meta["embed_chars"] / 1.2
    cost = (
        in_tok * gen_price["input"]
        + out_tok * gen_price["output"]
        + embed_tokens_est * emb_price["input"]
    ) / 1_000_000

    summary = {
        "run_id": run_id,
        "ts": datetime.now(UTC).isoformat(timespec="seconds"),
        "name": cfg["name"],
        "corpus": ",".join(cfg["corpus"]["tiers"]),
        "chunk_size": cfg["split"]["chunk_size"],
        "chunk_overlap": cfg["split"]["chunk_overlap"],
        "embedding": cfg["embedding"]["model"],
        "k": k,
        "gen_model": cfg["generation"]["model"],
        "prompt": cfg["generation"]["prompt"],
        "n_chunks": index_meta["n_chunks"],
        "index_seconds": index_meta["index_seconds"],
        "n_queries": len(queries),
        "latency_mean_s": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "est_cost_usd": round(cost, 4),
        "metrics": {},  # Ch 11에서 채운다 (Recall@k 등)
        "detail_file": f"{run_id}.jsonl",
    }

    RUNS_DIR.mkdir(exist_ok=True)
    (RUNS_DIR / f"{run_id}.jsonl").write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in details) + "\n", encoding="utf-8"
    )
    with (RUNS_DIR / "runs.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")
    return summary


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("config", nargs="?", default="config.yaml")
    ap.add_argument("--set", action="append", default=[], help="a.b=값 형식으로 설정 덮어쓰기")
    args = ap.parse_args(argv)

    cfg = load_config(ROOT / args.config, args.set)
    summary = run(cfg)
    keys = [
        "run_id",
        "chunk_size",
        "k",
        "embedding",
        "prompt",
        "n_chunks",
        "latency_mean_s",
        "input_tokens",
        "output_tokens",
        "est_cost_usd",
    ]
    print(" | ".join(f"{k}={summary[k]}" for k in keys))


if __name__ == "__main__":
    main(sys.argv[1:])
