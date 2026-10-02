"""3가지 청킹 × 2가지 임베딩 후보를 Ch 9 호환 JSONL로 기록한다."""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from document_processing import (
    EmbeddingCache,
    educational_feature_vectors,
    load_pdf,
    preflight_corpus,
    split_recursive,
    split_structural,
    split_token,
    top_k,
)

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[2]
CORPUS_ROOT = ROOT.parents[1] / "data" / "rag-corpus"
RUNS_DIR = ROOT / "runs" / "examples"
CACHE_DIR = ROOT / ".cache" / "embeddings-v2"
MODELS = ("text-embedding-3-small", "text-embedding-3-large")
QUERY_IDS = {"Q001", "Q037", "Q088"}


def load_questions(path: Path | None = None) -> list[dict[str, Any]]:
    is_default = path is None
    path = path or CORPUS_ROOT / "queries.jsonl"
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    return [row for row in rows if row["qid"] in QUERY_IDS] if is_default else rows


def corpus_paths() -> list[Path]:
    return sorted(
        path
        for tier in ("easy", "medium", "hard")
        for path in (CORPUS_ROOT / "pdf" / tier).glob("*.pdf")
    )


def make_embedder(backend: str, model: str):
    if backend == "educational-feature-hash":
        return educational_feature_vectors, "educational-feature-hash", "v1"
    if backend != "openai":
        raise ValueError("backend는 educational-feature-hash 또는 openai여야 합니다")
    load_dotenv(PROJECT_ROOT / ".env")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 없어 OpenAI 임베딩을 실행하지 못했습니다")
    client = OpenAI()

    def embed(texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(model=model, input=texts)
        return [row.embedding for row in response.data]

    return embed, "openai", "api-current"


def run_experiment(
    *,
    backend: str,
    output_dir: Path = RUNS_DIR,
    paths: list[Path] | None = None,
    query_file: Path | None = None,
) -> list[dict[str, Any]]:
    paths = corpus_paths() if paths is None else paths
    if not paths:
        raise ValueError("실험할 PDF가 없습니다")
    status = preflight_corpus(paths)
    corpus_fingerprint = hashlib.sha256(
        "".join(sorted(hashlib.sha256(path.read_bytes()).hexdigest() for path in paths)).encode()
    ).hexdigest()
    docs = [doc for path in paths for doc in load_pdf(path)]
    splitters = {
        "recursive": (
            {"chunk_size": 800, "overlap": 100},
            lambda: split_recursive(docs, chunk_size=800, overlap=100),
        ),
        "token": (
            {"chunk_tokens": 400, "overlap_tokens": 50, "encoding": "cl100k_base"},
            lambda: split_token(docs, chunk_tokens=400, overlap_tokens=50),
        ),
        "structural": (
            {"max_chars": 800},
            lambda: split_structural(docs, max_chars=800),
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    cache = EmbeddingCache(CACHE_DIR)
    summaries = []
    questions = load_questions(query_file)
    for split_name, (split_config, split) in splitters.items():
        chunks = split()
        for model in MODELS:
            started = time.perf_counter()
            embedder, provider, version = make_embedder(backend, model)
            dimensions = 128 if provider == "educational-feature-hash" else {
                "text-embedding-3-small": 1536,
                "text-embedding-3-large": 3072,
            }[model]
            vectors, first = cache.embed(
                [chunk.page_content for chunk in chunks],
                provider=provider,
                model=model,
                version=version,
                dimensions=dimensions,
                embedder=embedder,
            )
            _, second = cache.embed(
                [chunk.page_content for chunk in chunks],
                provider=provider,
                model=model,
                version=version,
                dimensions=dimensions,
                embedder=embedder,
            )
            run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f") + f"-{split_name}-{model}"
            details = [
                {
                    "qid": row["qid"],
                    "question": row["question"],
                    "gold_doc_id": row["doc_id"],
                    "retrieved": top_k(row["question"], chunks, vectors, embedder, 4),
                    "metrics": {},
                }
                for row in questions
            ]
            detail_file = output_dir / f"{run_id}.jsonl"
            detail_file.write_text(
                "\n".join(json.dumps(row, ensure_ascii=False) for row in details) + "\n",
                encoding="utf-8",
            )
            summary = {
                "run_id": run_id,
                "ts": datetime.now(UTC).isoformat(timespec="seconds"),
                "corpus_required": status["required"],
                "corpus_available": status["available"],
                "corpus_ready": status["ready"],
                "baseline_scope": f"{len(paths)} unique-input digital PDFs",
                "corpus_fingerprint_sha256": corpus_fingerprint,
                "chunk_method": split_name,
                "split_config": split_config,
                "embedding_candidate": model,
                "embedding_backend": provider,
                "embedding_version": version,
                "embedding_dimensions": dimensions,
                "n_pages": len(docs),
                "n_chunks": len(chunks),
                "first_pass_cache_hits": first.hits,
                "first_pass_cache_misses": first.misses,
                "second_pass_cache_hits": second.hits,
                "second_pass_cache_misses": second.misses,
                "elapsed_s": round(time.perf_counter() - started, 3),
                "n_queries": len(questions),
                "query_ids": [row["qid"] for row in questions],
                "metrics": {},
                "detail_file": detail_file.name,
                "model_selection_status": "[[미정: 임베딩 모델]]",
            }
            summaries.append(summary)
    (output_dir / "runs.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in summaries) + "\n",
        encoding="utf-8",
    )
    return summaries
