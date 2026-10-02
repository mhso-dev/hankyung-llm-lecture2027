import json
from pathlib import Path


ROOT = Path(__file__).parent
NOTEBOOKS = ROOT / "notebooks"

COMMON = [
    ("markdown", "## 실행 환경 준비\n\n이 노트북은 제공 PDF에서 실제 텍스트를 추출합니다. 답변 생성 API는 호출하지 않습니다."),
    ("code", '''from pathlib import Path
import json, math, re
from collections import Counter
from pypdf import PdfReader

# 현재 폴더에서 저장소의 공개 RAG 자료를 찾습니다.
root = next(p for p in (Path.cwd(), *Path.cwd().parents)
            if (p / "labs/data/rag-corpus/manifest.json").exists())
corpus = root / "labs/data/rag-corpus"
dataset_path = root / "labs/part3/ch11-evaluation/data/evaluation-queries.jsonl"
dataset = [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines()]
evaluation_items = [item for item in dataset if item["split"] == "dev"]
print(f"전체 질문: {len(dataset)}개")
print(f"설정 선택용 dev 질문: {len(evaluation_items)}개")'''),
    ("markdown", "## 공개 PDF를 페이지 단위 후보로 준비\n\n스캔본은 OCR이 필요하므로 이번 기초 검색에서 제외합니다."),
    ("code", '''manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
pages = []
for item in manifest:
    if item["tier"] == "scanned":
        continue
    reader = PdfReader(corpus / item["file"])
    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"doc_id": item["doc_id"], "page": page_no, "text": text})
print(f"검색 후보: {len(pages)}개 페이지")'''),
    ("markdown", "## 같은 검색기를 모든 질문에 적용\n\n단어와 한글 두 글자 조각의 겹침을 사용합니다. 점수가 같으면 문서 ID와 쪽 번호로 순서를 고정합니다."),
    ("code", '''def tokens(text):
    normalized = re.sub(r"\\s+", " ", text.lower())
    words = re.findall(r"[가-힣a-z0-9]+", normalized)
    compact = re.sub(r"[^가-힣a-z0-9]", "", normalized)
    return words + [compact[i:i+2] for i in range(max(0, len(compact)-1))]

def search(question, limit=50):
    query_counts = Counter(tokens(question))
    scored = []
    for page in pages:
        page_counts = Counter(tokens(page["text"]))
        overlap = sum(min(count, page_counts[token]) for token, count in query_counts.items())
        score = overlap / math.sqrt(max(1, sum(page_counts.values())))
        scored.append({"doc_id": page["doc_id"], "page": page["page"], "score": score})
    ranked_pages = sorted(scored, key=lambda row: (-row["score"], row["doc_id"], row["page"]))
    unique_docs, seen = [], set()
    for row in ranked_pages:
        if row["doc_id"] not in seen:
            unique_docs.append(row)
            seen.add(row["doc_id"])
    return unique_docs[:limit]

sample = search(dataset[0]["question"], 5)
print([(row["doc_id"], row["page"], round(row["score"], 3)) for row in sample])'''),
]

