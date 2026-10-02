import argparse
from pathlib import Path

import _paths  # noqa: F401

from document_processing import (
    estimate_embedding_cost,
    load_pdf,
    preflight_corpus,
    split_recursive,
    split_structural,
    split_token,
)
from experiment import corpus_paths, load_questions, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend",
        choices=["educational-feature-hash", "openai"],
        default="educational-feature-hash",
    )
    parser.add_argument("--corpus", type=Path, help="PDF를 재귀 검색할 코퍼스 디렉터리")
    parser.add_argument("--queries", type=Path, help="Ch 9 형식 JSONL 질의 파일")
    parser.add_argument("--require-count", type=int, default=0)
    args = parser.parse_args()
    paths = sorted(args.corpus.rglob("*.pdf")) if args.corpus else corpus_paths()
    status = preflight_corpus(paths, required=100)
    if args.require_count and preflight_corpus(paths, required=args.require_count)["ready"] is False:
        raise SystemExit(
            f"corpus preflight failed: required={args.require_count}, unique_available={status['available']}"
        )
    docs = [doc for path in paths for doc in load_pdf(path)]
    chunk_sets = [
        split_recursive(docs, chunk_size=800, overlap=100),
        split_token(docs, chunk_tokens=400, overlap_tokens=50),
        split_structural(docs, max_chars=800),
    ]
    query_texts = [row["question"] for row in load_questions(args.queries)] * 3
    all_chunk_texts = [chunk.page_content for chunks in chunk_sets for chunk in chunks]
    estimated_texts = all_chunk_texts + query_texts
    small = estimate_embedding_cost(
        estimated_texts, usd_per_million_tokens=0.02
    )
    large = estimate_embedding_cost(
        estimated_texts, usd_per_million_tokens=0.13
    )
    print(f"corpus_preflight=required:{status['required']},available:{status['available']},ready:{status['ready']}")
    print("baseline=18 digital PDFs; scanned variants excluded; no duplicated documents")
    print(f"cost_preflight_small_usd={small['estimated_usd']:.6f}")
    print(f"cost_preflight_large_usd={large['estimated_usd']:.6f}")
    print("pricing_assumption_usd_per_million_tokens=small:0.02,large:0.13 (verify before API run)")
    print("cost_scope=all 3 chunk sets x 2 candidates plus 3 query passes per candidate")
    summaries = run_experiment(
        backend=args.backend, paths=paths, query_file=args.queries
    )
    print(f"runs={len(summaries)} backend={args.backend}")
    for row in summaries:
        print(
            f"{row['chunk_method']} x {row['embedding_candidate']}: "
            f"chunks={row['n_chunks']} first={row['first_pass_cache_hits']}/{row['first_pass_cache_misses']} "
            f"second={row['second_pass_cache_hits']}/{row['second_pass_cache_misses']} metrics={row['metrics']}"
        )


if __name__ == "__main__":
    main()
