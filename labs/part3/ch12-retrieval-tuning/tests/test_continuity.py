import ast
import json
import math
import re
from pathlib import Path

import numpy as np
import pytest


ROOT = next(
    path
    for path in (Path(__file__).resolve(), *Path(__file__).resolve().parents)
    if (path / "labs/part3/ch12-retrieval-tuning").exists()
)
CH12 = ROOT / "labs/part3/ch12-retrieval-tuning"


def code_cell_trees(notebook_name):
    notebook = json.loads((CH12 / "notebooks" / notebook_name).read_text())
    trees = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        try:
            trees.append(ast.parse("".join(cell["source"])))
        except SyntaxError:
            continue  # %pip 같은 노트북 매직이 든 셀은 파이썬 문법이 아니라 건너뛴다
    return trees


def tool_namespace():
    """노트북이 `from rag_tools import …`로 가져오는 도구 파일 함수를 이름 공간에 먼저 넣는다(§2-7)."""
    scope = {}
    source = (CH12 / "notebooks" / "rag_tools.py").read_text()
    exec(compile(source, "rag_tools.py", "exec"), scope)
    return scope


def load_notebook_function(notebook_name, function_name, namespace=None):
    for tree in code_cell_trees(notebook_name):
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                module = ast.Module(body=[node], type_ignores=[])
                scope = {"np": np, **tool_namespace(), **(namespace or {})}
                exec(compile(ast.fix_missing_locations(module), notebook_name, "exec"), scope)
                return scope[function_name]
    raise AssertionError(f"{notebook_name}에서 {function_name}을 찾지 못했습니다")


def load_notebook_namespace(notebook_name, namespace=None):
    """도구 파일 함수와 노트북의 함수 정의를 한 이름 공간에 모아 서로 부를 수 있게 한다.

    노트북에 같은 이름의 정의가 있으면(그 절이 처음 가르친 판) 노트북 판이 도구 파일 판을 덮는다.
    """
    scope = {"np": np, **tool_namespace(), **(namespace or {})}
    for tree in code_cell_trees(notebook_name):
        defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if not defs:
            continue
        module = ast.Module(body=defs, type_ignores=[])
        exec(compile(ast.fix_missing_locations(module), notebook_name, "exec"), scope)
    return scope


def test_ch11_query_source_matches_ch12_distribution_copy():
    source = [
        json.loads(line)
        for line in (ROOT / "labs/part3/ch11-evaluation/data/evaluation-queries.jsonl")
        .read_text()
        .splitlines()
        if line
    ]
    distributed = json.loads((CH12 / "data/advanced-queries.json").read_text())
    assert source == distributed
    assert {row["split"] for row in source} == {"dev", "test"}
    assert sum(row["split"] == "dev" for row in source) == 15
    assert sum(row["split"] == "test" for row in source) == 15


def test_document_and_chunk_identifiers_preserve_source_position():
    data = json.loads((CH12 / "data/advanced-documents.json").read_text())
    parent_ids = {row["doc_id"] for row in data["parents"]}
    query_ids = {
        doc_id
        for row in json.loads((CH12 / "data/advanced-queries.json").read_text())
        for doc_id in row["gold_doc_ids"]
    }
    assert query_ids <= parent_ids
    for chunk in data["chunks"]:
        match = re.fullmatch(r"(.+)-P(\d{2})-C(\d{2})", chunk["chunk_id"])
        assert match
        assert match.group(1) == chunk["parent_id"]
        assert int(match.group(2)) == chunk["page"]
        assert chunk["parent_id"] in parent_ids


def test_continuity_logs_keep_query_level_evidence_and_scope():
    rows = [
        json.loads(line)
        for line in (CH12 / "runs/advanced-continuity-experiment-log.jsonl")
        .read_text()
        .splitlines()
        if line
    ]
    assert len(rows) == 36
    assert all(row["split"] == "dev" and row["query_count"] == 15 for row in rows)
    assert all(len(row["results"]) == 15 and row["slices"] for row in rows)
    assert all(row["source_chapter"] == "ch12" and row["query_source_chapter"] == "ch11" for row in rows)
    assert all(row["settings"]["candidate_unit"] == "chunk" for row in rows)
    assert all(row["metrics_policy"] == "chunk-candidate-unique-parent-macro-v1" for row in rows)
    assert all(row["comparison_policy"] == "compare-only-pairs-that-differ-by-one-setting" for row in rows)
    assert all(
        result["returned_count"] == len(result["top_results"])
        and all({"doc_id", "page", "chunk_id", "rank"} <= item.keys() for item in result["top_results"])
        for row in rows
        for result in row["results"]
    )
    assert all(row["corpus_fingerprint"] and row["query_fingerprint"] for row in rows)

    test = json.loads((CH12 / "runs/advanced-continuity-test-result.json").read_text())
    assert test["split"] == "test" and test["query_count"] == 15
    assert test["comparison_policy"] == "selected-on-dev-then-evaluate-test-once"
    assert len(test["results"]) == 15 and test["run_date"]

    smoke = json.loads((CH12 / "runs/advanced-continuity-integrated-result.json").read_text())
    assert smoke["run_type"] == "generation_smoke_test"
    assert smoke["split"] == "dev"
    assert smoke["retrieval_metrics"] is None
    assert smoke["generation_evaluation"]["status"] == "not_evaluated"
    assert smoke["settings"]["dimensions"] == 256
    assert smoke["settings"]["chat"] == "gpt-5.4-mini"
    assert all(item["chunk_id"].startswith(f"{item['doc_id']}-P{item['page']:02d}-") for item in smoke["retrieved"])

    session_dir = CH12 / "runs/continuity" / rows[0]["run_id"].removeprefix("advanced-continuity-").rsplit("-dev-", 1)[0]
    assert (session_dir / "advanced-continuity-experiment-log.jsonl").read_text() == (CH12 / "runs/advanced-continuity-experiment-log.jsonl").read_text()
    assert (session_dir / "advanced-continuity-test-result.json").read_text() == (CH12 / "runs/advanced-continuity-test-result.json").read_text()
    assert (session_dir / "advanced-continuity-integrated-result.json").read_text() == (CH12 / "runs/advanced-continuity-integrated-result.json").read_text()


