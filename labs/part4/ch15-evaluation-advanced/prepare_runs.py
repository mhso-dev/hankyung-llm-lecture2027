"""Ch 12의 검색 결과에서 실제 답변과 judge 기록을 만든다."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "labs/part3/ch12-retrieval-tuning"


def load_environment() -> None:
    for directory in [ROOT, *ROOT.parents]:
        candidate = directory / ".env"
        if candidate.is_file():
            load_dotenv(candidate)
            break
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다. 키 값은 출력하지 않습니다.")


def main() -> None:
    load_environment()
    documents = json.loads((SOURCE / "data/advanced-documents.json").read_text())["parents"]
    queries = json.loads((SOURCE / "data/advanced-queries.json").read_text())
    by_doc = {row["doc_id"]: row for row in documents}
    by_qid = {row["qid"]: row for row in queries}
    selected = [("Q002", "E01"), ("Q006", "E01"), ("Q090", "H01")]
    reference_answers = {
        "Q002": "도서는 한 번에 7권까지 14일 동안 빌릴 수 있습니다.",
        "Q006": "회원은 최초 2시간 무료이며 이후 30분마다 500원입니다.",
        "Q090": "제공된 본문에는 입회인 정보가 없어 확인할 수 없습니다.",
    }
    model_name = "gpt-5.4-mini"
    model = init_chat_model(model_name, model_provider="openai", temperature=0)
    cases = []
    for qid, doc_id in selected:
        query = by_qid[qid]
        context = by_doc[doc_id]["text"]
        prompt = (
            "아래 근거만 사용해 질문에 한국어로 한 문단으로 답하세요. "
            "답 뒤에 [문서ID]를 표시하세요. 근거가 없으면 모른다고 답하세요.\n\n"
            f"질문: {query['question']}\n문서ID: {doc_id}\n근거:\n{context}"
        )
        answer_message = model.invoke(prompt)
        answer = answer_message.text
        cases.append({
            "qid": qid,
            "question": query["question"],
            "gold_doc_ids": query["gold_doc_ids"],
            "retrieved_doc_ids": [doc_id],
            "context": context,
            "response": answer,
            "reference_answer": reference_answers[qid],
            "reference_kind": "교육용 작성자 기준",
            "answer_model": model_name,
            "answer_prompt_version": "rag-answer-v1.0.0",
        })

    judge_model = "gpt-5.4-mini"
    judge = init_chat_model(judge_model, model_provider="openai", temperature=0)
    rubric = (
        "응답이 근거 문서로 뒷받침되면 1, 아니면 0을 판정하세요. "
        "JSON만 출력하세요: {\"score\": 0 또는 1, \"reason\": \"한 문장\"}."
    )
    for case in cases:
        judge_prompt = (
            f"{rubric}\n질문: {case['question']}\n근거: {case['context']}\n"
            f"응답: {case['response']}"
        )
        verdict = judge.invoke(judge_prompt).text
        case["judge_raw"] = verdict
        case["judge_model"] = judge_model
        case["judge_placeholder"] = "[[미정: judge 모델]]"
        case["judge_prompt_version"] = "groundedness-v1.0.0"

    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "created_at": now,
        "source_experiment_count": 36,
        "source_experiment_kind": "TF-IDF+MMR retrieval configuration",
        "source_generation_status": "The 36 rows contain no generated answers.",
        "cases": cases,
    }
    data_dir = HERE / "data"
    runs_dir = HERE / "runs"
    data_dir.mkdir(exist_ok=True)
    runs_dir.mkdir(exist_ok=True)
    (data_dir / "evaluation-cases.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"saved {len(cases)} generated answers and {len(cases)} judge results")


if __name__ == "__main__":
    main()