TAILS = {
"01-질의셋과-정답-문서-ID": [
 ("markdown", "## 라벨 구조 확인\n\n질문과 정답 문서 ID만 공개합니다. 정답 문장은 검색 평가에 필요하지 않습니다."),
 ("code", '''required = {"qid", "tier", "question", "type", "gold_doc_ids", "answerable", "split"}
assert all(required == set(item) for item in dataset)
assert all("answer" not in item for item in dataset)
for item in dataset[:3]:
    print(item["qid"], item["tier"], item["split"], item["gold_doc_ids"], item["question"])'''),
 ("markdown", "## 값 하나를 바꿔 비교\n\n설정 선택용 dev 질문 수를 5개와 15개로 바꾸고 문서 분포가 어떻게 달라지는지 확인합니다."),
 ("code", '''for size in (5, 15):
    subset = evaluation_items[:size]
    counts = Counter(doc_id for item in subset for doc_id in item["gold_doc_ids"])
    print(size, "문항:", dict(sorted(counts.items())))'''),
],
"02-Recall-at-50": [
 ("markdown", "## Recall@50 계산\n\n정답 문서 중 후보 50개 안에 든 문서의 비율을 이 문항의 재현율로 계산합니다."),
 ("code", '''def recall_at(results, gold, k):
    found = {row["doc_id"] for row in results[:k]}
    return len(found & set(gold)) / len(gold) if gold else 0.0

rows = []
for item in evaluation_items:
    results = search(item["question"], 50)
    rows.append((item["qid"], recall_at(results, item["gold_doc_ids"], 50)))
print("Recall@50:", round(sum(score for _, score in rows) / len(rows), 3))
print("놓친 질문:", [qid for qid, score in rows if score < 1])'''),
 ("markdown", "## k 값 비교\n\nk만 바꾸고 질문·라벨·검색 점수를 고정합니다."),
 ("code", '''for k in (1, 5, 10, 50):
    scores = [recall_at(search(item["question"], 50), item["gold_doc_ids"], k)
              for item in evaluation_items]
    print(f"Recall@{k}: {sum(scores) / len(scores):.3f}")'''),
 ("markdown", "## 51위 누락을 작은 목록으로 확인\n\n현재 말뭉치는 검색 가능한 고유 문서가 17개라 Recall@50이 포화됩니다. 51개 목록으로 경계를 따로 검증합니다."),
 ("code", '''toy = [{"doc_id": f"D{i:02d}"} for i in range(1, 52)]
assert recall_at(toy, ["D50"], 50) == 1.0
assert recall_at(toy, ["D51"], 50) == 0.0
print("정답 50위:", recall_at(toy, ["D50"], 50))
print("정답 51위:", recall_at(toy, ["D51"], 50))'''),
],
"03-Precision-at-5": [
 ("markdown", "## Precision@5 계산\n\n중복 문서 ID를 제거한 상위 5개 문서 가운데 정답 문서가 차지하는 비율을 구합니다."),
 ("code", '''def precision_at(results, gold, k):
    return sum(row["doc_id"] in set(gold) for row in results[:k]) / k

rows = []
for item in evaluation_items:
    results = search(item["question"], 50)
    rows.append((item["qid"], precision_at(results, item["gold_doc_ids"], 5)))
mean_p5 = sum(score for _, score in rows) / len(rows)
print("Precision@5:", round(mean_p5, 3))
print("낮은 5개:", sorted(rows, key=lambda row: row[1])[:5])'''),
 ("markdown", "## k 값 비교\n\nk가 커질수록 관련 없는 페이지가 포함될 여지가 늘어납니다."),
 ("code", '''for k in (1, 3, 5, 10):
    scores = [precision_at(search(item["question"], 50), item["gold_doc_ids"], k)
              for item in evaluation_items]
    print(f"Precision@{k}: {sum(scores) / len(scores):.3f}")'''),
],
"04-nDCG-at-5": [
 ("markdown", "## 예제 순위를 손으로 계산\n\n관련도 1과 0만 사용하는 이진 라벨로 DCG와 이상적인 DCG를 비교합니다."),
 ("code", '''def ndcg_from_gains(gains):
    dcg = sum(gain / math.log2(rank + 2) for rank, gain in enumerate(gains))
    ideal = sorted(gains, reverse=True)
    idcg = sum(gain / math.log2(rank + 2) for rank, gain in enumerate(ideal))
    return dcg / idcg if idcg else 0.0

example = [0, 1, 0, 1, 0]
manual = (1 / math.log2(3) + 1 / math.log2(5)) / (1 + 1 / math.log2(3))
print("함수:", round(ndcg_from_gains(example), 6))
print("수계산:", round(manual, 6))
assert math.isclose(ndcg_from_gains(example), manual)'''),
 ("markdown", "## 개발용 15문항 nDCG@5\n\n설정 선택에는 dev 분할만 사용합니다. 정답 문서가 앞에 있을수록 점수가 높습니다."),
 ("code", '''def ndcg_at(results, gold, k):
    gains = [1 if row["doc_id"] in set(gold) else 0 for row in results[:k]]
    dcg = sum(gain / math.log2(rank + 2) for rank, gain in enumerate(gains))
    idcg = sum(1 / math.log2(rank + 2) for rank in range(min(k, len(set(gold)))))
    return dcg / idcg if idcg else 0.0

scores = [ndcg_at(search(item["question"], 50), item["gold_doc_ids"], 5)
          for item in evaluation_items]
print("nDCG@5:", round(sum(scores) / len(scores), 3))
print("최솟값/최댓값:", round(min(scores), 3), round(max(scores), 3))'''),
],
"05-조건별-평가와-오류-분류": [
 ("markdown", "## 질문 유형별로 나누어 측정\n\n전체 평균과 유형별 평균을 함께 봅니다."),
 ("code", '''eligible = [item for item in evaluation_items if item["answerable"] and item["gold_doc_ids"]]
excluded_count = len(evaluation_items) - len(eligible)

def metrics(item):
    results = search(item["question"], 50)
    gold = set(item["gold_doc_ids"])
    r50 = len({row["doc_id"] for row in results} & gold) / len(gold) if gold else 0.0
    p5 = sum(row["doc_id"] in gold for row in results[:5]) / 5
    return r50, p5

grouped = {}
for item in eligible:
    grouped.setdefault(item["type"], []).append(metrics(item))
for name, values in sorted(grouped.items()):
    print(name, len(values), f"R@50={sum(v[0] for v in values)/len(values):.3f}",
          f"P@5={sum(v[1] for v in values)/len(values):.3f}")
print("검색 평균 제외:", excluded_count)'''),
 ("markdown", "## 오류를 검색 단계 이름으로 분류\n\n후보 누락과 상위 순위 문제를 서로 다른 이름으로 기록합니다."),
 ("code", '''labels = Counter()
for item in eligible:
    results = search(item["question"], 50)
    gold = set(item["gold_doc_ids"])
    top50 = {row["doc_id"] for row in results}
    top5 = {row["doc_id"] for row in results[:5]}
    if not top50 & gold:
        labels["candidate_miss"] += 1
    elif not top5 & gold:
        labels["ranking_miss"] += 1
    else:
        labels["top5_hit"] += 1
print(dict(labels))'''),
],
"06-실험-로그와-자동-실행": [
 ("markdown", "## Ch 9·10의 실제 검색 로그 찾기\n\n두 챕터가 Q001을 실행해 남긴 새 continuity 로그를 읽습니다. 원래 로그는 수정하지 않습니다."),
 ("code", '''source_logs = [
    root / "labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl",
    root / "labs/part3/ch10-document-processing/runs/continuity-ch10-indexing.jsonl",
]
for path in source_logs:
    assert path.exists(), f"앞 챕터 continuity 로그가 없습니다: {path}"
    print(path.relative_to(root), "행:", len(path.read_text(encoding="utf-8").splitlines()))'''),
 ("markdown", "## 검색 결과만 지표로 계산하기\n\n<code>evaluate.py</code>는 질문과 정답 문서 ID가 Ch 11 질의셋과 같은지 검사합니다. Ch 9의 생성 답변은 Ch 15 평가 대상이므로 이 실행에서 점수를 계산하지 않습니다."),
 ("code", '''import subprocess, sys
from datetime import datetime, timezone

ch11 = root / "labs/part3/ch11-evaluation"
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
output = ch11 / "runs" / f"continuity-upstream-{stamp}.json"
command = [sys.executable, str(ch11 / "evaluate.py"), "--split", "dev"]
for path in source_logs:
    command.extend(["--retrieval-log", str(path)])
command.extend(["--output", str(output)])
completed = subprocess.run(command, cwd=root, check=True, text=True, capture_output=True)
print(completed.stdout.strip())'''),
 ("markdown", "## 실행별 범위와 지표 확인\n\nQ001 하나로 계산한 결과는 연결 형식을 확인합니다. 30개 질문 기준선과 수치를 직접 비교하지 않습니다."),
 ("code", '''report = json.loads(output.read_text(encoding="utf-8"))
for run in report["runs"]:
    print(run["source_chapter"], run["run_id"], run["query_count"], run["metrics"])
    assert run["query_ids"] == ["Q001"]
print("평가 단위:", report["runs"][0]["evaluation_unit"])
print("새 결과:", output.relative_to(root))'''),
],
}


TITLES = {
    "01-질의셋과-정답-문서-ID": "질의셋과 정답 문서 ID",
    "02-Recall-at-50": "Recall@50",
    "03-Precision-at-5": "Precision@5",
    "04-nDCG-at-5": "nDCG@5",
    "05-조건별-평가와-오류-분류": "조건별 평가와 오류 분류",
    "06-실험-로그와-자동-실행": "실험 로그와 자동 실행",
}


def cell(kind, source, number):
    base = {"cell_type": kind, "id": f"cell-{number:02d}", "metadata": {}}
    base["source"] = source.splitlines(keepends=True)
    if kind == "code":
        base.update({"execution_count": None, "outputs": []})
    return base


for slug, title in TITLES.items():
    parts = [("markdown", f"# {title}\n\n전체 30개 질문을 읽고 dev 15개로 설정을 검토합니다."), *COMMON, *TAILS[slug]]
    cells = [cell(kind, source, index) for index, (kind, source) in enumerate(parts, start=1)]
    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": "experiment"},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (NOTEBOOKS / f"{slug}.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
