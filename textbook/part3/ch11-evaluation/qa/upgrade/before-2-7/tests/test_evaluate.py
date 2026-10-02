import ast
import importlib.util
import json
from pathlib import Path


spec = importlib.util.spec_from_file_location("ch11_evaluate", Path(__file__).parents[1] / "evaluate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
evaluate = module.evaluate
evaluate_retrieval_records = module.evaluate_retrieval_records
load_retrieval_records = module.load_retrieval_records
ndcg_at = module.ndcg_at
precision_at = module.precision_at
recall_at = module.recall_at
search = module.search


def ranked(count=51):
    return [{"doc_id": f"D{i:02d}", "page": 1, "score": 1 / i} for i in range(1, count + 1)]


def test_cutoff_boundaries():
    results = ranked()
    assert recall_at(results, {"D06"}, 50) == 1.0
    assert precision_at(results, {"D06"}, 5) == 0.0
    assert ndcg_at(results, {"D06"}, 5) == 0.0
    assert recall_at(results, {"D51"}, 50) == 0.0


def test_duplicate_doc_ids_are_counted_once():
    results = [
        {"doc_id": "G", "page": 1},
        {"doc_id": "G", "page": 2},
        {"doc_id": "X", "page": 1},
    ]
    assert precision_at(results, {"G"}, 2) == 0.5
    assert ndcg_at(results, {"G"}, 2) == 1.0


def test_page_baseline_preserves_candidate_provenance():
    pages = [{"doc_id": "D", "page": 2, "text": "휴관일은 월요일입니다."}]
    result = search("휴관일", pages, 5)[0]
    assert result["chunk_id"] == "D:page2"
    assert result["rank"] == 1


def test_baseline_log_preserves_candidates_beyond_reported_top_results(monkeypatch):
    dataset = [{
        "qid": "Q", "tier": "easy", "split": "dev", "type": "multi_doc",
        "question": "검색어", "gold_doc_ids": ["G1", "G6"], "answerable": True,
    }]
    candidates = [
        {"doc_id": doc_id, "page": 1, "chunk_id": f"{doc_id}:page1", "rank": rank, "score": 1 / rank}
        for rank, doc_id in enumerate(["G1", "D2", "D3", "D4", "D5", "G6"], start=1)
    ]
    monkeypatch.setattr(module, "search", lambda _question, _pages, limit: candidates[:limit])
    report = evaluate(dataset, [], 5)
    row = report["results"][0]
    assert report["run_id"].endswith("Z-lexical-overlap")
    assert row["returned_count"] == 5
    assert row["candidate_count"] == 6
    assert "G6" not in row["top_doc_ids"]
    assert "G6" in row["candidate_doc_ids"]
    assert len(set(row["candidate_doc_ids"]) & set(row["gold_doc_ids"])) / len(row["gold_doc_ids"]) == 1.0


def test_empty_results_and_empty_gold_policy():
    assert recall_at([], {"G"}, 50) == 0.0
    assert precision_at([], {"G"}, 5) == 0.0
    assert ndcg_at([], {"G"}, 5) == 0.0
    dataset = [{"qid": "Q0", "tier": "easy", "split": "dev", "type": "single", "question": "없음", "gold_doc_ids": [], "answerable": False}]
    report = evaluate(dataset, [], 5)
    assert report["query_count"] == 0
    assert report["excluded_query_count"] == 1


def test_upstream_retrieval_log_uses_dataset_labels(tmp_path):
    dataset = [{
        "qid": "Q1", "tier": "easy", "split": "dev", "type": "single",
        "question": "질문", "gold_doc_ids": ["G", "H"], "answerable": True,
    }]
    row = {
        "qid": "Q1", "question": "질문", "gold_doc_ids": ["G", "H"],
        "source_chapter": "ch09", "source_run_id": "baseline", "config": {"k": 2},
        "retrieved": [
            {"doc_id": "G", "page": 1, "chunk_id": "G:1:0", "rank": 1, "score": 0.9},
            {"doc_id": "X", "page": 2, "chunk_id": "X:2:0", "rank": 2, "score": 0.8},
        ],
    }
    path = tmp_path / "log.jsonl"
    path.write_text(__import__("json").dumps(row, ensure_ascii=False), encoding="utf-8")
    records = load_retrieval_records(path, dataset)
    report = evaluate_retrieval_records(records, 2)[0]
    assert report["metrics"]["recall_at_logged_candidates"] == 0.5
    assert report["metrics"]["recall_at_5"] is None
    assert report["metrics"]["recall_at_50"] is None
    assert report["metrics"]["precision_at_5"] is None
    assert report["metrics"]["ndcg_at_5"] is None
    assert report["split_counts"] == {"dev": 1}
    assert report["results"][0]["top_results"][0]["chunk_id"] == "G:1:0"
    assert report["results"][0]["candidate_count"] == 2
    assert report["results"][0]["candidate_doc_ids"] == ["G", "X"]
    assert report["results"][0]["returned_count"] == 2


def test_upstream_retrieval_log_rejects_changed_question(tmp_path):
    dataset = [{
        "qid": "Q1", "tier": "easy", "split": "test", "type": "single",
        "question": "원래 질문", "gold_doc_ids": ["G"], "answerable": True,
    }]
    row = {
        "qid": "Q1", "question": "바꾼 질문", "gold_doc_ids": ["G"],
        "source_chapter": "ch10", "source_run_id": "run", "config": {}, "retrieved": [],
    }
    path = tmp_path / "bad.jsonl"
    path.write_text(__import__("json").dumps(row, ensure_ascii=False), encoding="utf-8")
    try:
        load_retrieval_records(path, dataset)
    except ValueError as error:
        assert "질문이 평가셋과 다릅니다" in str(error)
    else:
        raise AssertionError("질문 변경을 거부해야 합니다.")


def test_notebook_05_multi_gold_recall_is_fractional():
    notebook_path = Path(__file__).parents[1] / "notebooks/05-조건별-평가와-오류-분류.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    source = next(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code" and "def metrics(item):" in "".join(cell["source"])
    )
    function = next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef))
    namespace = {"search": lambda _question, _k: [{"doc_id": "G"}]}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(notebook_path), "exec"), namespace)
    recall, _precision = namespace["metrics"]({"question": "q", "gold_doc_ids": ["G", "H"]})
    assert recall == 0.5
