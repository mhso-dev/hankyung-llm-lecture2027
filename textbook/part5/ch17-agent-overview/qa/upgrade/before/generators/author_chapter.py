"""Ch 17 정본 노트북·데이터·교재 원본을 생성합니다."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB = ROOT / "labs/part5/ch17-agent-overview"
BOOK = ROOT / "textbook/part5/ch17-agent-overview"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": text.splitlines(True)}


def code(text: str) -> dict:
    text = "# 이 셀의 계산과 출력에서 현재 단계의 결과를 확인합니다.\n" + text
    return {
        "cell_type": "code", "execution_count": None, "id": "", "metadata": {},
        "outputs": [], "source": text.splitlines(True),
    }


SETUP_BODY = '''
start = Path.cwd().resolve()
candidates = (start, *start.parents)
ROOT = next(path for path in candidates if (path / "labs/part5/ch17-agent-overview").is_dir())
LAB = ROOT / "labs/part5/ch17-agent-overview"
print("Python:", sys.version.split()[0], "| 실습 폴더:", LAB.relative_to(ROOT))'''

SETUP = '''from pathlib import Path
import sys
''' + SETUP_BODY

SETUP_BOUNDARY = '''from collections import Counter
from collections.abc import Mapping
from pathlib import Path
import sys
from typing import TypedDict
''' + SETUP_BODY

SETUP_TRACE = '''from pathlib import Path
import sys
from typing import TypedDict
''' + SETUP_BODY

SETUP_COST = '''from pathlib import Path
import sys
from typing import TypedDict
''' + SETUP_BODY + '''
# 비용·지연 사건의 필드 타입을 고정해 합산 대상을 분명히 합니다.
class CostEvent(TypedDict):
    event: str
    ms: int
    cost: int'''

SETUP_EVIDENCE = '''import csv
import json
from pathlib import Path
import sys
''' + SETUP_BODY


NOTEBOOKS = {
"01-워크플로우와-에이전트-경계": [
    md("# 워크플로우와 에이전트 경계\n\n누가 다음 단계를 정하는지 사건별로 표시해 두 구조의 경계를 확인합니다."),
    md("## 실행 환경 준비\n\n외부 API를 호출하지 않습니다. 교육용 고정 사례를 읽고 분류하므로 실행할 때마다 같은 결과가 나옵니다."),
    code(SETUP_BOUNDARY),
    md("## 사례 준비\n\n`decision_owner`는 다음 행동을 정한 주체입니다. `code`면 미리 작성한 경로, `model`이면 입력과 관찰 결과를 본 모델의 선택입니다."),
    code('''class Case(TypedDict):
    name: str
    steps: int | None
    decision_owner: str
    unknown_steps: bool

cases: list[Case] = [
    {"name": "정해진 환불 절차", "steps": 4, "decision_owner": "code", "unknown_steps": False},
    {"name": "여러 파일의 결함 수정", "steps": None, "decision_owner": "model", "unknown_steps": True},
    {"name": "문서 요약 뒤 형식 검사", "steps": 3, "decision_owner": "code", "unknown_steps": False},
    {"name": "낯선 장애 원인 조사", "steps": None, "decision_owner": "model", "unknown_steps": True},
]
print(*cases, sep="\\n")'''),
    md("## 경계 분류\n\n도구 사용 여부보다 다음 단계의 결정 주체를 먼저 봅니다."),
    code('''def architecture(case: Mapping[str, object]) -> str:
    if case["decision_owner"] == "model" and case["unknown_steps"] is True:
        return "에이전트 후보"
    return "워크플로우"

for case in cases:
    print(case["name"], "→", architecture(case))'''),
    md("## 값 하나를 바꿔 비교\n\n같은 환불 절차에서 도구를 세 개로 늘려도 분기를 코드가 정하면 분류는 바뀌지 않습니다."),
    code('''refund = cases[0] | {"tool_count": 3}
print("도구 수:", refund["tool_count"])
print("결정 주체:", refund["decision_owner"])
print("분류:", architecture(refund))
assert architecture(refund) == "워크플로우"'''),
    md("## 전체 사례 집계\n\n분류 결과는 교육용 사례의 필드에서 계산한 값입니다. 실제 제품의 내부 구조를 측정한 결과가 아닙니다."),
    code('''counts = Counter(architecture(case) for case in cases)
print(dict(counts))
print("판정 기준: 다음 단계 결정 주체 + 필요한 단계의 사전 예측 가능성")
assert counts == {"워크플로우": 2, "에이전트 후보": 2}'''),
],
"02-워크플로우가-충분한-조건": [
    md("# 워크플로우가 충분한 조건\n\n다섯 가지 질문으로 중간 프로젝트에 필요한 자율성 수준을 판단합니다."),
    md("## 실행 환경 준비\n\n점수와 비용은 설계를 비교하기 위한 교육용 고정값입니다. 모델 호출, 실제 청구, 품질 측정을 수행하지 않습니다."),
    code(SETUP_TRACE),
    md("## 진단 기준\n\n경로를 미리 적을 수 있고 실패 처리와 승인 지점이 명확할수록 워크플로우가 적합합니다."),
    code('''criteria = [
    ("단계를 미리 나열할 수 있는가", 2),
    ("입력 유형을 안정적으로 구분할 수 있는가", 1),
    ("실패 때 실행할 대체 경로가 정해져 있는가", 1),
    ("외부 쓰기 전에 승인 지점을 둘 수 있는가", 1),
    ("같은 입력에 같은 절차가 중요한가", 1),
]
print("워크플로우 적합 최대점:", sum(weight for _, weight in criteria))'''),
    md("## 두 프로젝트 비교\n\n값은 가상 수업 사례에 대해 미리 정한 진단 응답입니다."),
    code('''projects = {
    "사내 규정 질의응답": [True, True, True, True, True],
    "낯선 저장소 장애 수정": [False, False, False, True, False],
}

def workflow_score(answers: list[bool]) -> int:
    return sum(weight for (_, weight), answer in zip(criteria, answers) if answer)

for name, answers in projects.items():
    score = workflow_score(answers)
    recommendation = "워크플로우 우선" if score >= 4 else "제한된 에이전트 검토"
    print(name, score, "/ 6", recommendation)
assert workflow_score(projects["사내 규정 질의응답"]) == 6
assert workflow_score(projects["낯선 저장소 장애 수정"]) == 1'''),
    md("## 불필요한 자율성의 교육용 비용\n\n규정 질의응답에 모델 결정 단계를 두 개 추가했다고 가정합니다. 호출 수와 시간은 실제 측정값이 아닙니다."),
    code('''fixed_scenario = {"calls": 2, "latency_s": 2.4, "cost_units": 2}
agentic_scenario = {"calls": 4, "latency_s": 5.9, "cost_units": 5}
for key in fixed_scenario:
    delta = agentic_scenario[key] - fixed_scenario[key]
    shown = f"{delta:.1f}" if isinstance(delta, float) else delta
    print(key, "교육용 차이:", shown)
print("품질 향상은 이 데이터로 측정하지 않았습니다.")'''),
    md("## 민감도 확인\n\n임계값을 바꿨을 때 추천이 얼마나 쉽게 달라지는지 확인합니다."),
    code('''for threshold in (3, 4, 5):
    labels = {name: workflow_score(value) >= threshold for name, value in projects.items()}
    print("임계값", threshold, labels)
print("경계 점수는 팀 검토가 필요하며 자동 결정 규칙으로 사용하지 않습니다.")
assert agentic_scenario["calls"] - fixed_scenario["calls"] == 2
assert agentic_scenario["cost_units"] - fixed_scenario["cost_units"] == 3'''),
],
"03-모델-도구-루프와-정지-조건": [
    md("# 모델·도구·루프와 정지 조건\n\n완성된 에이전트를 만들지 않고 사건 목록으로 루프와 중단 이유를 읽습니다."),
    md("## 실행 환경 준비\n\n아래 코드는 모델이나 도구를 호출하지 않는 상태 전이 시뮬레이터입니다. Ch 20의 ToolNode 그래프 루프를 미리 구현하지 않습니다."),
    code(SETUP),
    md("## 세 요소와 관찰\n\n모델은 다음 행동을 제안하고, 도구는 환경에서 결과를 가져오며, 루프는 결과를 다음 판단에 다시 넣습니다."),
    code('''class TraceEvent(TypedDict):
    step: int
    actor: str
    event: str
    progress: float
    cost: int

trace: list[TraceEvent] = [
    {"step": 1, "actor": "model", "event": "search", "progress": 0.20, "cost": 1},
    {"step": 2, "actor": "tool", "event": "search_result", "progress": 0.45, "cost": 0},
    {"step": 3, "actor": "model", "event": "read", "progress": 0.65, "cost": 1},
    {"step": 4, "actor": "tool", "event": "read_result", "progress": 0.90, "cost": 0},
    {"step": 5, "actor": "model", "event": "finish", "progress": 1.00, "cost": 1},
]
for event in trace:
    print(event)'''),
    md("## 정지 판정\n\n완료, 최대 단계, 예산, 사람 확인 요청을 서로 다른 종료 이유로 보존합니다."),
    code('''def stop_reason(
    events: list[TraceEvent], max_steps: int = 6, max_cost: int = 4
) -> str | None:
    if not events:
        return None
    if events[-1]["event"] == "finish":
        return "완료"
    if any(item["event"] == "human_check" for item in events):
        return "사람 확인"
    if len(events) >= max_steps:
        return "최대 단계"
    if sum(item["cost"] for item in events) >= max_cost:
        return "예산"
    return None

print("기본 추적 정지:", stop_reason(trace))'''),
    md("## 완료 사건을 제거한 비교\n\n마지막 완료를 제거하면 아직 실행 중인 상태로 판정됩니다."),
    code('''unfinished: list[TraceEvent] = trace[:-1]
print("사건 수:", len(unfinished))
print("정지 이유:", stop_reason(unfinished))
assert stop_reason(unfinished) is None'''),
    md("## 세 가지 중단 사례\n\n각 사례는 정지 조건의 우선순위를 확인하기 위한 교육용 사건입니다."),
    code('''maxed: list[TraceEvent] = unfinished + [{"step": 5, "actor": "model", "event": "retry", "progress": .9, "cost": 1},
                      {"step": 6, "actor": "tool", "event": "same_result", "progress": .9, "cost": 0}]
budgeted: list[TraceEvent] = trace[:4] + [{"step": 5, "actor": "model", "event": "retry", "progress": .9, "cost": 2}]
human: list[TraceEvent] = trace[:2] + [{"step": 3, "actor": "model", "event": "human_check", "progress": .45, "cost": 1}]
for name, events in [("반복 상한", maxed), ("예산 상한", budgeted), ("확인 요청", human)]:
    print(name, "→", stop_reason(events))
assert stop_reason(maxed) == "최대 단계"
assert stop_reason(budgeted) == "예산"
assert stop_reason(human) == "사람 확인"'''),
],
"04-자율성의-대가": [
    md("# 자율성의 대가\n\n같은 최종 답에 도달한 두 합성 궤적을 비용·지연·경로 편차·디버깅 단서로 비교합니다."),
    md("## 실행 환경 준비\n\n사건별 시간과 비용 단위는 교육용 합성값입니다. 제공자 가격이나 Ch 20의 실제 호출 측정을 대신하지 않습니다."),
    code(SETUP_COST),
    md("## 합성 궤적 준비\n\n워크플로우는 경로가 고정되어 있고, 에이전트 후보는 관찰에 따라 검색을 반복했다고 가정합니다."),
    code('''traces: dict[str, list[CostEvent]] = {
    "workflow": [
        {"event": "retrieve", "ms": 240, "cost": 0},
        {"event": "generate", "ms": 900, "cost": 2},
        {"event": "validate", "ms": 30, "cost": 0},
    ],
    "agent_candidate": [
        {"event": "plan", "ms": 650, "cost": 1},
        {"event": "search", "ms": 380, "cost": 0},
        {"event": "inspect", "ms": 720, "cost": 1},
        {"event": "search", "ms": 410, "cost": 0},
        {"event": "finish", "ms": 830, "cost": 2},
    ],
}
print(*traces.items(), sep="\\n")'''),
    md("## 계기판 계산\n\n최종 답의 정확도는 주어지지 않았으므로 처리량 지표만 계산합니다."),
    code('''def metrics(events: list[CostEvent]) -> dict[str, int]:
    return {
        "steps": len(events),
        "latency_ms": sum(item["ms"] for item in events),
        "cost_units": sum(item["cost"] for item in events),
        "searches": sum(item["event"] == "search" for item in events),
    }

for name, events in traces.items():
    print(name, metrics(events))
assert metrics(traces["workflow"])["latency_ms"] == 1170
assert metrics(traces["agent_candidate"])["steps"] == 5'''),
    md("## 원인 위치 찾기\n\n지연이 큰 사건과 반복 사건을 표시하면 디버깅의 출발점을 만들 수 있습니다."),
    code('''for name, events in traces.items():
    slowest = max(events, key=lambda item: item["ms"])
    repeated: list[str] = sorted({item["event"] for item in events if sum(e["event"] == item["event"] for e in events) > 1})
    print(name, "가장 긴 사건:", slowest, "반복:", repeated)'''),
    md("## 경로 편차 비교\n\n같은 최종 결과라도 중간 경로가 다르면 최종 답만으로 효율과 잘못된 행동을 평가할 수 없습니다."),
    code('''second_agent_run: list[str] = ["plan", "search", "inspect", "finish"]
first_agent_run: list[str] = [item["event"] for item in traces["agent_candidate"]]
print("첫 경로:", first_agent_run)
print("둘째 경로:", second_agent_run)
print("경로 동일:", first_agent_run == second_agent_run)
print("Ch 29에서는 이런 중간 궤적을 별도 평가합니다.")
assert first_agent_run != second_agent_run'''),
],
"05-제품-트레이스와-자율성-진단": [
    md("# 제품 트레이스와 자율성 진단\n\n공식 저장소가 공개한 실제 실행 궤적 두 건과 제품 추적 단서를 읽고 중간 프로젝트 진단표를 완성합니다."),
    md("## 실행 환경 준비\n\n`public-trace-extracts.json`은 공개된 SWE-agent·mini-SWE-agent 원시 궤적에서 사건 순서를 추출한 자료입니다. 원본 커밋·URL·SHA-256·MIT 라이선스를 함께 기록했습니다. 이 컴퓨터에서 두 제품을 다시 실행한 로그는 아닙니다."),
    code(SETUP_EVIDENCE),
    md("## 실제 공개 궤적 읽기\n\n첫 궤적은 14개의 action-observation 턴, 둘째 궤적은 10개의 명령과 반환 결과를 포함합니다."),
    code('''traces = json.loads((LAB / "data/public-trace-extracts.json").read_text())
for trace in traces:
    print(trace["product"], "| 사건:", len(trace["events"]), "| SHA-256:", trace["sha256"][:12])
    print(" 경로:", " → ".join(event["action"] for event in trace["events"]))
    print(" 출처:", trace["raw_url"])
assert [len(trace["events"]) for trace in traces] == [14, 10]
assert all(len(trace["sha256"]) == 64 for trace in traces)'''),
    md("## 오류 뒤 경로 변경 확인\n\n원시 궤적에서 반환 실패나 편집 거부 다음에 실제 행동이 바뀐 위치를 읽습니다."),
    code('''for trace in traces:
    failures = [event for event in trace["events"] if event["outcome"] == "failure"]
    print(trace["product"], "실패 사건:", [(e["step"], e["action"], e["evidence"]) for e in failures])
    print(" 관찰 뒤 다음 행동:", trace["recovery_pairs"])
    print(" 하드코딩 경계:", trace["hardcoded_boundary"])
assert traces[0]["events"][9]["outcome"] == "failure"
assert traces[1]["events"][-1]["outcome"] == "unconfirmed"'''),
    md("## 공식 제품 추적 단서와 증거 수준\n\nCodex·Claude Code·Deep Research 문서는 추적 인터페이스와 행동 유형을 확인하는 보조 자료입니다. 실제 단일 실행 원문과 구분합니다."),
    code('''products = json.loads((LAB / "data/product-trace-evidence.json").read_text())
for product in products:
    print(product["product"], product["artifact_type"], "| 로컬 실행:", product["local_execution"])
    print(" 한계:", product["limitation"])
assert all(product["local_execution"] is False for product in products)'''),
    md("## 작성된 진단 예시\n\n중간 프로젝트 RAG 예시는 검색과 답변 경로가 정해져 있어 워크플로우 유지로 판정했습니다."),
    code('''example = json.loads((LAB / "data/autonomy-diagnostic-example.json").read_text())
for key, value in example.items():
    print(f"{key}: {value}")
sheet = list(csv.DictReader((LAB / "data/autonomy-diagnostic-sheet.csv").open()))
print("재사용 진단 질문 수:", len(sheet))
assert example["recommended_architecture"] == "워크플로우 유지"'''),
],
}


def write_notebooks() -> None:
    target = LAB / "notebooks"
    for slug, cells in NOTEBOOKS.items():
        for index, cell in enumerate(cells, 1):
            cell["id"] = f"cell-{index:02d}"
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.12"},
                "lesson_format": "experiment",
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        (target / f"{slug}.ipynb").write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )


PRODUCT_EVIDENCE = [
    {
        "product": "OpenAI Codex",
        "artifact_type": "official_public_trace_signals",
        "local_execution": False,
        "source_url": "https://openai.com/index/introducing-codex/",
        "checked": "2026-09-10",
        "observable_events": [
            {"event": "repository/file citation", "control": "제품 코드가 증거를 노출"},
            {"event": "terminal log", "control": "에이전트 행동의 증거; 세부 선택 주체는 공개 자료만으로 미확인"},
            {"event": "test result", "control": "도구 결과; 완료 판정의 세부 구현은 미확인"},
        ],
        "limitation": "공식 소개가 공개한 증거 유형이며 하나의 전체 실행 원문은 공개되지 않았습니다.",
    },
    {
        "product": "Anthropic Claude Code",
        "artifact_type": "official_public_trace_interface",
        "local_execution": False,
        "source_url": "https://code.claude.com/docs/en/cli-usage",
        "checked": "2026-09-10",
        "observable_events": [
            {"event": "stream-json turn output", "control": "제품 코드가 턴 사건을 직렬화"},
            {"event": "verbose turn-by-turn output", "control": "제품 코드가 증거를 노출"},
            {"event": "max-turns stop", "control": "코드로 정한 실행 상한"},
            {"event": "allowed/disallowed tools", "control": "코드로 정한 권한 경계"},
        ],
        "limitation": "CLI가 제공하는 추적 인터페이스이며 특정 사용자 작업의 실제 출력은 포함하지 않습니다.",
    },
    {
        "product": "OpenAI Deep Research",
        "artifact_type": "official_public_behavior_trace",
        "local_execution": False,
        "source_url": "https://openai.com/index/introducing-deep-research/",
        "checked": "2026-09-10",
        "observable_events": [
            {"event": "multi-step plan", "control": "모델 판단"},
            {"event": "web browse/search", "control": "모델이 고른 도구 행동"},
            {"event": "backtrack on information", "control": "관찰 뒤 모델 판단"},
            {"event": "Python analysis", "control": "모델이 고른 도구 행동"},
            {"event": "cited report", "control": "제품 출력 요건과 모델 생성"},
        ],
        "limitation": "공식 설명의 행동 경로를 사건으로 추출했으며 원시 내부 추론이나 완전한 실행 로그가 아닙니다.",
    },
]

PUBLIC_TRACES = [
    {
        "product": "SWE-agent v0.7.0 demonstration",
        "repository": "SWE-agent/SWE-agent",
        "commit": "3ea751c087f32b16e039a2233dd6eefecef325d5",
        "license": "MIT",
        "license_url": "https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/LICENSE",
        "raw_url": "https://raw.githubusercontent.com/SWE-agent/SWE-agent/3ea751c087f32b16e039a2233dd6eefecef325d5/trajectories/demonstrations/replay__marshmallow-code__marshmallow-1867__default__t-0.20__p-0.95__c-2.00__install-1___install_from_source/marshmallow-code__marshmallow-1867.traj",
        "sha256": "8856076ec31832f20aefa7f0a2714e3ad6bc752f14815d94d2e852e50213a459",
        "artifact_format": "SWE-agent .traj JSON; action-observation turns",
        "events": [
            {"step": 1, "action": "ls", "outcome": "success", "evidence": "repository listing"},
            {"step": 2, "action": "open setup.py", "outcome": "success", "evidence": "94-line file opened"},
            {"step": 3, "action": "install dev dependencies", "outcome": "success", "evidence": "editable install output"},
            {"step": 4, "action": "create reproduction", "outcome": "success", "evidence": "reproduce.py created"},
            {"step": 5, "action": "write reproduction", "outcome": "success", "evidence": "9-line script"},
            {"step": 6, "action": "run reproduction", "outcome": "success", "evidence": "observed 344"},
            {"step": 7, "action": "list files", "outcome": "success", "evidence": "reproduce.py present"},
            {"step": 8, "action": "find fields.py", "outcome": "success", "evidence": "one match"},
            {"step": 9, "action": "open target lines", "outcome": "success", "evidence": "TimeDelta serialization lines"},
            {"step": 10, "action": "edit without indentation", "outcome": "failure", "evidence": "E999 IndentationError; edit rejected"},
            {"step": 11, "action": "edit with indentation", "outcome": "success", "evidence": "file updated"},
            {"step": 12, "action": "rerun reproduction", "outcome": "success", "evidence": "observed 345"},
            {"step": 13, "action": "remove reproduction", "outcome": "success", "evidence": "temporary file removed"},
            {"step": 14, "action": "submit patch", "outcome": "success", "evidence": "exit_status submitted; one-line patch"},
        ],
        "recovery_pairs": [[10, 11, "편집 거부 뒤 들여쓰기를 고쳐 다시 편집"]],
        "hardcoded_boundary": "도구 문법 검사기가 들여쓰기 오류가 있는 편집을 거부하고 submit 도구가 종료를 표시합니다.",
        "interpretation_limit": "저장된 demonstration을 분석했으며 현재 버전의 SWE-agent를 다시 실행하지 않았습니다.",
    },
    {
        "product": "mini-SWE-agent GitHub issue fixture",
        "repository": "SWE-agent/mini-swe-agent",
        "commit": "04d809ceab9df28f9adaed044884180159172930",
        "license": "MIT",
        "license_url": "https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/LICENSE.md",
        "raw_url": "https://raw.githubusercontent.com/SWE-agent/mini-swe-agent/04d809ceab9df28f9adaed044884180159172930/tests/test_data/github_issue.traj.json",
        "sha256": "86d060a4881efc19b59b4ee6667b1c80b2b769544d4f6cecb42521e09e95c6a0",
        "artifact_format": "mini-SWE-agent message trajectory; assistant command and user tool-result pairs",
        "events": [
            {"step": 1, "action": "read absolute path", "outcome": "failure", "evidence": "returncode 1; file not found"},
            {"step": 2, "action": "list repository", "outcome": "success", "evidence": "returncode 0"},
            {"step": 3, "action": "list tests", "outcome": "success", "evidence": "returncode 0"},
            {"step": 4, "action": "read target file", "outcome": "success", "evidence": "returncode 0; missing colon visible"},
            {"step": 5, "action": "add missing colon", "outcome": "success", "evidence": "returncode 0"},
            {"step": 6, "action": "read edited file", "outcome": "success", "evidence": "returncode 0"},
            {"step": 7, "action": "run script", "outcome": "success", "evidence": "returncode 0; output 8.2"},
            {"step": 8, "action": "run issue input", "outcome": "failure", "evidence": "returncode 1; ZeroDivisionError"},
            {"step": 9, "action": "add zero check", "outcome": "success", "evidence": "returncode 0"},
            {"step": 10, "action": "submit plus git diff", "outcome": "unconfirmed", "evidence": "diff is present but no returncode wrapper; completion status not verified"},
        ],
        "recovery_pairs": [[1, 2, "잘못된 절대 경로 뒤 현재 저장소를 목록으로 확인"], [8, 9, "ZeroDivisionError 뒤 0 검사 추가"]],
        "hardcoded_boundary": "시스템 지시는 응답당 명령 하나와 단독 완료 명령을 요구하지만 마지막 행동은 완료 명령에 git 명령을 결합했습니다.",
        "interpretation_limit": "테스트 fixture를 분석했으며 패치의 요구 범위 적합성이나 외부 평가 통과는 확인하지 않았습니다.",
    },
]


def write_data() -> None:
    data = LAB / "data"
    data.mkdir(exist_ok=True)
    (data / "product-trace-evidence.json").write_text(
        json.dumps(PRODUCT_EVIDENCE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (data / "public-trace-extracts.json").write_text(
        json.dumps(PUBLIC_TRACES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    example = {
        "project": "중간 프로젝트 규정 RAG",
        "goal": "승인된 규정 문서에서 답과 출처를 반환",
        "path_predefined": "yes",
        "unknown_steps_required": "no",
        "model_decides_next_action": "no",
        "write_side_effect": "no",
        "stop_conditions": "검색 결과 없음, 출처 검증 실패, 답변 반환",
        "evidence": "retrieve → generate → citation_validate 순서가 모든 질문에 동일",
        "recommended_architecture": "워크플로우 유지",
        "reason": "경로가 고정되어 있으며 자율적 재검색의 품질 이득을 아직 측정하지 않았습니다.",
        "next_measurement": "Ch 20에서 고정 분기와 모델 분기의 호출 수·비용·결과 편차 비교",
    }
    (data / "autonomy-diagnostic-example.json").write_text(
        json.dumps(example, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = [
        ["1", "목표와 성공 조건을 한 문장으로 적을 수 있는가", "", ""],
        ["2", "필요한 단계를 입력 전에 나열할 수 있는가", "", ""],
        ["3", "관찰 결과에 따라 새 단계가 필요할 수 있는가", "", ""],
        ["4", "다음 행동을 모델이 정해야 하는가", "", ""],
        ["5", "쓰기·결제·삭제 같은 부작용이 있는가", "", ""],
        ["6", "최대 단계·예산·사람 확인·완료 조건이 있는가", "", ""],
        ["7", "현재 워크플로우의 실패를 실제 추적으로 확인했는가", "", ""],
        ["8", "자율성 추가 뒤 비교할 품질·비용·지연 지표가 있는가", "", ""],
        ["9", "권장 구조와 근거", "", ""],
    ]
    with (data / "autonomy-diagnostic-sheet.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "question", "answer", "evidence"])
        writer.writerows(rows)


def quiz(items: list[tuple[str, str, str]]) -> str:
    blocks = []
    for index, (level, question, answer) in enumerate(items, 1):
        blocks.append(
            f'<details class="quiz"><summary>{index}. {level}</summary>'
            f'<p class="quiz-q">{question}</p><p class="quiz-a">{answer} '
            '<b>오답 시 다시 볼 곳:</b> 이 페이지의 핵심 개념과 실험 결과 해석</p></details>'
        )
    return "".join(blocks)


COMMON_SOURCES = (
    '<li><a href="https://www.anthropic.com/engineering/building-effective-agents">Anthropic · Building effective agents</a> · 확인 2026-09-10</li>'
    '<li><a href="https://openai.github.io/openai-agents-python/tracing/">OpenAI Agents SDK · Tracing</a> · 확인 2026-09-10</li>'
)


SECTIONS = {
"01-워크플로우와-에이전트-경계": {
"meta":"강의 1h | 실습 0.5h | 새 용어 5", "title":"워크플로우와 에이전트 경계",
"goals":["다음 단계를 정하는 주체를 기준으로 워크플로우와 에이전트를 구분할 수 있습니다.","도구를 사용한다는 사실만으로 에이전트라고 부를 수 없는 이유를 설명할 수 있습니다.","중간 프로젝트의 결정 지점을 코드와 모델로 나누어 표시할 수 있습니다."],
"why":"중간 프로젝트에서는 검색, 생성, 출처 검증 순서를 모두 코드로 작성했습니다. 모델이 문장을 만들었으므로 겉으로는 지능적인 시스템처럼 보이지만, 다음에 무엇을 할지는 프로그램이 정했습니다. 이제 기능 이름보다 결정권의 위치를 살펴야 합니다. 그래야 고정된 흐름에 자율성을 추가할 필요가 있는지, 추가한다면 어떤 책임과 측정이 따라오는지 판단할 수 있습니다.",
"prior":"Ch 9의 첫 RAG는 검색한 뒤 답을 생성했고, Ch 13은 StateGraph의 노드와 엣지로 실행 순서를 명시했습니다. Ch 16은 입력 검증, 예산 상한, 재시도와 감사 기록을 모델 바깥 코드에 두었습니다. 이 세 챕터는 사람이 흐름을 적는 구조의 구체적인 선수 사례입니다.",
"concept":"공항의 자동 수하물 벨트는 여러 장비를 사용하지만 이동 경로가 정해져 있습니다. 반면 현장 담당자가 막힌 통로를 보고 다른 통로와 운반 수단을 고르면 관찰에 따라 다음 행동이 달라집니다. LLM 애플리케이션도 같은 질문으로 구분합니다. <strong>워크플로우(workflow)</strong>는 모델과 도구가 미리 작성한 코드 경로를 따라 실행되는 구조입니다. <strong>에이전트(agent)</strong>는 모델이 관찰 결과를 바탕으로 다음 과정과 도구 사용을 동적으로 정하는 구조입니다. <strong>결정 지점(decision point)</strong>은 여러 다음 행동 중 하나를 고르는 자리입니다. <strong>동적(dynamic)</strong>이라는 말은 입력과 중간 결과에 따라 필요한 단계의 수나 종류가 달라질 수 있음을 뜻합니다. 도구 호출은 둘 모두에 있을 수 있으므로 도구의 존재는 경계 기준이 아닙니다. 모델이 요약 문장을 만들더라도 코드가 언제 요약할지, 다음에 무엇을 실행할지 모두 정하면 워크플로우입니다.",
"result":"고정된 네 사례를 분류한 결과 정해진 환불 절차와 문서 요약 뒤 형식 검사는 워크플로우, 여러 파일의 결함 수정과 낯선 장애 원인 조사는 에이전트 후보로 표시됐습니다. 환불 사례의 도구 수를 세 개로 늘려도 결정 주체가 코드이므로 분류는 워크플로우로 유지됐습니다. 이 결과는 제품 성능 비교가 아니라 경계 정의를 코드로 확인한 분류 연습입니다. 실제 시스템에서는 로그에서 모델 출력, 도구 호출 요청, 프로그램 분기, 사람 승인 사건을 함께 읽어야 결정권을 판정할 수 있습니다.",
"notes":["제품 소개에서 ‘agent’라는 이름을 사용하더라도 실제 경로를 보지 않고 구조를 확정하지 않습니다.","모델이 분류값을 출력하고 코드가 그 값으로 정해진 세 갈래 중 하나를 고르는 라우팅은 모델 결정이 일부 포함된 워크플로우가 될 수 있습니다.","Ch 18의 오케스트레이터-워커에서 모델이 하위 작업을 동적으로 나누지만, Ch 17에서는 그 구조를 구현하지 않습니다."],
"next":"다음 절에서는 경로를 미리 적을 수 있는 문제에 워크플로우가 주는 예측 가능성과 검증 이점을 살펴봅니다.",
"quiz":[("이해","워크플로우와 에이전트를 가르는 중심 질문은 무엇인가요?","관찰 결과를 본 뒤 다음 단계와 도구 사용을 누가 정하는지 묻습니다."),("적용","모델로 이메일을 작성한 뒤 코드가 정한 검사와 저장 단계를 실행하면 어떤 구조인가요?","다음 단계가 코드에 미리 정해져 있으므로 워크플로우입니다."),("분석","도구가 세 개 있다는 사실만으로 에이전트라고 할 수 없는 이유는 무엇인가요?","워크플로우도 도구를 호출할 수 있으며 결정권이 코드에 있을 수 있기 때문입니다."),("평가","라우팅 모델이 세 경로 중 하나를 고르는 구조를 설명할 때 무엇을 함께 적어야 하나요?","모델이 고르는 범위와 코드가 제한한 후보·실패 처리·승인 경계를 함께 적어야 합니다.")]},
"02-워크플로우가-충분한-조건": {
"meta":"강의 1h | 실습 0.5h | 새 용어 5", "title":"워크플로우가 충분한 조건",
"goals":["경로 예측 가능성·반복성·실패 처리를 근거로 워크플로우 적합성을 진단할 수 있습니다.","자율성 추가 전에 품질 이득을 측정해야 하는 이유를 설명할 수 있습니다.","교육용 합성 비용과 실제 측정값을 구분해 해석할 수 있습니다."],
"why":"새로운 구조를 배우면 기존 프로젝트에도 적용하고 싶어집니다. 그러나 규정 질의응답처럼 단계가 분명한 문제는 고정 흐름이 더 적은 호출로 같은 요구를 충족할 수 있습니다. 모델 판단을 한 단계 추가할 때마다 호출과 지연, 실패 지점도 늘어납니다. 자율성은 기능 목록이 아니라 문제의 불확실성을 해결할 때만 비용을 감수할 근거가 생깁니다.",
"prior":"Ch 11과 Ch 15에서는 측정이 튜닝보다 먼저라는 순서를 배웠습니다. Ch 16에서는 호출 전에 계획 비용과 최대 호출 수를 확인했습니다. 이번에도 같은 원칙을 적용해 현재 워크플로우의 실패를 먼저 기록하고, 추가 구조가 그 실패를 줄이는지 비교할 측정 항목을 정합니다.",
"concept":"매일 같은 시간에 같은 정류장을 도는 버스는 노선표가 있는 편이 운영과 안내에 유리합니다. 목적지는 같지만 도로 폐쇄와 현장 요청에 따라 방문 순서를 계속 바꿔야 하는 복구 차량은 더 많은 판단이 필요합니다. <strong>경로 예측 가능성</strong>은 입력을 받기 전에 필요한 단계를 나열할 수 있는 정도입니다. <strong>반복성(repeatability)</strong>은 같은 조건에서 절차와 결과가 일관되게 재현되는 성질입니다. <strong>부작용(side effect)</strong>은 결제·삭제·전송처럼 외부 상태를 바꾸는 동작입니다. <strong>승인 지점</strong>은 위험한 동작 전에 사람이 확인하는 자리입니다. <strong>점진적 복잡성</strong>은 현재 구조로 해결하지 못한 증거가 있을 때 필요한 판단만 추가하는 설계 방식입니다. 단계가 알려져 있고 실패 경로가 명확하며 반복성이 중요하면 워크플로우를 우선 검토합니다.",
"result":"교육용 진단에서 사내 규정 질의응답은 6점으로 ‘워크플로우 우선’, 낯선 저장소 장애 수정은 1점으로 ‘제한된 에이전트 검토’가 나왔습니다. 규정 사례에 모델 판단 두 단계를 추가한 합성 시나리오는 호출 수 2회, 지연 3.5초, 비용 단위 3이 더 컸습니다. 이 숫자는 실제 모델 실행이나 가격표가 아니며 품질 향상을 측정하지 않았습니다. 따라서 ‘비용이 증가했으니 에이전트가 나쁘다’고 결론 내릴 수 없습니다. 현재 증거가 말하는 범위는 추가 판단에는 추가 실행이 필요하고, 그 대가를 정당화할 품질 지표가 별도로 필요하다는 것입니다.",
"notes":["적합 점수는 대화를 돕는 점검표이며 임계값 하나로 설계를 자동 확정하지 않습니다.","부작용이 큰 업무는 모델 판단 범위가 작더라도 권한 제한과 사람 승인이 필요합니다.","Ch 20에서 고정 분기와 모델 분기를 실제로 실행해 호출 수·비용·결과 편차를 측정하므로, 이 절의 합성값을 그 결과처럼 인용하지 않습니다."],
"next":"다음 절에서는 에이전트 후보에 필요한 모델·도구·루프를 정리하고 완료·단계·예산·사람 확인 정지 조건을 구분합니다.",
"quiz":[("이해","워크플로우가 적합한 조건 두 가지를 적어 보세요.","단계를 미리 나열할 수 있고 같은 입력에서 일관된 절차가 중요할 때 적합합니다."),("적용","정해진 규정 문서만 검색하고 출처를 검사하는 RAG에는 무엇을 먼저 선택하나요?","현재 실패 증거가 없다면 고정 검색·생성·검증 워크플로우를 먼저 선택합니다."),("분석","합성 비용표로 실제 청구액을 예측할 수 없는 이유는 무엇인가요?","모델·토큰·가격·네트워크를 실행해 측정한 값이 아니라 설계 비교용 고정 단위이기 때문입니다."),("평가","자율성을 추가하기 전에 남겨야 할 증거는 무엇인가요?","현재 워크플로우가 실패한 입력과 지점, 추가 구조 뒤 비교할 품질·비용·지연 지표를 남깁니다.")]},
"03-모델-도구-루프와-정지-조건": {
"meta":"강의 1h | 실습 0.5h | 새 용어 6", "title":"모델·도구·루프와 정지 조건",
"goals":["에이전트의 모델·도구·루프가 각각 맡는 역할을 설명할 수 있습니다.","완료·최대 단계·예산·사람 확인을 서로 다른 정지 이유로 기록할 수 있습니다.","상태 전이 시뮬레이션과 실제 도구 에이전트 구현을 구분할 수 있습니다."],
"why":"모델과 도구를 연결한 뒤 종료 규칙을 두지 않으면 같은 검색을 반복하거나 비용 상한을 넘길 수 있습니다. ‘모델이 알아서 끝낸다’는 설명만으로 운영 조건을 만들 수 없습니다. 모델이 완료를 제안하는 경로와 프로그램이 강제로 멈추는 경로, 사람이 판단을 이어받는 경로를 따로 설계해야 합니다.",
"prior":"Ch 13에서는 노드와 엣지로 상태가 이동하는 모습을 확인했고, Ch 16에서는 최대 호출 수와 비용 상한을 모델 호출 전에 검사했습니다. 이 절은 그 상태와 상한 개념을 에이전트 후보의 반복 구조에 적용합니다. 실제 ToolNode와 조건부 엣지는 Ch 20에서 처음 직접 조립합니다.",
"concept":"탐사팀에서 분석가는 다음 조사 장소를 고르고, 측정 장비는 현장의 값을 가져오며, 기록 담당자는 결과를 다음 판단 자료에 넣습니다. 탐사 완료 선언과 연료 한도, 위험 지역 앞의 책임자 확인도 필요합니다. <strong>모델(model)</strong>은 현재 상태를 읽고 다음 행동 또는 완료를 제안합니다. <strong>도구(tool)</strong>는 검색·파일 읽기·계산처럼 환경과 상호작용하고 결과를 반환합니다. <strong>루프(loop)</strong>는 모델의 선택, 도구 결과, 갱신된 상태를 다시 모델 입력으로 이어 주는 반복입니다. <strong>정지 조건(stopping condition)</strong>은 반복을 종료하는 판정입니다. <strong>하드 리밋(hard limit)</strong>은 최대 단계와 예산처럼 모델 의사와 관계없이 프로그램이 적용하는 상한입니다. <strong>사람 확인(human check)</strong>은 정보 부족이나 고위험 행동 앞에서 판단을 넘기는 종료 상태입니다.",
"result":"완료 사건이 있는 다섯 단계 합성 추적은 ‘완료’로 판정됐습니다. 마지막 완료 사건을 제거한 네 단계 추적은 정지 이유가 없어서 실행 중 상태로 남았습니다. 별도 사례에서는 여섯 사건에 도달한 경로가 ‘최대 단계’, 누적 비용이 상한에 도달한 경로가 ‘예산’, 확인 사건을 포함한 경로가 ‘사람 확인’으로 기록됐습니다. 이 코드는 사건 목록에 규칙을 적용했을 뿐 모델이 행동을 선택하거나 검색 도구를 실행하지 않았습니다. 따라서 자율 에이전트를 구현한 결과로 해석하지 않습니다.",
"notes":["완료 조건은 ‘좋아 보이는 답’보다 검증할 수 있는 산출물과 연결합니다. 예를 들면 테스트 통과와 필요한 파일 존재 여부입니다.","여러 정지 조건이 동시에 맞을 수 있으므로 판정 우선순위와 모든 발생 사건을 로그에 보존합니다.","모델의 완료 선언만 신뢰하지 말고 프로그램 상한과 필요한 사람 확인을 함께 둡니다."],
"next":"다음 절에서는 반복 단계가 늘 때 비용·지연·경로 편차·디버깅·평가 범위가 어떻게 넓어지는지 합성 궤적으로 측정합니다.",
"quiz":[("이해","모델·도구·루프의 역할을 각각 한 문장으로 설명해 보세요.","모델은 다음 행동을 제안하고, 도구는 환경 결과를 반환하며, 루프는 결과를 다음 판단 상태로 이어 줍니다."),("적용","결제 도구 호출 직전에 어떤 정지 또는 확인 조건을 둘 수 있나요?","금액·권한을 검사하고 사람이 승인하기 전에는 실행하지 않는 확인 조건을 둡니다."),("분석","완료 선언과 최대 단계가 동시에 발생하면 무엇을 기록해야 하나요?","적용한 우선순위뿐 아니라 완료 선언과 상한 도달 사건을 모두 보존해 원인을 추적합니다."),("평가","정지 조건 없이 모델의 판단만으로 반복하게 할 때 생기는 문제는 무엇인가요?","반복이 길어져 비용과 지연이 커지고 같은 행동을 되풀이해도 프로그램이 강제로 멈추기 어렵습니다.")]},
"04-자율성의-대가": {
"meta":"강의 1h | 실습 0.5h | 새 용어 6", "title":"자율성의 대가",
"goals":["자율성 증가를 비용·지연·경로 편차·디버깅·평가 관점에서 설명할 수 있습니다.","최종 답 평가와 중간 궤적 평가가 답하는 질문을 구분할 수 있습니다.","합성 지표가 보여 주는 범위와 실제 측정이 필요한 부분을 명시할 수 있습니다."],
"why":"에이전트 후보는 중간 결과를 보고 검색을 더 하거나 다른 도구를 선택할 수 있습니다. 이 유연성은 알려지지 않은 문제를 다룰 가능성을 늘리지만 실행 경로도 길고 다양하게 만듭니다. 최종 답 한 건만 보면 불필요한 반복, 잘못된 도구, 가장 느린 단계를 놓칠 수 있습니다. 자율성을 설계할 때는 결과 품질과 함께 실행 과정의 대가를 계기판에 올려야 합니다.",
"prior":"Ch 15에서는 p50·p95·p99와 평가 실행 기록을 다뤘고, Ch 16에서는 호출 수와 계획 비용 상한을 분리했습니다. 이 절은 같은 측정 습관을 에이전트 궤적에 적용합니다. 정식 궤적 평가 전략과 매칭 방식은 Ch 29에서 학습합니다.",
"concept":"택배가 도착했다는 사실만 보면 어느 길을 이용했고 몇 번 되돌아갔는지 알 수 없습니다. 배송 기록을 보면 긴 구간과 반복 방문을 찾을 수 있습니다. <strong>궤적(trajectory)</strong>은 한 요청에서 발생한 모델 판단, 도구 호출, 도구 결과, 사람 확인, 종료 사건의 순서입니다. <strong>비용(cost)</strong>은 모델 토큰, 유료 도구, 실행 자원에 드는 사용량입니다. <strong>지연(latency)</strong>은 요청부터 결과까지 걸린 시간이며 각 단계의 대기와 실행 시간이 누적됩니다. <strong>경로 편차</strong>는 같은 목적의 실행이 서로 다른 사건 순서를 갖는 정도입니다. <strong>디버깅(debugging)</strong>은 실패가 시작된 사건과 입력·출력을 찾아 고치는 과정입니다. <strong>평가 난이도</strong>는 정답 경로가 여러 개일 때 좋은 과정과 불필요하거나 위험한 과정을 함께 판정해야 하는 부담입니다.",
"result":"합성 워크플로우는 3단계·1,170ms·비용 단위 2, 에이전트 후보는 5단계·2,990ms·비용 단위 4로 계산됐습니다. 에이전트 후보에서는 검색 사건이 두 번 나타났고 가장 긴 사건은 830ms의 완료 생성이었습니다. 둘째 합성 실행에서는 검색이 한 번뿐이라 첫 경로와 달랐습니다. 숫자는 구조를 읽는 연습을 위한 고정값이며 실제 제품 성능이나 가격을 나타내지 않습니다. 또한 두 경로의 최종 답 품질이 주어지지 않았으므로 더 긴 경로가 유용했는지 판단할 수 없습니다.",
"notes":["비용 평균만 보면 드물게 매우 긴 실행을 놓칠 수 있으므로 운영에서는 분포와 상위 백분위수를 함께 봅니다.","전체 프롬프트와 도구 결과를 저장하면 개인정보와 비공개 자료가 포함될 수 있으므로 추적 보존 범위와 마스킹을 정합니다.","최종 답이 맞아도 불필요한 쓰기 도구 호출이나 반복이 있으면 운영상 실패일 수 있습니다."],
"next":"마지막 절에서는 실제 제품의 공식 공개 추적 단서를 읽고, 자기 중간 프로젝트에 필요한 자율성을 한 장으로 진단합니다.",
"quiz":[("이해","궤적에는 어떤 사건이 포함되나요?","모델 판단, 도구 호출과 결과, 사람 확인, 종료처럼 한 요청의 중간 사건과 순서가 포함됩니다."),("적용","최종 답은 맞지만 검색을 다섯 번 반복했습니다. 어떤 지표를 추가로 보나요?","단계 수, 도구 호출 수, 지연, 비용, 반복 사건과 각 단계의 입력·출력을 봅니다."),("분석","두 합성 경로의 비용 차이만으로 더 좋은 구조를 고를 수 없는 이유는 무엇인가요?","최종 품질과 실패율을 측정하지 않았으므로 추가 비용이 성능 이득을 만들었는지 알 수 없습니다."),("평가","추적에 전체 입력을 저장할 때 먼저 정할 것은 무엇인가요?","개인정보와 비공개 자료의 마스킹, 접근 권한, 보존 기간과 삭제 기준을 정합니다.")]},
"05-제품-트레이스와-자율성-진단": {
"meta":"강의 1h | 실습 1h | 새 용어 6", "title":"제품 트레이스와 자율성 진단",
"goals":["공식 공개 자료에서 모델 판단·도구 사건·프로그램 제한을 구분할 수 있습니다.","공개 추적 단서와 로컬 실행 로그의 증거 수준 차이를 설명할 수 있습니다.","중간 프로젝트의 자율성 진단 한 장을 근거와 함께 작성할 수 있습니다."],
"why":"‘실제 에이전트 제품’이라는 이름만 비교하면 어떤 결정이 모델에 있고 어떤 제한이 코드에 있는지 보이지 않습니다. 실행 과정을 사건 단위로 나누면 도구 결과, 턴 상한, 권한 경계, 완료 증거를 구분할 수 있습니다. 다만 공식 소개 페이지가 전체 원시 로그를 공개하지 않는 경우도 많습니다. 이때 확인한 사실과 알 수 없는 내부 과정을 분리해 적는 태도가 추적 분석의 첫 기준입니다.",
"prior":"앞의 네 절에서 결정 주체, 워크플로우 적합 조건, 정지 조건, 궤적 지표를 배웠습니다. 중간 프로젝트에서는 검색→생성→출처 검증 순서를 직접 작성했습니다. 이 절은 그 프로젝트를 진단표에 넣고 Ch 20의 실제 비교 실험에서 무엇을 측정할지 준비합니다.",
"concept":"경기 중계의 하이라이트와 전체 심판 기록은 증거의 깊이가 다릅니다. 하이라이트로 확인한 장면은 말할 수 있지만 보이지 않은 모든 판정을 추정해서는 안 됩니다. <strong>트레이스(trace)</strong>는 한 요청의 처음부터 끝까지 연결된 실행 기록입니다. <strong>스팬(span)</strong>은 모델 생성이나 도구 호출처럼 시작과 끝이 있는 한 작업 단위입니다. <strong>공개 추적 단서</strong>는 제품 공식 문서가 공개한 로그 유형, 사건 이름, 제한 옵션, 행동 경로입니다. <strong>원시 로그(raw log)</strong>는 특정 실행에서 실제로 저장된 사건과 입력·출력입니다. <strong>증거 수준</strong>은 출처가 실제 실행 원문인지, 공식 동작 설명인지, 교육용 재구성인지 구분하는 표시입니다. <strong>자율성 진단</strong>은 문제의 불확실성, 결정권, 부작용, 정지 조건, 측정 계획을 한 장에 정리하는 절차입니다.",
"result":"SWE-agent v0.7.0 공개 demonstration은 14개의 action-observation 사건을 포함했습니다. 재현 스크립트가 344를 출력한 뒤 대상 코드를 찾았고, 10번째 편집은 들여쓰기 오류로 도구가 거부했습니다. 다음 사건에서 들여쓰기를 고쳐 다시 편집하고 재현값 345를 확인한 뒤 패치를 제출했습니다. mini-SWE-agent 공개 fixture는 10개의 명령 사건을 포함했습니다. 첫 절대 경로 읽기가 실패하자 저장소와 tests 폴더를 확인했고, 문법 오류를 고친 뒤 실행값 8.2를 확인했습니다. 원래 입력 23÷0에서는 ZeroDivisionError가 발생해 0 검사를 추가했습니다. 마지막에는 시스템이 단독 완료 명령을 요구했는데 git 명령을 결합했으며 반환 코드 래퍼도 없어 규칙 준수와 완료 증거가 불충분합니다. 두 자료는 커밋과 SHA-256으로 고정된 실제 공개 실행 궤적이지만 이 컴퓨터에서 제품을 다시 실행한 결과는 아닙니다. Codex·Claude Code·Deep Research 자료는 보조적인 공식 추적 단서로만 구분했습니다. 작성 예시의 규정 RAG는 자율 재검색의 측정된 이득이 없어 ‘워크플로우 유지’로 판정했습니다.",
"notes":["실제 공개 궤적은 저장된 당시 제품 버전의 행동입니다. 최신 제품 전체의 성능으로 일반화하지 않습니다.","mini-SWE-agent fixture에서 0 검사를 추가한 행동이 원래 요청 범위에 맞는지는 별도 평가가 필요합니다. 실행 성공과 요구 충족을 구분합니다.","원시 파일은 MIT 라이선스이며 실습 추출본에 저장소·커밋·원문 URL·SHA-256을 남겼습니다.","진단표의 결론은 현재 증거에 대한 결정이며 Ch 20 비교 결과가 나오면 갱신합니다."],
"next":"Ch 18에서는 고정된 네 패턴과 동적으로 작업을 나누는 오케스트레이터-워커를 직접 구현합니다. Ch 20에서는 이 과정에서 처음으로 ToolNode 그래프 루프가 모델의 도구 선택을 받아 실행되며, 고정 분기와 비용·지연·결과 편차를 실제로 비교합니다.",
"quiz":[("이해","공개 추적 단서와 원시 로그의 차이는 무엇인가요?","공개 단서는 공식 문서가 설명한 사건 유형과 인터페이스이고, 원시 로그는 특정 실행에서 실제 발생한 사건과 값입니다."),("적용","Claude Code의 `--max-turns`는 모델 판단과 하드코딩 중 어디에 해당하나요?","런타임이 적용하는 최대 턴 제한이므로 하드코딩된 정지 경계입니다."),("분석","Deep Research의 웹 검색을 모델 판단으로 표시하려면 어떤 근거가 필요한가요?","공식 자료가 모델이 다단계 경로를 계획하고 정보에 반응해 검색·되돌아가기를 수행한다고 설명하는 근거가 필요합니다."),("평가","자율성 진단이 ‘워크플로우 유지’로 끝나도 타당한 경우는 언제인가요?","경로가 알려져 있고 현재 실패 증거와 자율성의 측정된 품질 이득이 없으며 고정 흐름이 요구를 충족할 때 타당합니다.")]},
}

PROCEDURES = {
    "01-워크플로우와-에이전트-경계": "실제 로그를 볼 때는 먼저 사건을 시간순으로 적습니다. 각 사건 옆에 다음 행동의 후보를 누가 만들었는지, 누가 하나를 골랐는지, 실패 때 어떤 경로가 강제됐는지 표시합니다. 모델이 만든 텍스트와 모델이 고른 행동을 구분하고, 도구가 많다는 사실을 자율성의 증거로 사용하지 않습니다. 마지막으로 입력이 바뀌어도 코드가 같은 경로를 강제하는지 확인합니다.",
    "02-워크플로우가-충분한-조건": "첫째, 현재 워크플로우의 실제 실패 사례를 모읍니다. 둘째, 실패가 고정 분기·검증·데이터 보강으로 해결되는지 확인합니다. 셋째, 필요한 단계를 입력 전에 적기 어려운 경우에만 모델 판단 후보를 표시합니다. 넷째, 추가 판단 전후에 같은 평가셋으로 품질·호출 수·지연·비용을 비교할 계획을 세웁니다. 측정하지 않은 유연성을 이점으로 계산하지 않습니다.",
    "03-모델-도구-루프와-정지-조건": "루프 설계표에는 현재 상태, 모델이 선택할 수 있는 행동, 각 도구의 반환값, 상태 갱신 규칙을 적습니다. 그 다음 정상 완료, 최대 단계, 예산 상한, 사람 확인을 종료 상태로 나눕니다. 정지 이유가 여러 개면 모두 기록하되 프로그램이 어떤 우선순위로 반환할지 정합니다. 부작용이 있는 행동은 일반 반복 안에 그대로 넣지 않고 별도 승인 경계를 둡니다.",
    "04-자율성의-대가": "한 요청의 최종 답과 함께 단계 수, 도구 호출 수, 각 사건의 시간, 토큰 또는 비용 단위, 오류, 재시도, 종료 이유를 모읍니다. 여러 요청을 실행한 뒤 평균만 보지 않고 긴 실행의 상위 백분위수와 경로 종류를 봅니다. 품질이 같은데 경로가 길어진 사례와 비용이 늘었지만 품질이 좋아진 사례를 분리해야 구조의 대가와 이득을 함께 판단할 수 있습니다.",
    "05-제품-트레이스와-자율성-진단": "먼저 원시 궤적의 저장소, 커밋, 해시, 라이선스를 확인합니다. 다음으로 사건 순서를 변경하지 않고 행동과 관찰을 짝지어 적습니다. 실패 직후의 다음 행동을 찾아 모델이 환경 피드백에 반응한 자리를 표시하고, 도구 검사·턴 상한·완료 명령처럼 코드가 강제한 경계를 따로 표시합니다. 마지막으로 성공 출력, 요구 충족, 범위 준수, 종료 증거를 서로 다른 평가 질문으로 남깁니다.",
}

DIAGRAMS = {
    "01-워크플로우와-에이전트-경계": "입력과 현재 상태에서 시작해 다음 단계를 결정하는 지점을 봅니다. 보라색 결정이 항상 코드의 고정 후보 안에서만 움직이는지, 관찰 결과에 따라 새 행동을 고를 수 있는지가 경계입니다.",
    "02-워크플로우가-충분한-조건": "현재 실패 증거가 첫 입력입니다. 경로를 미리 적을 수 있으면 파란 워크플로우를 먼저 선택하고, 노란 비교 계획에서 품질 이득을 확인한 뒤에만 복잡성을 늘립니다.",
    "03-모델-도구-루프와-정지-조건": "보라색 모델 판단과 초록 도구 결과가 상태 갱신을 거쳐 반복됩니다. 노란 종료 상자는 정상 완료와 강제 상한, 사람 확인을 함께 나타내므로 각 이유를 구분해 기록합니다.",
    "04-자율성의-대가": "초록 궤적에서 파란 단계 수와 반복을 세고 노란 비용·지연을 합산합니다. 마지막 평가는 가장 긴 사건과 반복 위치를 실제 원인 후보로 연결합니다.",
    "05-제품-트레이스와-자율성-진단": "공식 원시 궤적과 공개 추적 단서를 먼저 구분합니다. 사건마다 모델 판단, 도구 결과, 코드 제한, 미확인을 표시한 뒤 자기 프로젝트의 구조 선택과 다음 측정으로 이어집니다.",
}

SUMMARIES = {
    "01-워크플로우와-에이전트-경계": ["워크플로우는 미리 작성한 코드 경로를 따릅니다.", "에이전트 후보에서는 모델이 관찰 뒤 다음 행동을 고릅니다.", "도구 수와 모델 생성 여부만으로 경계를 정하지 않습니다."],
    "02-워크플로우가-충분한-조건": ["단계와 실패 처리를 미리 적을 수 있으면 워크플로우를 우선합니다.", "자율성은 측정된 품질 이득이 추가 실행의 대가를 정당화할 때 검토합니다.", "합성 비용 단위는 실제 청구나 성능 측정값이 아닙니다."],
    "03-모델-도구-루프와-정지-조건": ["모델은 행동을 제안하고 도구는 환경 결과를 반환하며 루프가 상태를 잇습니다.", "완료·최대 단계·예산·사람 확인은 서로 다른 정지 이유입니다.", "이 절의 코드는 사건 판정기이며 실제 도구 에이전트가 아닙니다."],
    "04-자율성의-대가": ["자율성이 커지면 단계·비용·지연과 가능한 경로도 늘어날 수 있습니다.", "최종 답만으로 반복 호출과 느린 사건을 찾을 수 없습니다.", "합성 궤적은 계기판 계산을 보여 주며 제품 우열을 증명하지 않습니다."],
    "05-제품-트레이스와-자율성-진단": ["SWE-agent와 mini-SWE-agent의 실제 공개 궤적에서 실패와 회복 순서를 확인했습니다.", "제품 설명의 추적 단서와 특정 실행의 원시 로그를 구분합니다.", "현재 증거가 고정 경로를 지지하면 ‘워크플로우 유지’도 완전한 진단입니다."],
}


def write_sources() -> None:
    for index, (slug, item) in enumerate(SECTIONS.items(), 1):
        goals = "".join(f"<li>{goal}</li>" for goal in item["goals"])
        notes = "".join(f"<li>{note}</li>" for note in item["notes"])
        extra_sources = ""
        if index == 5:
            extra_sources = (
                '<li><a href="https://openai.com/index/introducing-codex/">OpenAI · Introducing Codex</a> · 확인 2026-09-10</li>'
                '<li><a href="https://code.claude.com/docs/en/cli-usage">Anthropic · Claude Code CLI reference</a> · 확인 2026-09-10</li>'
                '<li><a href="https://openai.com/index/introducing-deep-research/">OpenAI · Introducing deep research</a> · 확인 2026-09-10</li>'
                '<li><a href="https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/docs/usage/trajectories.md">SWE-agent · trajectory documentation and demonstration</a> · 커밋 3ea751c · MIT · 확인 2026-09-10</li>'
                '<li><a href="https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/tests/test_data/github_issue.traj.json">mini-SWE-agent · public trajectory fixture</a> · 커밋 04d809c · MIT · 확인 2026-09-10</li>'
            )
        summary = "".join(f"<li>{line}</li>" for line in SUMMARIES[slug])
        source = f'''<!--meta: {item["meta"]} | 코드 Jupyter Notebook -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{item["why"]}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{item["prior"]}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예와 정의</h3><p>{item["concept"]}</p><h3>판단 절차</h3><p>{PROCEDURES[slug]}</p><h3>도식 읽기</h3>{{{{svg:{index:02d}-흐름}}}}<p>{DIAGRAMS[slug]} 초록은 입력과 관찰 자료, 파랑은 코드 처리, 보라는 모델 판단, 노랑은 측정을 나타냅니다.</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>노트북은 Python 3.12 새 커널에서 독립 실행되며 외부 API를 호출하지 않습니다. 고정된 교육용 사례와 공개 자료 추출본을 사용하므로 실제 모델 품질·비용·지연 측정과 구분합니다.</p>{{{{notebook:{slug}}}}}<p class="look"><b>확인할 점</b> — 출력의 결정 주체, 정지 이유, 합성값 또는 공개 자료라는 증거 수준을 함께 읽습니다.</p>
<h2 id="b6"><span class="no">6</span>실험 결과 해석</h2><p>{item["result"]}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{notes}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{summary}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {item["next"]}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz(item["quiz"])}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{COMMON_SOURCES}{extra_sources}</ul>
'''
        (BOOK / "_src" / f"{slug}.html").write_text(source, encoding="utf-8")


def main() -> None:
    write_data()
    write_notebooks()
    write_sources()
    print("wrote 5 notebooks, 5 sources, and 3 data files")


if __name__ == "__main__":
    main()