def test_student_metric_functions_handle_multi_gold_duplicates_and_empty_gold():
    mixed = [
        {"qid": "Q-MULTI", "question": "도서관 휴관일", "tier": "basic", "split": "dev",
         "answerable": True, "gold_doc_ids": ["D1", "D2", "D2"]},
        {"qid": "Q-EMPTY", "question": "빈 정답", "tier": "basic", "split": "dev",
         "answerable": True, "gold_doc_ids": []},
        {"qid": "Q-NA", "question": "답변 불가", "tier": "basic", "split": "dev",
         "answerable": False, "gold_doc_ids": ["D3"]},
    ]
    space_08 = load_notebook_namespace(
        "08-후보-수와-리랭커-비교.ipynb",
        {
            "parent_by_chunk": {"D1-P01-C01": "D1", "D1-P01-C02": "D1"},
            "candidate_sets": {"Q-MULTI": ["D1-P01-C01", "D1-P01-C02"]},
            "recall_place": 3,
            "report_place": 5,
        },
    )
    eligible_08 = space_08["eligible_items"]
    space_08["dev_queries"] = eligible_08(mixed)
    assert [item["qid"] for item in space_08["dev_queries"]] == ["Q-MULTI"]
    assert space_08["dev_queries"][0]["gold_doc_ids"] == ["D1", "D2"]
    recall, _ = space_08["evaluate"]({"Q-MULTI": [2.0, 1.0]}, candidate_k=2)
    assert recall == 0.5

    space_08["dev_queries"] = []
    with pytest.raises(ValueError, match="평가 가능한 개발 문항"):
        space_08["evaluate"]({}, candidate_k=2)

    # 12절 노트북도 사다리에 맞춰 함수를 잘게 나눠 서로 부르므로 이름 공간으로 불러온다
    space_12 = load_notebook_namespace(
        "12-종합-튜닝과-실험-로그.ipynb",
        {
            "math": math,
            "similarity_top": 1,
            "rank_constant": 60,
            "candidate_count": 8,
            "recall_place": 3,
            "report_place": 5,
            "metric_names": ["recall_at_3", "recall_at_5", "recall_at_50",
                             "precision_at_5", "ndcg_at_5", "chunk_precision_at_5"],
            "parent_by_chunk": {"D1-P01-C01": "D1", "D2-P01-C01": "D2"},
            "page_by_chunk": {"D1-P01-C01": 1, "D2-P01-C01": 1},
            "vector_by_chunk": {"D1-P01-C01": [1.0, 0.0], "D2-P01-C01": [0.0, 1.0]},
        },
    )
    eligible_12 = space_12["eligible_items"]
    assert [item["qid"] for item in eligible_12(mixed)] == ["Q-MULTI"]
    # metrics는 값 여섯 개를 내고 두 번째·세 번째가 자리 5·후보 안 재현율이다
    scores_12 = space_12["metrics"](["D1"], ["D1"], ["D1", "D2"], ["D1-P01-C01"])
    assert (scores_12[1], scores_12[2]) == (0.5, 0.5)

    # 10절 노트북의 mmr은 파이썬 목록을 받아 고른 자리 번호 목록을 돌려준다(닮은 정도는 도구 파일 cosine_similarity)
    space_10 = load_notebook_namespace("10-MMR-다양성-선택.ipynb", {"similarity_top": 1, "math": math})
    selected = space_10["mmr"](
        [1.0, 0.0], [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], pick_count=3, relevance_weight=0.5
    )
    assert len(selected) == len(set(selected)) == 3

    # 12절이 도구 파일에서 가져오는 mmr도 10절과 같이 파이썬 목록을 받고 고른 자리 번호 목록을 돌려준다
    selected_12 = space_12["mmr"](
        [1.0, 0.0], [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], pick_count=3, relevance_weight=0.5
    )
    assert len(selected_12) == len(set(selected_12)) == 3

    # evaluate_config는 질문 ID로 미리 만들어 둔 순위 목록·질문 벡터를 읽는다
    space_12["lists_by_qid"] = {"Q-MULTI": [["D1-P01-C01", "D2-P01-C01"],
                                            ["D2-P01-C01", "D1-P01-C01"]]}
    space_12["vector_by_qid"] = {"Q-MULTI": [1.0, 0.0]}
    config = {"weights": [1.0, 1.0], "relevance_weight": 0.8, "rank_constant": 60,
              "candidate_k": 8, "candidate_unit": "chunk",
              "report_k": 2, "report_unit": "unique-parent-document"}
    summary, slices, results = space_12["evaluate_config"](config, mixed)
    assert [result["qid"] for result in results] == ["Q-MULTI"]
    assert set(summary) == set(space_12["metric_names"]) and set(slices) == {"basic"}
    assert [hit["rank"] for hit in results[0]["top_results"]] == [1, 2]
    with pytest.raises(ValueError, match="평가 가능한 문항"):
        space_12["evaluate_config"](config, mixed[1:])
