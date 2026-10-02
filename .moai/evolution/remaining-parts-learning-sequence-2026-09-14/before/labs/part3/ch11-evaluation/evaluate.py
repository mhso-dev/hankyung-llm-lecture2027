from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

from pypdf import PdfReader


METRIC_KEYS = ("recall_at_5", "recall_at_50", "precision_at_5", "ndcg_at_5")


def find_repo_root(start: Path) -> Path:
    for folder in (start, *start.parents):
        if (folder / "labs" / "data" / "rag-corpus" / "manifest.json").exists():
            return folder
    raise FileNotFoundError("labs/data/rag-corpus를 찾지 못했습니다.")


def tokens(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text.lower())
    words = re.findall(r"[가-힣a-z0-9]+", normalized)
    compact = re.sub(r"[^가-힣a-z0-9]", "", normalized)
    return words + [compact[i : i + 2] for i in range(max(0, len(compact) - 1))]


def load_pages(corpus: Path) -> list[dict]:
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    pages = []
    for item in manifest:
        if item["tier"] == "scanned":
            continue
        pdf_path = corpus / item["file"]
        for page_no, page in enumerate(PdfReader(pdf_path).pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"doc_id": item["doc_id"], "page": page_no, "text": text})
    return pages


def corpus_fingerprint(corpus: Path) -> str:
    manifest_bytes = (corpus / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    digest = hashlib.sha256(manifest_bytes)
    for item in sorted(manifest, key=lambda row: row["file"]):
        if item["tier"] != "scanned":
            digest.update((corpus / item["file"]).read_bytes())
    return digest.hexdigest()


def search(question: str, pages: list[dict], limit: int = 50) -> list[dict]:
    query_counts = Counter(tokens(question))
    scored = []
    for page in pages:
        page_counts = Counter(tokens(page["text"]))
        overlap = sum(min(count, page_counts[token]) for token, count in query_counts.items())
        score = overlap / math.sqrt(max(1, sum(page_counts.values())))
        scored.append({"doc_id": page["doc_id"], "page": page["page"], "score": score})
    ranked_pages = sorted(scored, key=lambda row: (-row["score"], row["doc_id"], row["page"]))
    unique_docs = []
    seen = set()
    for row in ranked_pages:
        if row["doc_id"] not in seen:
            unique_docs.append(row)
            seen.add(row["doc_id"])
    return [
        {**row, "chunk_id": f"{row['doc_id']}:page{row['page']}", "rank": rank}
        for rank, row in enumerate(unique_docs[:limit], start=1)
    ]


def recall_at(results: list[dict], gold: set[str], k: int) -> float:
    results = dedupe_docs(results)[:k]
    found = {row["doc_id"] for row in results}
    return len(found & gold) / len(gold) if gold else 0.0


def precision_at(results: list[dict], gold: set[str], k: int) -> float:
    top = dedupe_docs(results)[:k]
    return sum(row["doc_id"] in gold for row in top) / k if k else 0.0


def ndcg_at(results: list[dict], gold: set[str], k: int) -> float:
    gains = [1.0 if row["doc_id"] in gold else 0.0 for row in dedupe_docs(results)[:k]]
    dcg = sum(gain / math.log2(rank + 2) for rank, gain in enumerate(gains))
    ideal_count = min(k, len(gold))
    idcg = sum(1.0 / math.log2(rank + 2) for rank in range(ideal_count))
    return dcg / idcg if idcg else 0.0


def dedupe_docs(results: list[dict]) -> list[dict]:
    unique = []
    seen = set()
    for row in results:
        if row["doc_id"] not in seen:
            unique.append(row)
            seen.add(row["doc_id"])
    return unique


def metric_values(results: list[dict], gold: set[str]) -> dict[str, float]:
    return {
        "recall_at_5": recall_at(results, gold, 5),
        "recall_at_50": recall_at(results, gold, 50),
        "precision_at_5": precision_at(results, gold, 5),
        "ndcg_at_5": ndcg_at(results, gold, 5),
    }


def mean_metrics(rows: list[dict]) -> dict[str, float | None]:
    return {
        key: (sum(row[key] for row in rows) / len(rows) if rows else None)
        for key in METRIC_KEYS
    }


def grouped_metrics(rows: list[dict], field: str) -> dict[str, dict]:
    groups = sorted({row[field] for row in rows})
    return {
        group: mean_metrics([row for row in rows if row[field] == group])
        for group in groups
    }


def mean_available(rows: list[dict], key: str) -> float | None:
    values = [row[key] for row in rows if row.get(key) is not None]
    return sum(values) / len(values) if values else None


def observed_metrics(rows: list[dict]) -> dict[str, float | int | None]:
    cutoffs = [row["logged_candidate_k"] for row in rows]
    return {
        "recall_at_logged_candidates": mean_available(rows, "recall_at_logged_candidates"),
        "recall_at_5": mean_available(rows, "recall_at_5"),
        "recall_at_50": mean_available(rows, "recall_at_50"),
        "precision_at_5": mean_available(rows, "precision_at_5"),
        "ndcg_at_5": mean_available(rows, "ndcg_at_5"),
        "logged_candidate_k_min": min(cutoffs),
        "logged_candidate_k_max": max(cutoffs),
    }


def grouped_observed_metrics(rows: list[dict], field: str) -> dict[str, dict]:
    groups = sorted({row[field] for row in rows})
    return {
        group: observed_metrics([row for row in rows if row[field] == group])
        for group in groups
    }


def evaluate(dataset: list[dict], pages: list[dict], top_k: int) -> dict:
    eligible = [item for item in dataset if item.get("answerable") and item.get("gold_doc_ids")]
    rows = []
    for item in eligible:
        results = search(item["question"], pages, limit=50)
        reported_results = results[:top_k]
        candidate_doc_ids = [row["doc_id"] for row in results]
        gold = set(item["gold_doc_ids"])
        rows.append({
            "qid": item["qid"], "tier": item["tier"], "split": item["split"], "type": item["type"],
            "gold_doc_ids": sorted(gold), "candidate_count": len(candidate_doc_ids),
            "candidate_doc_ids": candidate_doc_ids, "returned_count": len(reported_results),
            **metric_values(results, gold),
            "top_doc_ids": [row["doc_id"] for row in reported_results],
            "top_results": reported_results,
        })
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ-lexical-overlap")
    return {"run_id": run_id, "run_date": date.today().isoformat(), "settings": {"retriever": "word+bigrams-overlap", "candidate_k": 50, "report_k": top_k}, "metrics_policy": "unique-doc-macro-v1", "metrics": mean_metrics(rows), "slices": grouped_metrics(rows, "tier"), "split_slices": grouped_metrics(rows, "split"), "query_count": len(rows), "excluded_query_count": len(dataset) - len(eligible), "results": rows}


def load_retrieval_records(path: Path, dataset: list[dict]) -> list[dict]:
    labels = {item["qid"]: item for item in dataset}
    required = {"qid", "question", "gold_doc_ids", "retrieved", "source_chapter", "source_run_id", "config"}
    retrieved_required = {"doc_id", "chunk_id", "page", "rank", "score"}
    records = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        missing = required - row.keys()
        if missing:
            raise ValueError(f"{path}:{line_no} 필수 필드 누락: {sorted(missing)}")
        if row["qid"] not in labels:
            raise ValueError(f"{path}:{line_no} 평가셋에 없는 qid: {row['qid']}")
        label = labels[row["qid"]]
        if row["question"] != label["question"]:
            raise ValueError(f"{path}:{line_no} {row['qid']} 질문이 평가셋과 다릅니다.")
        if sorted(row["gold_doc_ids"]) != sorted(label["gold_doc_ids"]):
            raise ValueError(f"{path}:{line_no} {row['qid']} 정답 문서 ID가 평가셋과 다릅니다.")
        for expected_rank, item in enumerate(row["retrieved"], start=1):
            missing_item = retrieved_required - item.keys()
            if missing_item:
                raise ValueError(f"{path}:{line_no} 검색 항목 필드 누락: {sorted(missing_item)}")
            if item["rank"] != expected_rank:
                raise ValueError(f"{path}:{line_no} rank는 1부터 연속해야 합니다.")
        records.append({**row, "tier": label["tier"], "split": label["split"], "type": label["type"]})
    if not records:
        raise ValueError(f"{path}에 평가할 행이 없습니다.")
    return records


def evaluate_retrieval_records(records: list[dict], top_k: int) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in records:
        key = (row["source_chapter"], row["source_run_id"])
        grouped.setdefault(key, []).append(row)

    reports = []
    for (source_chapter, source_run_id), run_rows in sorted(grouped.items()):
        qids = [row["qid"] for row in run_rows]
        if len(qids) != len(set(qids)):
            raise ValueError(f"{source_chapter}/{source_run_id}에 중복 qid가 있습니다.")
        configs = {json.dumps(row["config"], ensure_ascii=False, sort_keys=True) for row in run_rows}
        if len(configs) != 1:
            raise ValueError(f"{source_chapter}/{source_run_id}의 config가 서로 다릅니다.")
        result_rows = []
        for row in run_rows:
            results = row["retrieved"]
            reported_results = results[:top_k]
            candidate_doc_ids = list(dict.fromkeys(result["doc_id"] for result in results))
            gold = set(row["gold_doc_ids"])
            logged_k = len(results)
            result_rows.append({
                "qid": row["qid"], "tier": row["tier"], "split": row["split"], "type": row["type"],
                "gold_doc_ids": sorted(gold), "candidate_count": len(candidate_doc_ids),
                "candidate_doc_ids": candidate_doc_ids, "returned_count": len(reported_results),
                "logged_candidate_k": logged_k,
                "recall_at_logged_candidates": recall_at(results, gold, logged_k),
                "recall_at_5": recall_at(results, gold, 5) if logged_k >= 5 else None,
                "recall_at_50": recall_at(results, gold, 50) if logged_k >= 50 else None,
                "precision_at_5": precision_at(results, gold, 5) if logged_k >= 5 else None,
                "ndcg_at_5": ndcg_at(results, gold, 5) if logged_k >= 5 else None,
                "top_results": reported_results,
            })
        reports.append({
            "run_id": source_run_id,
            "source_chapter": source_chapter,
            "settings": run_rows[0]["config"],
            "metrics_policy": "unique-doc-observed-candidates-v1",
            "evaluation_unit": "unique document ID per question",
            "query_ids": sorted(qids),
            "query_count": len(result_rows),
            "split_counts": dict(sorted(Counter(row["split"] for row in result_rows).items())),
            "metrics": observed_metrics(result_rows),
            "slices": grouped_observed_metrics(result_rows, "tier"),
            "split_slices": grouped_observed_metrics(result_rows, "split"),
            "results": result_rows,
        })
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--split", choices=("dev", "test", "all"), default="dev")
    parser.add_argument("--output", type=Path, default=Path("runs/baseline.json"))
    parser.add_argument("--retrieval-log", type=Path, action="append", default=[])
    args = parser.parse_args()
    root = find_repo_root(Path.cwd())
    dataset_path = root / "labs" / "part3" / "ch11-evaluation" / "data" / "evaluation-queries.jsonl"
    dataset = [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines() if line]
    selected_dataset = dataset if args.split == "all" else [item for item in dataset if item["split"] == args.split]
    if args.retrieval_log:
        source_files = [(root / path).resolve() if not path.is_absolute() else path for path in args.retrieval_log]
        records = [row for path in source_files for row in load_retrieval_records(path, dataset)]
        if args.split != "all":
            records = [row for row in records if row["split"] == args.split]
        if not records:
            raise ValueError(f"{args.split} 분할에 평가할 continuity 행이 없습니다.")
        report = {
            "report_type": "retrieval-continuity",
            "run_date": date.today().isoformat(),
            "metrics_policy": "unique-doc-observed-candidates-v1",
            "requested_split": args.split,
            "comparison_policy": "질문 목록·문서 집합·평가 단위가 같은 실행만 수치를 직접 비교합니다.",
            "source_files": [str(path.relative_to(root)) for path in source_files],
            "runs": evaluate_retrieval_records(records, args.top_k),
        }
    else:
        corpus = root / "labs" / "data" / "rag-corpus"
        report = evaluate(selected_dataset, load_pages(corpus), args.top_k)
        report["requested_split"] = args.split
        report["corpus_fingerprint"] = corpus_fingerprint(corpus)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.retrieval_log:
        summary = {"run_count": len(report["runs"]), "query_counts": [run["query_count"] for run in report["runs"]], "output": str(args.output)}
    else:
        summary = {"metrics": report["metrics"], "query_count": report["query_count"], "output": str(args.output)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
