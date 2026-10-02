"""Ch 15 정본 원고·노트북·도식을 생성한다."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LAB = ROOT / "labs/part4/ch15-evaluation-advanced"

SECTIONS = [
    ("01-실패-로그와-평가-대상", "실패 로그와 평가 대상", "experiment"),
    ("02-4대-RAG-평가자", "4대 RAG 평가자", "experiment"),
    ("03-judge-프롬프트와-편향", "judge 프롬프트와 편향", "experiment"),
    ("04-제시-라벨과-일치율", "제시 라벨과 일치율", "experiment"),
    ("05-로컬-트레이싱과-지연", "로컬 트레이싱과 지연", "experiment"),
    ("06-대화당-비용-백분위수", "대화당 비용 백분위수", "experiment"),
    ("07-회귀-스위트", "회귀 스위트", "paired"),
    ("08-Batch-평가-입력", "Batch 평가 입력", "experiment"),
]

OFFICIAL = (
    '<li><a href="https://docs.langchain.com/langsmith/evaluate-rag-tutorial">LangSmith RAG 평가 안내</a> · 확인 2026-09-10 · LangSmith 0.7.14</li>'
    '<li><a href="https://docs.langchain.com/langsmith/log-llm-trace">LangSmith LLM trace 기록</a> · 확인 2026-09-10</li>'
    '<li><a href="https://developers.openai.com/api/reference/resources/batches">OpenAI Batch API</a> · 확인 2026-09-10</li>'
)

FIGURE_READ = {
    "01-실패-로그와-평가-대상": "왼쪽의 Ch12 검색 설정 36행에서 출발해 질문별 정답·후보를 확인합니다. 누락과 낮은 순위를 분류한 뒤 답변과 전달 문서를 준비하고, 발견한 실패에 맞는 평가를 선택하는 순서입니다.",
    "02-4대-RAG-평가자": "네 상자는 평가 이름과 비교 대상을 짝지어 보여 줍니다. Correctness만 정답 답변이 필요하며, 나머지는 질문·응답·전달 문서 가운데 표시된 두 대상을 비교합니다.",
    "03-judge-프롬프트와-편향": "같은 후보 A와 B를 A→B, B→A 순서로 각각 평가 모델에 전달합니다. 평가 모델이 고른 위치를 원래 후보 ID로 변환한 뒤 두 실행이 같은 후보를 골랐는지 비교합니다.",
    "04-제시-라벨과-일치율": "교재 제시 라벨과 평가 모델 값을 사례 ID로 짝지어 일치율을 계산합니다. 제시 라벨은 사람 수집 라벨과 구분하며, 마지막에는 불일치 사례의 원문을 확인합니다.",
    "05-로컬-트레이싱과-지연": "호출 시작, 첫 텍스트 도착, 마지막 응답 완료 시각으로 TTFT와 total을 각각 계산합니다. 입력·출력·캐시 사용량은 시간선 아래에서 서로 다른 필드로 기록합니다.",
    "06-대화당-비용-백분위수": "대화별 합성 비용의 범위를 확인하고 작은 값부터 정렬합니다. 표본 수와 계산 규칙을 고정한 뒤 p50·p95·p99를 읽고 비싼 사례를 조사합니다.",
    "07-회귀-스위트": "고정 사례와 평가 기준을 유지한 채 이전 결과와 변경 후 결과를 사례 ID로 비교합니다. 성공에서 실패로 바뀐 사례를 고치고 같은 기준으로 다시 검사합니다.",
    "08-Batch-평가-입력": "평가 사례에 custom_id를 붙여 JSONL 요청을 만들고 형식과 ID 중복을 검사합니다. 모의 결과를 ID로 연결하는 연습과 실제 Batch 제출 완료 상태를 구분합니다.",
}

ANALOGY = {
    "01-실패-로그와-평가-대상": "병원 접수 기록만 보고 치료가 실패했다고 말할 수는 없습니다. 접수, 검사, 처방은 서로 다른 단계입니다. RAG에서도 검색 설정 행과 생성 응답 행을 먼저 구분해야 실제로 발생한 실패를 올바른 단계에 연결할 수 있습니다.",
    "02-4대-RAG-평가자": "한 답변을 네 방향에서 비추는 손전등을 떠올려 봅니다. 정답과 같은지, 질문을 직접 다루는지, 문서가 주장을 뒷받침하는지, 가져온 문서가 질문에 필요한지를 각각 비추면 어두운 지점이 달라집니다.",
    "03-judge-프롬프트와-편향": "두 음식을 비교할 때 접시 위치를 바꾸었는데 선택도 함께 바뀐다면 맛 이외의 조건이 판정에 영향을 준 것입니다. 평가 모델도 후보 순서와 답변 길이에 영향을 받을 수 있어 순서 교환 검사가 필요합니다.",
    "04-제시-라벨과-일치율": "답안지를 만든 사람의 예시 점수와 여러 채점자가 독립적으로 매긴 점수는 근거가 다릅니다. 두 자료를 같은 이름으로 부르면 일치율의 의미도 달라집니다. 이 절은 작성자 기준과 사람 수집 라벨을 구분합니다.",
    "05-로컬-트레이싱과-지연": "택배가 늦었을 때 전체 배송 시간만 보면 창고, 간선 운송, 지역 배송 중 어디가 늦었는지 알 수 없습니다. 실행 추적도 재작성·검색·리랭킹·생성 구간을 따로 기록해 지연의 위치를 찾습니다.",
    "06-대화당-비용-백분위수": "식당의 주문 한 건에는 음료와 추가 메뉴가 여러 줄로 찍힐 수 있습니다. 메뉴 한 줄의 평균 가격보다 손님 한 팀의 총 결제액을 봐야 매출과 비용을 관리할 수 있습니다. 모델 호출도 대화별로 합산합니다.",
    "07-회귀-스위트": "학급 평균이 올라도 한 학생이 필수 과목에서 낙제할 수 있습니다. 같은 방식으로 평균 품질만 확인하면 핵심 질문 하나의 실패를 놓칩니다. 회귀 스위트는 평균과 필수 사례를 함께 검사합니다.",
    "08-Batch-평가-입력": "택배 상자에 운송장 번호를 붙이듯 비동기 평가 요청에는 custom_id를 붙입니다. 나중에 결과가 다른 순서로 도착해도 이 ID로 원래 사례를 찾고 누락이나 중복을 확인할 수 있습니다.",
}

RESULTS = {
    "01-실패-로그와-평가-대상": "Ch12 개발 로그는 정확히 36행이었고 생성 응답 필드는 0개였습니다. 선택 설정의 시험 결과에서 Q006과 Q090은 Recall@5가 1이지만 정답 문서가 2위여서 nDCG@5가 각각 0.6309였습니다. 준비 단계에서 이 두 질문과 Q002에 문서 본문을 전달해 실제 답변 3건을 만들었습니다. 따라서 관찰한 실패는 검색 순위 문제 2건이며 생성 실패 36건이 아닙니다.",
    "02-4대-RAG-평가자": "Q002에서 실제 근거 충실도 평가 모델은 1을 반환했습니다. 작성자 기준 답변과 응답의 단어 겹침은 0.667, 질문과 응답은 0.5, 질문과 검색 문서는 0.5였습니다. 세 겹침 값은 계산 절차를 보여 주는 교육용 근사값이며 LangSmith 평가 결과로 해석하지 않습니다. 실제 의미 평가로 실행한 값은 근거 충실도 평가 모델 하나입니다.",
    "03-judge-프롬프트와-편향": "첫 후보 ID만 반환하는 잘못된 평가자는 short→long 순서에서 short를, long→short 순서에서 long을 골랐습니다. 후보 내용은 같고 순서만 바뀌었으므로 승자 변경은 위치에 의존한 판정입니다. 이 실험은 편향 검사 방법을 보여 주며 `gpt-5.4-mini`의 실제 위치 편향률을 측정하지 않았습니다.",
    "04-제시-라벨과-일치율": "교육용 작성자 기준과 예시 평가 모델 라벨 6쌍 가운데 5쌍이 같아 정확 일치율은 0.833이었습니다. 혼동 행렬은 TP 3, TN 2, FP 1, FN 0이었습니다. 이 수치는 독립 검토자가 만든 인간 라벨과의 일치율이 아니므로 운영 평가 모델 적용 근거로 사용할 수 없습니다.",
    "05-로컬-트레이싱과-지연": "고정 로컬 실행 추적에서 생성은 61ms에 시작했고 첫 텍스트는 146ms에 도착하여 첫 토큰 도착 시간은 85ms였습니다. 전체 요청은 0ms부터 301ms까지여서 전체 지연은 301ms였습니다. 캐시 읽기 420개의 토큰과 캐시 생성 80개의 토큰을 분리해 저장했습니다. 실제 LangSmith 클라우드 실행 추적 업로드는 수행하지 않았습니다.",
    "06-대화당-비용-백분위수": "합성 대화 비용 100개를 가장 가까운 순위 방식으로 정렬했습니다. p50과 p99의 비율이 10배를 넘어 일부 높은 비용이 평균에서 충분히 드러나지 않는 구조를 확인했습니다. 이 값은 백분위수 계산을 위한 교육용 원자료이며 실제 모델 가격이나 청구액을 나타내지 않습니다.",
    "07-회귀-스위트": "평균 0.66 이상만 보는 Before 기준은 Q090 점수 0을 포함하고도 통과했습니다. 사례별 점수, p95 전체 지연 1,500ms 이하, p99 비용 0.08달러 이하를 함께 검사한 After 기준은 같은 입력을 실패로 판정했습니다. Q090 점수를 1로 수정한 교육용 결과는 같은 기준을 통과했습니다.",
    "08-Batch-평가-입력": "세 사례를 <code>/v1/responses</code>용 JSONL 3행으로 만들고 JSON 구문, 요청 식별자 유일성, POST 메서드, 엔드포인트, 요청 본문 필드를 모두 통과했습니다. 이어서 만든 모의 결과에서는 누락 ID, 중복 ID와 알 수 없는 ID를 각각 검출했습니다. 실제 업로드·완료·50% 할인 청구는 확인하지 않았습니다.",
}

SUMMARIES = {
    "01-실패-로그와-평가-대상": ["36개 Ch12 행은 생성 답변이 없는 검색 설정 로그입니다.", "Q006과 Q090에서 정답 문서의 낮은 순위를 실제 검색 문제로 분류했습니다.", "실제 답변을 생성한 세 사례만 생성 평가 대상으로 등록했습니다."],
    "02-4대-RAG-평가자": ["네 평가자는 서로 다른 두 대상을 비교합니다.", "Correctness만 정답 답변이 필요하고 gold 문서 ID로 대신할 수 없습니다.", "코드 근사값과 실제 LLM judge 결과를 구분해 기록했습니다."],
    "03-judge-프롬프트와-편향": ["후보 순서를 바꾸고 승자를 원래 ID로 변환해야 위치 영향을 확인할 수 있습니다.", "평가 모델·온도·프롬프트 해시·출력 형식을 함께 고정했습니다.", "운영 평가 모델은 사람 기준과 비교하기 전까지 미정입니다."],
    "04-제시-라벨과-일치율": ["작성자 기준 라벨과 사람 수집 라벨은 서로 다른 자료입니다.", "일치율 0.833과 혼동 행렬을 같은 여섯 사례에서 계산했습니다.", "운영 적용에는 도메인 검토자의 독립 라벨이 추가로 필요합니다."],
    "05-로컬-트레이싱과-지연": ["실행 추적은 RAG 단계를 하위 실행으로 나눕니다.", "첫 토큰 도착 시간 85ms와 전체 지연 301ms는 시작점과 끝점이 다릅니다.", "캐시 읽기와 생성 토큰을 별도 필드로 보존했습니다."],
    "06-대화당-비용-백분위수": ["여러 호출을 대화 ID로 합산한 비용을 주요 관리 지표로 사용합니다.", "p50·p95·p99는 일반 구간과 높은 비용 구간을 함께 보여 줍니다.", "표본 수와 백분위수 계산법을 결과와 함께 기록합니다."],
    "07-회귀-스위트": ["평균만 보는 기준은 Q090 핵심 실패를 놓쳤습니다.", "사례별 품질과 지연·비용 상한을 하나의 통과 조건으로 검사했습니다.", "데이터나 평가 모델이 바뀌면 기준선 버전도 다시 측정합니다."],
    "08-Batch-평가-입력": ["Batch 요청은 요청 식별자(custom_id)로 원래 사례와 연결합니다.", "JSONL 형식과 요청 식별자 문제를 업로드 전에 검사했습니다.", "입력 검증과 실제 제출·완료·할인 확인을 구분했습니다."],
}

REFERENCES = {
    "01-실패-로그와-평가-대상": '<li><a href="https://docs.langchain.com/langsmith/evaluation-concepts">LangSmith 평가 개념</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluation-types">LangSmith 평가 유형</a> · 확인 2026-09-10</li>',
    "02-4대-RAG-평가자": '<li><a href="https://docs.langchain.com/langsmith/evaluate-rag-tutorial">LangSmith RAG 평가 안내</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluation-concepts">LangSmith 평가 개념</a> · 확인 2026-09-10</li>',
    "03-judge-프롬프트와-편향": '<li><a href="https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback">사람 피드백으로 judge 개선하기</a> · 확인 2026-09-10</li><li><a href="https://arxiv.org/abs/2306.05685">LLM-as-a-Judge 연구 논문</a> · 확인 2026-09-10</li>',
    "04-제시-라벨과-일치율": '<li><a href="https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback">사람 피드백으로 judge 개선하기</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluation-concepts">LangSmith 인간 평가와 annotation queue</a> · 확인 2026-09-10</li>',
    "05-로컬-트레이싱과-지연": '<li><a href="https://docs.langchain.com/langsmith/log-llm-trace">LangSmith LLM trace 기록</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluation-concepts">LangSmith run과 trace 개념</a> · 확인 2026-09-10</li>',
    "06-대화당-비용-백분위수": '<li><a href="https://docs.langchain.com/langsmith/log-llm-trace">LangSmith 토큰·비용 메타데이터</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluate-llm-application">LangSmith 실험의 지연·토큰 비교</a> · 확인 2026-09-10</li>',
    "07-회귀-스위트": '<li><a href="https://docs.langchain.com/langsmith/evaluation-types">LangSmith 회귀 평가</a> · 확인 2026-09-10</li><li><a href="https://docs.langchain.com/langsmith/evaluation-concepts">LangSmith 평가와 테스트</a> · 확인 2026-09-10</li>',
    "08-Batch-평가-입력": '<li><a href="https://developers.openai.com/api/reference/resources/batches">OpenAI Batch API</a> · 확인 2026-09-10</li><li><a href="https://platform.openai.com/docs/guides/batch">OpenAI Batch 안내</a> · 확인 2026-09-10</li>',
}

NOTEBOOK_TEXT = {
    "01-실패-로그와-평가-대상": ["Ch12 검색 설정 36행과 Ch15 제공 답변 읽기", "정답 문서가 1위가 아닌 시험 질문 찾기", "실제 생성 답변의 모델과 프롬프트 버전 확인"],
    "02-4대-RAG-평가자": ["네 평가자의 비교 대상과 정답 답변 필요 여부", "Q002 질문·응답·문서 입력 확인", "교육용 근사값과 실제 근거 충실도 평가 구분"],
    "03-judge-프롬프트와-편향": ["후보 순서를 바꾸는 위치 편향 실험", "평가 모델 사양과 프롬프트 해시 고정", "저장된 실제 평가 모델 버전 확인"],
    "04-제시-라벨과-일치율": ["교육용 작성자 기준과 judge 예시 라벨", "정확 일치율과 혼동 행렬 계산", "불일치 사례와 운영 적용 조건 확인"],
    "05-로컬-트레이싱과-지연": ["RAG 단계별 로컬 실행 추적 준비", "첫 토큰 도착 시간과 전체 지연 계산", "캐시 읽기·생성 사용량 분리"],
    "06-대화당-비용-백분위수": ["대화당 합성 비용 100개 준비", "가장 가까운 순위로 p50·p95·p99 계산", "p99와 p50의 비율 해석"],
    "07-회귀-스위트": ["Before: 평균만 보는 기준의 누락", "After: 사례별 품질·지연·비용 통과 조건", "수정 결과를 같은 기준으로 재검사"],
    "08-Batch-평가-입력": ["세 사례를 Batch JSONL로 변환", "요청 형식과 요청 식별자 검증", "모의 결과의 누락·중복·알 수 없는 ID 검사"],
}

LOOK = {
    "01-실패-로그와-평가-대상": "Ch12 설정 행 36개, 생성 응답 필드 0개, 낮은 검색 순위 사례 2개와 별도 생성 답변 3개를 확인합니다.",
    "02-4대-RAG-평가자": "네 평가자의 비교 대상, Q002의 교육용 근사값 세 개와 실제 근거 충실도 평가 모델 값 하나를 구분합니다.",
    "03-judge-프롬프트와-편향": "후보 순서를 바꿨을 때 승자 ID가 short에서 long으로 바뀌는지와 고정한 평가 모델·프롬프트 버전을 확인합니다.",
    "04-제시-라벨과-일치율": "비교 사례 6개, 일치율 0.833과 TP 3·TN 2·FP 1·FN 0을 확인하고 인간 평가 결과와 구분합니다.",
    "05-로컬-트레이싱과-지연": "하위 실행 네 구간, 첫 토큰 도착 시간 85ms, 전체 지연 301ms와 캐시 읽기·생성 토큰을 확인합니다.",
    "06-대화당-비용-백분위수": "합성 대화 비용 100개의 p50·p95·p99와 p99/p50 비율을 확인합니다.",
    "07-회귀-스위트": "평균만 보는 Before가 Q090을 놓치는지, 사례별 통과 조건을 둔 After가 실패를 검출하는지 확인합니다.",
    "08-Batch-평가-입력": "JSONL 3행의 형식 검사와 모의 결과의 누락·중복·알 수 없는 요청 식별자를 확인합니다.",
}

CONTENT = {
"01-실패-로그와-평가-대상": {
"goals": ["Ch12 검색 로그 36건과 생성 답변 로그를 구분할 수 있습니다.", "실제 검색 순위 문제를 분류하고 생성 평가 대상을 고를 수 있습니다.", "평가하지 않은 결과를 실패로 표시하지 않는 기록 원칙을 적용할 수 있습니다."],
"why": "자동 평가자를 먼저 많이 만들면 실제 시스템에서 나타나지 않은 문제에 시간을 쓰기 쉽습니다. Ch12는 36개의 TF-IDF와 MMR 검색 설정을 비교했습니다. 각 행에는 질문, 후보 문서와 검색 지표가 있지만 생성 답변은 없습니다. 따라서 이 행을 생성 실패 36건으로 세면 사실과 다른 기록이 됩니다. 이 절에서는 검색 결과의 순위가 낮아진 실제 사례를 먼저 찾고, 그 질문에 관련 문서 본문을 전달해 실제 답변을 생성한 뒤에만 생성 평가 대상으로 등록합니다.",
"prior": "Ch11의 <code>evaluation-queries.jsonl</code>은 질문과 정답 문서 ID를 제공합니다. Ch12의 <code>advanced-continuity-experiment-log.jsonl</code> 36행은 개발용 검색 설정 비교이며, <code>advanced-continuity-test-result.json</code>은 선택 설정의 시험 평가입니다. 별도 통합 로그의 Q002 답변만 생성되었고 <code>generation_evaluation.status</code>는 <code>not_evaluated</code>였습니다.",
"concept": "평가 대상 단위는 한 질문의 입력, 검색 문서, 생성 응답, 평가 기준을 묶은 레코드입니다. 검색 실패는 정답 문서가 검색 후보나 평가할 상위 k개 순위에 들어오지 않은 상태이고, 생성 실패는 근거가 전달되었는데도 답이 틀리거나 근거 밖 내용을 추가한 상태입니다. Q006과 Q090은 정답 문서가 2위에 있어 nDCG가 0.6309로 낮아졌지만 Recall@5는 1입니다. 이는 검색 순위 문제이며 생성 실패가 아닙니다.",
"observe": "노트북은 36행의 종류와 생성 응답 필드 부재를 확인합니다. 이어서 선택 설정 시험 결과에서 nDCG가 가장 낮은 Q006과 Q090을 찾습니다. 준비 스크립트는 두 질문과 Q002에 대해 <code>gpt-5.4-mini</code>로 실제 답변을 생성했고, 응답 모델·프롬프트 버전·평가 모델 원문을 <code>evaluation-cases.json</code>에 저장했습니다. 출력에서 검색 사례 수 36, 생성 응답 수 3, 낮은 순위 사례 2를 확인합니다.",
"limits": ["검색 지표가 낮아졌다는 사실만으로 최종 답이 틀렸다고 결론 내리지 않습니다.", "생성 응답을 만들 때 사용한 문서는 Ch12의 공개 학습용 가상 문서입니다. 실제 기관 정책을 뜻하지 않습니다.", "생성 모델과 실행일을 고정했지만 서비스 쪽 모델 스냅샷 변경 가능성은 실행 로그와 함께 확인합니다."],
"next": "다음 절에서는 세 생성 응답에 네 평가자를 적용하고 어떤 평가자에 정답 답변이 필요한지 구분합니다.",
"quiz": [("36개 행을 생성 실패로 세면 안 되는 이유는 무엇인가요?", "행에 생성 답변이 없고 검색 설정과 검색 지표만 있기 때문입니다."), ("Q006의 nDCG@5가 낮고 Recall@5가 1이면 무엇을 알 수 있나요?", "정답 문서는 상위 5개 안에 있지만 첫 순위가 아니어서 순위 품질이 낮아졌음을 알 수 있습니다."), ("생성 평가 레코드에 함께 저장할 항목을 네 가지 적어 보세요.", "질문, 검색 문서, 응답, 모델, 프롬프트 버전, 평가 기준 중 네 가지를 적으면 됩니다.")],
},
"02-4대-RAG-평가자": {
"goals": ["정답 일치도(Correctness)·답변 관련성(Relevance)·근거 충실도(Groundedness)·검색 관련성(Retrieval relevance)의 비교 대상을 설명할 수 있습니다.", "정답 답변이 필요한 평가자와 필요하지 않은 평가자를 구분할 수 있습니다.", "코드 규칙과 평가 모델(LLM judge)의 역할을 함께 설계할 수 있습니다."],
"why": "RAG 답변이 좋다는 한 문장에는 서로 다른 네 질문이 들어 있습니다. 답이 정답과 맞는지, 사용자의 질문에 직접 답하는지, 검색 문서가 답을 뒷받침하는지, 검색 문서 자체가 질문과 관련 있는지를 각각 확인해야 원인을 찾을 수 있습니다. 네 점수를 하나로 합치기 전에 각 점수가 비교하는 두 대상을 확인해야 합니다.",
"prior": "앞 절의 세 레코드에는 질문, 검색된 문서 본문, 실제 응답이 있습니다. Ch11의 <code>gold_doc_ids</code>는 검색 정답 문서 ID입니다. 이것은 정답 답변 문장과 다르므로 Correctness의 reference answer로 그대로 사용할 수 없습니다.",
"concept": "정답 일치도(Correctness)는 응답과 정답 답변을 비교하므로 정답 답변이 필요합니다. 답변 관련성(Relevance)은 응답이 질문을 직접 다루는지 비교합니다. 근거 충실도(Groundedness 또는 faithfulness)는 응답의 주장이 검색 문서로 뒷받침되는지 봅니다. 검색 관련성(Retrieval relevance)은 검색 문서가 질문에 필요한 내용을 담는지 봅니다. 뒤의 세 평가는 정답 답변 없이 수행할 수 있습니다. 코드 평가자는 출처 표기·JSON 형식처럼 명확한 조건에 적합하고, 평가 모델(LLM judge)은 의미가 같은 표현이나 응답의 일부 주장만 문서로 확인되는 경우를 판정할 때 사용합니다.",
"observe": "노트북은 평가자별 입력 필요 여부를 표로 만들고, Q002 응답에 네 평가자를 적용합니다. 제공된 정답 답변은 학습용 작성자 기준이며 사람 검토 라벨이 아닙니다. 코드 평가자는 출처 ID가 응답에 있는지 확인하고, 단어 집합 겹침은 평가 구조를 보여 주는 교육용 근사값으로만 사용합니다. 실제 평가 모델 원문은 준비 단계에서 고정한 <code>groundedness-v1.0.0</code> 결과를 읽습니다.",
"limits": ["Correctness의 reference answer와 검색용 gold document ID를 혼동하지 않습니다.", "단어 겹침 점수는 문장의 의미가 같은지 판정하지 못하므로 운영 품질 점수로 사용하지 않습니다.", "네 평가자 중 하나의 점수만 높아도 전체 답변이 좋다고 결론 내릴 수 없습니다."],
"next": "다음 절에서는 같은 응답도 평가 모델 프롬프트와 후보 순서에 따라 판정이 달라질 수 있는지 확인합니다.",
"quiz": [("정답 답변이 반드시 필요한 평가자는 무엇인가요?", "응답과 정답 답변을 비교하는 Correctness입니다."), ("Groundedness는 무엇과 무엇을 비교하나요?", "생성 응답의 주장과 검색 문서 본문을 비교합니다."), ("출처 ID 형식 확인에는 어떤 평가자가 적합한가요?", "조건이 명확하므로 결정적인 코드 평가자가 적합합니다."), ("gold_doc_ids를 정답 답변으로 쓸 수 없는 이유는 무엇인가요?", "문서 식별자는 정답 문장이 아니며 답의 의미를 담지 않기 때문입니다.")],
},
"03-judge-프롬프트와-편향": {
"goals": ["평가 모델(LLM judge)·프롬프트·온도·버전을 한 평가 실행에 고정할 수 있습니다.", "위치·장황함·자기 선호 편향을 구분할 수 있습니다.", "후보 순서를 바꾼 쌍대 비교로 위치 편향 신호를 확인할 수 있습니다."],
"why": "평가 모델(LLM judge)도 언어 모델이므로 같은 품질을 항상 같은 점수로 판정하지 않습니다. 앞에 놓인 후보, 더 긴 답, 평가 모델과 비슷한 말투를 선호할 수 있습니다. 평가 대상 모델을 고정했더라도 평가 모델 조건이 바뀌면 점수 변화가 애플리케이션 변화인지 평가자 변화인지 구분할 수 없습니다.",
"prior": "앞 절은 네 평가자의 입력을 나누었습니다. 이 절은 의미 판단이 필요한 근거 충실도(Groundedness)를 골라 평가자 자체를 실험합니다. 실행용 모델은 <code>gpt-5.4-mini</code>로 기록하지만 과정의 운영 평가 모델 선택은 <code>[[미정: judge 모델]]</code>로 유지합니다.",
"concept": "평가 모델(LLM judge) 사양에는 모델 이름, 제공자(provider), 온도, 프롬프트 전문 또는 해시, 프롬프트 버전, 출력 스키마, 평가 데이터 지문을 포함합니다. 위치 편향은 먼저 제시된 답을 선호하는 경향이고, 장황함 편향은 더 긴 답을 더 좋게 평가하는 경향입니다. 자기 선호는 평가 모델 계열과 비슷한 표현이나 출력 스타일에 유리한 판정을 내릴 가능성입니다. 후보 A와 B의 순서를 바꾸어 두 번 평가하고 승자가 뒤집히는지 기록하면 위치 민감도를 확인할 수 있습니다.",
"observe": "노트북은 내용이 같은 간결한 답과 불필요한 설명을 붙인 긴 답을 준비합니다. 규칙 기반 쌍대 비교를 A/B와 B/A 순서로 실행해 항상 첫 위치의 후보를 고르는 잘못된 규칙 기반 판정기를 재현합니다. 이어서 저장된 실제 평가 모델 결과의 모델·프롬프트 버전을 확인합니다. 이 로컬 실험은 편향이 발생할 수 있는 구조를 보여 주며 특정 상용 모델의 편향률을 측정한 결과는 아닙니다.",
"limits": ["한 질문의 순서 교환 결과를 평가 모델 전체의 편향률로 일반화하지 않습니다.", "프롬프트 버전은 사람이 읽을 수 있는 이름과 내용 해시를 함께 기록합니다.", "운영 평가 모델은 비용·정확도·사람 라벨 일치율을 확인한 뒤 확정하므로 자리표시자를 유지합니다."],
"next": "다음 절에서는 작성자가 제공한 교육용 라벨과 평가 모델 결과의 일치율을 계산하고 인간 평가와 구분합니다.",
"quiz": [("평가 모델 실행에서 고정할 항목을 네 가지 적어 보세요.", "모델, 온도, 프롬프트 버전, 출력 스키마, 데이터 지문 중 네 가지입니다."), ("위치 편향을 확인하는 방법은 무엇인가요?", "같은 두 후보의 제시 순서를 바꾸어 판정 결과가 유지되는지 확인합니다."), ("더 긴 답이 항상 좋은 답이 아닌 이유는 무엇인가요?", "질문과 관계없는 내용이나 근거 없는 내용을 더 많이 포함할 수 있기 때문입니다.")],
},
"04-제시-라벨과-일치율": {
"goals": ["교육용 제시 라벨과 독립적인 사람 라벨을 구분할 수 있습니다.", "정확 일치율과 혼동 행렬을 계산할 수 있습니다.", "운영 평가 모델(LLM judge) 적용 전에 필요한 사람 검토 절차를 설명할 수 있습니다."],
"why": "평가 모델이 일관되게 점수를 낸다는 사실만으로 사람의 품질 기준과 맞는다고 말할 수 없습니다. 사람이 먼저 기준표를 읽고 독립적으로 라벨을 붙인 자료가 있어야 일치율을 계산할 수 있습니다. 이 교재에는 기존 인간 라벨이 없으므로, 실습 정답은 작성자가 만든 교육용 제시 라벨로 분명히 표시합니다.",
"prior": "앞 절은 평가 모델 조건을 고정하고 순서 교환을 수행했습니다. 이 절은 같은 판정 결과를 이진 라벨로 바꾸어 비교합니다. 저장된 세 평가 모델 결과는 실제 모델 출력이지만 비교 기준은 교육용 작성자 기준입니다.",
"concept": "정확 일치율은 전체 사례 중 두 라벨이 같은 비율입니다. 양성 일치와 음성 일치를 분리하려면 혼동 행렬을 함께 봅니다. 클래스가 한쪽으로 치우치면 높은 일치율이 나타날 수 있습니다. 실제 운영에서는 여러 검토자가 같은 기준표로 일부 사례를 독립 판정하고, 의견 차이를 조정한 뒤 기준을 고칩니다. LangSmith Annotation Queue는 이 과정을 지원하지만 이 실습에는 클라우드 키가 없어 로컬 JSON으로만 구조를 확인합니다.",
"observe": "노트북은 여섯 개의 교육용 제시 라벨과 평가 모델 예시 라벨을 비교합니다. 정확 일치율, TP·TN·FP·FN을 직접 계산합니다. 출력의 0.833은 여섯 사례 중 다섯 사례가 같다는 뜻입니다. 이 값은 작성자 기준과 예시 평가 모델의 일치율이며 인간 평가자와의 일치율로 표시하지 않습니다.",
"limits": ["작성자 기준 라벨을 사람 다수 검토 결과로 설명하지 않습니다.", "사례 여섯 개의 일치율은 운영 임계값을 정하기에 부족합니다.", "운영 적용 전에는 실제 도메인 담당자의 독립 라벨과 정기적인 재측정이 필요합니다."],
"next": "다음 절에서는 품질 점수와 함께 원인을 찾을 수 있도록 로컬 실행 추적에 단계별 시간과 사용량을 남깁니다.",
"quiz": [("이 실습의 라벨을 인간 평가라고 부를 수 없는 이유는 무엇인가요?", "독립적인 도메인 검토자가 판정한 자료가 아니라 작성자가 교육을 위해 제시한 기준이기 때문입니다."), ("일치율과 함께 혼동 행렬을 보는 이유는 무엇인가요?", "어떤 종류의 불일치가 많은지와 클래스 쏠림을 확인하기 위해서입니다."), ("운영 적용 전에 무엇을 추가해야 하나요?", "도메인 검토자의 독립 라벨, 기준 조정, 충분한 사례 수와 주기적인 재평가가 필요합니다.")],
},
"05-로컬-트레이싱과-지연": {
"goals": ["질문 재작성·검색·리랭킹·생성을 하위 실행(child run)으로 기록할 수 있습니다.", "첫 토큰 도착 시간(TTFT)과 전체 지연(total latency)을 분리해 계산할 수 있습니다.", "캐시 읽기(cache read)와 캐시 생성(cache creation) 토큰을 별도 필드로 보존할 수 있습니다."],
"why": "최종 답과 전체 시간만 남기면 어느 단계가 느렸는지, 비용이 어디서 생겼는지 알 수 없습니다. 검색이 늦었는지 생성 첫 토큰이 늦었는지 구분하려면 단계별 시작·종료 시각과 생성의 첫 토큰 시각을 기록해야 합니다. 캐시 사용량도 읽은 토큰과 새로 만든 토큰을 합치면 비용 변화를 설명하기 어렵습니다.",
"prior": "앞 절에서 평가 대상과 평가 모델 결과를 레코드로 묶었습니다. 이제 같은 레코드에 실행 경로를 추가합니다. LangSmith 클라우드 키가 없으므로 기본 실습은 표준 JSON 로컬 실행 추적이며, 클라우드 업로드는 선택 확장으로만 안내합니다.",
"concept": "실행 추적(trace)은 한 요청의 전체 실행 기록이고 하위 실행(child run)은 그 안의 단계별 기록입니다. 첫 토큰 도착 시간(TTFT, time to first token)은 생성 시작부터 첫 토큰 도착까지의 시간입니다. 전체 지연(total latency)은 요청 시작부터 최종 응답 종료까지의 시간입니다. 스트리밍하지 않은 호출에는 첫 토큰 이벤트가 없으므로 TTFT를 추정해 넣지 않고 <code>null</code>로 남깁니다. 사용량은 input·output·cache_read·cache_creation 토큰을 구분합니다.",
"observe": "노트북은 재작성 12ms, 검색 31ms, 리랭킹 18ms, 생성 240ms인 로컬 실행 추적을 만듭니다. 생성 시작 후 85ms에 첫 토큰이 도착하도록 기록하고 첫 토큰 도착 시간 85ms, 전체 지연 301ms를 계산합니다. 캐시 읽기 420개의 토큰과 캐시 생성 80개의 토큰도 분리합니다. 이 숫자는 계측 구조를 학습하기 위한 고정 실습값이며 실제 API 실행 추적으로 가장하지 않습니다.",
"limits": ["TTFT는 스트리밍의 첫 토큰 이벤트가 있을 때만 계산합니다.", "서버 처리 시간과 네트워크 왕복 시간이 함께 포함될 수 있으므로 측정 위치를 기록합니다.", "LangSmith 클라우드에서는 비밀 키나 개인정보를 trace 입력에 넣지 않도록 전송 전 마스킹 정책을 적용합니다."],
"next": "다음 절에서는 여러 실행 추적을 대화 단위로 묶고 비용의 p50·p95·p99를 계산합니다.",
"quiz": [("첫 토큰 도착 시간과 전체 지연의 시작점과 끝점을 설명해 보세요.", "첫 토큰 도착 시간은 생성 시작부터 첫 토큰까지이고, 전체 지연은 요청 시작부터 최종 응답 종료까지입니다."), ("첫 토큰 이벤트가 없을 때 어떻게 기록하나요?", "추정하지 않고 TTFT를 null로 기록합니다."), ("캐시 사용량을 두 필드로 나누는 이유는 무엇인가요?", "기존 캐시를 읽은 양과 새 캐시를 만든 양의 비용과 동작이 다르기 때문입니다."), ("하위 실행으로 남길 RAG 단계 네 가지는 무엇인가요?", "질문 재작성, 검색, 리랭킹, 생성입니다.")],
},
"06-대화당-비용-백분위수": {
"goals": ["여러 모델 호출을 대화 ID로 묶어 비용을 합산할 수 있습니다.", "대화당 비용의 p50·p95·p99를 계산할 수 있습니다.", "평균만으로 드러나지 않는 긴 꼬리 비용을 설명할 수 있습니다."],
"why": "한 번의 호출 비용은 낮아도 한 대화에서 재작성·검색 보조·답변 생성·평가 모델이 여러 번 실행되면 한 대화에 드는 총비용은 커집니다. 일부 긴 대화가 대부분의 비용을 차지할 때 평균만 보면 예산 상한을 정하기 어렵습니다. 대화 ID로 먼저 합산하고 백분위수를 봐야 일반적인 사용자와 비용이 큰 사용자를 함께 이해할 수 있습니다.",
"prior": "앞 절의 실행 추적에는 단계와 토큰이 있습니다. 각 하위 실행에 <code>conversation_id</code>와 비용을 추가하면 여러 호출을 한 대화로 묶을 수 있습니다. 가격표가 바뀔 수 있으므로 이 실습은 고정된 교육용 비용 원자료를 사용합니다.",
"concept": "p50은 정렬한 값의 가운데 수준, p95는 약 95%의 대화가 그 값 이하에 놓이는 경계, p99는 약 99%가 그 값 이하인 경계입니다. 표본이 작으면 보간 방법에 따라 값이 달라지므로 계산 방식을 기록합니다. 이 노트북은 가장 가까운 순위 방식으로 계산합니다. 주요 관리 지표는 대화당 총비용이며 호출당 비용은 원인 분석용 보조 지표입니다.",
"observe": "노트북은 100개 대화의 고정 비용을 생성합니다. 대부분은 0.002~0.008달러이고 마지막 다섯 대화는 0.02~0.12달러입니다. 가장 가까운 순위로 p50, p95, p99를 계산하면 긴 꼬리의 영향이 p95와 p99에서 나타납니다. 평균과 p50의 차이도 함께 출력해 평균만 보고한 경우의 한계를 확인합니다.",
"limits": ["교육용 비용은 실제 OpenAI 청구액이 아니며 모델별 최신 단가와 사용량으로 다시 계산해야 합니다.", "서로 다른 기간이나 제품군의 백분위수를 한 집합에 섞지 않습니다.", "p99는 표본 수가 적을수록 불안정하므로 표본 수와 계산법을 함께 기록합니다."],
"next": "다음 절에서는 품질·지연·비용 기준을 회귀 스위트의 통과 조건으로 바꿉니다.",
"quiz": [("호출당 비용보다 대화당 비용을 우선하는 이유는 무엇인가요?", "사용자 한 대화가 여러 호출을 만들므로 실제 서비스 비용 단위가 대화이기 때문입니다."), ("평균과 p99가 크게 다른 경우 무엇을 확인하나요?", "일부 긴 대화나 재시도, 과도한 도구 호출이 긴 꼬리 비용을 만드는지 확인합니다."), ("백분위수와 함께 기록할 항목은 무엇인가요?", "표본 수, 기간, 제품군, 계산 방법을 기록합니다.")],
},
"07-회귀-스위트": {
"goals": ["과거 성공 사례를 고정된 회귀 데이터로 만들 수 있습니다.", "새 버전의 품질·지연·비용을 기준선과 비교할 수 있습니다.", "점수 평균이 좋아도 핵심 사례가 깨지면 배포를 막을 수 있습니다."],
"why": "프롬프트를 고친 뒤 평균 점수가 올라도 과거에 잘 답하던 중요한 질문이 틀릴 수 있습니다. 회귀 스위트는 이미 확인한 성공 사례와 실패 후 수정한 사례를 다시 실행해 품질 저하를 배포 전에 발견합니다. 통과 조건은 배포 전에 자동으로 판정할 수 있을 만큼 구체적으로 적어야 합니다.",
"prior": "앞 절까지 생성 품질, 첫 토큰 도착 시간(TTFT)·전체 지연(total), 대화당 비용을 각각 측정했습니다. 이 절은 이 지표를 하나의 배포 기준에 연결합니다. Q002·Q006·Q090은 실제 생성 답변이 저장된 회귀 후보입니다.",
"concept": "회귀 사례에는 입력, 기대 행동, 최소 점수, 최대 지연·비용, 모델과 프롬프트 버전을 둡니다. 기준선은 비교의 출발점이고 통과 조건(gate)은 반드시 지켜야 하는 기준입니다. 평균 지표와 핵심 사례별 조건을 함께 사용합니다. 원문이나 기준을 바꾸면 데이터셋 버전을 올리고 과거 결과와 같은 시험이라고 부르지 않습니다.",
"observe": "Before 예제는 평균 근거 충실도(Groundedness)만 확인해 핵심 Q090의 실패를 놓칩니다. After 예제는 모든 핵심 사례 점수, p95 전체 지연(total), p99 대화 비용을 각각 검사합니다. 처음 실행은 Q090 점수 0 때문에 실패하고, 수정된 결과는 세 조건을 모두 통과합니다. 이 비교는 모델의 실제 오류 재현이 아니라 평균만 확인하는 기준이 핵심 사례 실패를 놓치는 과정을 보여 주는 교육용 입력입니다.",
"limits": ["평균 점수만으로 핵심 사례 통과를 대신하지 않습니다.", "임계값을 현재 결과에 맞추어 매번 낮추면 회귀 스위트가 보호 기능을 잃습니다.", "평가 모델 버전이나 데이터셋이 바뀌면 기준선을 다시 측정하고 변경 이유를 기록합니다."],
"next": "마지막 절에서는 같은 회귀 평가 요청을 Batch API용 JSONL로 만들고 제출 전 검증합니다.",
"quiz": [("평균이 올라도 배포를 막아야 하는 경우는 언제인가요?", "법적·안전·핵심 업무 질문 같은 필수 사례가 통과하지 못한 경우입니다."), ("회귀 사례에 포함할 항목을 네 가지 적어 보세요.", "입력, 기대 행동, 점수 기준, 지연·비용 상한, 모델·프롬프트·데이터셋 버전 중 네 가지입니다."), ("평가 모델이 바뀌었을 때 기준선을 다시 측정하는 이유는 무엇인가요?", "점수 변화가 애플리케이션이 아니라 평가자 변화에서 생길 수 있기 때문입니다.")],
},
"08-Batch-평가-입력": {
"goals": ["평가 요청을 OpenAI Batch API 입력 JSONL로 만들 수 있습니다.", "요청 식별자(custom_id) 중복·엔드포인트(endpoint)·요청 본문을 제출 전에 검증할 수 있습니다.", "Batch 완료·할인과 로컬 입력 검증의 확인 범위를 구분할 수 있습니다."],
"why": "회귀 스위트가 커지면 평가 요청을 한 건씩 기다리는 방식은 느리고 비용 관리도 어렵습니다. OpenAI Batch API는 비동기 작업을 24시간 완료 창으로 처리하며 공식 문서는 50% 할인을 안내합니다. 다만 제출과 완료 확인에는 시간이 걸리므로 수업 기본 경로는 JSONL 생성과 정적 검증까지 수행합니다.",
"prior": "앞 절의 회귀 사례에는 질문, 응답과 평가 모델 기준이 있습니다. Batch 한 행은 요청 식별자(<code>custom_id</code>), HTTP 메서드(method), 엔드포인트(endpoint), 요청 본문(body)을 포함합니다. 이 절은 <code>/v1/responses</code>용 요청을 만듭니다.",
"concept": "JSONL은 한 줄에 하나의 JSON 객체를 저장하는 형식입니다. 각 Batch 요청의 <code>custom_id</code>는 결과를 원래 사례와 연결하는 요청 식별자이며 파일 안에서 중복되면 안 됩니다. 메서드(method)는 POST, <code>url</code>은 선택한 엔드포인트(endpoint), 요청 본문(body)에는 모델과 입력을 둡니다. 업로드할 때 purpose는 batch이고 현재 완료 기한(completion window)은 24h입니다.",
"observe": "노트북은 세 평가 사례를 <code>batch-eval-input.jsonl</code>로 만듭니다. 각 줄을 다시 읽어 JSON 구문, custom_id 유일성, POST, <code>/v1/responses</code>, 모델과 입력 존재를 검증합니다. 실제 파일 업로드·Batch 생성·완료 대기·청구 할인 확인은 수행하지 않습니다. 따라서 출력은 입력 파일이 유효하다는 증거이며 Batch가 완료되었다는 증거가 아닙니다.",
"limits": ["Batch는 실시간 사용자 응답 경로에 사용하지 않고 오프라인 평가에 사용합니다.", "공식 50% 할인 정책과 실제 계정 청구액 확인은 구분합니다.", "입력 파일에 API 키나 개인정보를 넣지 않으며 업로드 전 별도 검사를 수행합니다."],
"next": "Ch16에서는 이 회귀 결과와 실행 추적을 사용해 입력 검증, 비용 상한, 재시도와 감사 로그를 직접 구현합니다.",
"quiz": [("요청 식별자(custom_id)가 필요한 이유는 무엇인가요?", "비동기 결과를 원래 평가 사례와 연결하기 위해서입니다."), ("이 실습에서 실제 Batch 완료를 확인했다고 말할 수 있나요?", "아닙니다. JSONL 생성과 제출 전 검증까지만 수행했습니다."), ("Batch를 실시간 응답에 쓰기 어려운 이유는 무엇인가요?", "비동기 처리이며 완료 기한이 24시간이어서 즉시 응답이 필요한 경로와 맞지 않기 때문입니다."), ("입력 검증 항목을 세 가지 적어 보세요.", "JSON 구문, 요청 식별자 유일성, 메서드·엔드포인트, 모델·입력 존재 중 세 가지입니다.")],
},
}


NOTEBOOK_CODE = {
"01-실패-로그와-평가-대상": [
"""from pathlib import Path\nimport json\nroot = next(p for p in [Path.cwd(), *Path.cwd().parents]\n            if (p / 'labs/part3/ch12-retrieval-tuning').is_dir())\nch12 = root / 'labs/part3/ch12-retrieval-tuning/runs'\nrows = [json.loads(x) for x in (ch12 / 'advanced-continuity-experiment-log.jsonl').read_text().splitlines()]\ncases = json.loads((root / 'labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json').read_text())\nprint('검색 설정 행:', len(rows))\nprint('36행의 생성 응답 필드:', sum('response' in row for row in rows))\nprint('새로 생성한 답변:', len(cases['cases']))""",
"""test = json.loads((ch12 / 'advanced-continuity-test-result.json').read_text())\nlow = [r for r in test['results'] if r['ndcg_at_5'] < 1]\nfor row in low:\n    first = row['top_results'][0]['doc_id']\n    print(row['qid'], '첫 문서=', first, 'gold=', row['gold_doc_ids'],\n          'Recall@5=', row['recall_at_5'], 'nDCG@5=', round(row['ndcg_at_5'], 4))""",
"""for case in cases['cases']:\n    print(case['qid'], case['answer_model'], case['answer_prompt_version'])\n    print(case['response'][:100])\nassert len(rows) == 36 and len(low) == 2\nassert all('response' in case for case in cases['cases'])"""],
"02-4대-RAG-평가자": [
"""evaluators = {\n 'Correctness': ('응답', '정답 답변', True),\n 'Relevance': ('응답', '질문', False),\n 'Groundedness': ('응답', '검색 문서', False),\n 'Retrieval relevance': ('검색 문서', '질문', False),\n}\nfor name, (left, right, reference) in evaluators.items():\n    print(f'{name:20} {left} vs {right} | reference={reference}')""",
"""from pathlib import Path\nimport json, re\nroot = next(p for p in [Path.cwd(), *Path.cwd().parents]\n            if (p / 'labs/part4/ch15-evaluation-advanced').is_dir())\ndata = json.loads((root / 'labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json').read_text())\ncase = next(x for x in data['cases'] if x['qid'] == 'Q002')\ndef words(text: str) -> set[str]:\n    return set(re.findall(r'[가-힣A-Za-z0-9]+', text))\nprint('질문-응답 겹침:', round(len(words(case['question']) & words(case['response'])) / len(words(case['question'])), 3))\nprint('출처 표기:', all(doc in case['response'] for doc in case['retrieved_doc_ids']))""",
"""verdict = json.loads(case['judge_raw'])\ncorrectness = len(words(case['reference_answer']) & words(case['response'])) / len(words(case['reference_answer']))\nrelevance = len(words(case['question']) & words(case['response'])) / len(words(case['question']))\nretrieval = len(words(case['question']) & words(case['context'])) / len(words(case['question']))\nscores = {'Correctness 교육용 근사': round(correctness, 3),\n          'Relevance 교육용 근사': round(relevance, 3),\n          'Groundedness 실제 judge': verdict['score'],\n          'Retrieval relevance 교육용 근사': round(retrieval, 3)}\nfor name, score in scores.items():\n    print(name, score)\nprint(case['reference_kind'], case['judge_model'], case['judge_prompt_version'])\nassert case['judge_prompt_version'] == 'groundedness-v1.0.0'"""],
"03-judge-프롬프트와-편향": [
"""short = ('short', '도서는 7권까지 14일 동안 빌릴 수 있습니다. [E01]')\nlong = ('long', short[1] + ' 도서관은 시민을 위한 지식 공간입니다.')\ndef biased_pairwise(first: tuple[str, str], second: tuple[str, str]) -> str:\n    return first[0]  # 잘못된 평가자: 내용 대신 첫 후보 ID를 선택\nwinner_ab = biased_pairwise(short, long)\nwinner_ba = biased_pairwise(long, short)\nprint('short/long 승자:', winner_ab)\nprint('long/short 승자:', winner_ba)\nprint('순서를 바꿔도 같은 후보인가:', winner_ab == winner_ba)""",
"""import hashlib\njudge_prompt = '근거로 뒷받침되면 1, 아니면 0. JSON만 출력.'\nspec = {\n 'model': 'gpt-5.4-mini', 'temperature': 0,\n 'prompt_version': 'groundedness-v1.0.0',\n 'prompt_sha256': hashlib.sha256(judge_prompt.encode()).hexdigest(),\n 'output_schema': {'score': '0|1', 'reason': 'string'},\n}\nprint(spec)""",
"""from pathlib import Path\nimport json\nroot = next(p for p in [Path.cwd(), *Path.cwd().parents]\n            if (p / 'labs/part4/ch15-evaluation-advanced').is_dir())\ndata = json.loads((root / 'labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json').read_text())\nfor case in data['cases']:\n    print(case['qid'], case['judge_model'], case['judge_prompt_version'])\nassert all(x['judge_placeholder'] == '[[미정: judge 모델]]' for x in data['cases'])"""],
"04-제시-라벨과-일치율": [
"""labels = [\n ('C01', 1, 1), ('C02', 1, 1), ('C03', 0, 0),\n ('C04', 0, 1), ('C05', 1, 1), ('C06', 0, 0),\n]\nprint('라벨 출처: 교육용 작성자 기준(인간 평가 아님)')\nprint('사례 수:', len(labels))""",
"""agree = sum(gold == judge for _, gold, judge in labels) / len(labels)\ntp = sum(g == j == 1 for _, g, j in labels)\ntn = sum(g == j == 0 for _, g, j in labels)\nfp = sum(g == 0 and j == 1 for _, g, j in labels)\nfn = sum(g == 1 and j == 0 for _, g, j in labels)\nprint('정확 일치율:', round(agree, 3))\nprint({'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn})""",
"""for case_id, author, judge in labels:\n    mark = '일치' if author == judge else '불일치'\n    print(case_id, author, judge, mark)\nassert round(agree, 3) == 0.833\nprint('운영 적용: 독립적인 도메인 검토자 라벨 필요')"""],
"05-로컬-트레이싱과-지연": [
"""trace = {\n 'trace_id': 'local-trace-001', 'conversation_id': 'conv-001',\n 'started_ms': 0, 'first_token_ms': 146, 'ended_ms': 301,\n 'children': [\n  {'name': 'rewrite', 'start': 0, 'end': 12},\n  {'name': 'retrieve', 'start': 12, 'end': 43},\n  {'name': 'rerank', 'start': 43, 'end': 61},\n  {'name': 'generate', 'start': 61, 'end': 301},\n ],\n}""",
"""generate = next(x for x in trace['children'] if x['name'] == 'generate')\nttft = trace['first_token_ms'] - generate['start']\ntotal = trace['ended_ms'] - trace['started_ms']\nprint('TTFT(ms):', ttft)\nprint('total(ms):', total)\nfor run in trace['children']:\n    print(run['name'], run['end'] - run['start'])""",
"""usage = {\n 'input_tokens': 1200, 'output_tokens': 180,\n 'cache_read_tokens': 420, 'cache_creation_tokens': 80,\n}\ntrace['usage'] = usage\nprint(usage)\nassert ttft == 85 and total == 301\nprint('cloud 업로드: 미실행(LangSmith API 키 없음)')"""],
"06-대화당-비용-백분위수": [
"""costs = [0.002 + (i % 7) * 0.001 for i in range(95)]\ncosts += [0.020, 0.035, 0.050, 0.080, 0.120]\nprint('대화 수:', len(costs))\nprint('총비용(교육용 달러):', round(sum(costs), 3))""",
"""import math, statistics\ndef nearest_rank(values: list[float], percentile: int) -> float:\n    ordered = sorted(values)\n    rank = max(1, math.ceil(percentile / 100 * len(ordered)))\n    return ordered[rank - 1]\nfor p in (50, 95, 99):\n    print(f'p{p}:', f'${nearest_rank(costs, p):.3f}')\nprint('평균:', f'${statistics.mean(costs):.3f}')""",
"""p50 = nearest_rank(costs, 50)\np99 = nearest_rank(costs, 99)\nprint('p99/p50:', round(p99 / p50, 1))\nassert p99 > p50 * 10\nprint('해석: 일부 대화의 긴 꼬리 비용을 별도로 조사합니다.')"""],
"07-회귀-스위트": [
"""baseline = {'Q002': 1, 'Q006': 1, 'Q090': 1}\ncurrent = {'Q002': 1, 'Q006': 1, 'Q090': 0}\naverage_pass = sum(current.values()) / len(current) >= 0.66\nprint('Before 평균 기준 통과:', average_pass)\nprint('놓친 핵심 실패:', [qid for qid in baseline if current[qid] < baseline[qid]])""",
"""limits = {'p95_total_ms': 1500, 'p99_cost_usd': 0.08}\nobserved = {'p95_total_ms': 980, 'p99_cost_usd': 0.06}\ndef gate(scores: dict[str, int]) -> bool:\n    quality = all(scores[qid] >= baseline[qid] for qid in baseline)\n    latency = observed['p95_total_ms'] <= limits['p95_total_ms']\n    cost = observed['p99_cost_usd'] <= limits['p99_cost_usd']\n    return quality and latency and cost\nprint('After 사례별 기준 통과:', gate(current))""",
"""fixed = {'Q002': 1, 'Q006': 1, 'Q090': 1}\nprint('수정 결과 통과:', gate(fixed))\nassert not gate(current)\nassert gate(fixed)\nprint('회귀 데이터셋 버전: rag-regression-v1.0.0')"""],
"08-Batch-평가-입력": [
"""from pathlib import Path\nimport json\nroot = next(p for p in [Path.cwd(), *Path.cwd().parents]\n            if (p / 'labs/part4/ch15-evaluation-advanced').is_dir())\ndata = json.loads((root / 'labs/part4/ch15-evaluation-advanced/data/evaluation-cases.json').read_text())\nout = root / 'labs/part4/ch15-evaluation-advanced/runs/batch-eval-input.jsonl'\nrows = []\nfor case in data['cases']:\n    rows.append({'custom_id': f"judge-{case['qid']}", 'method': 'POST',\n      'url': '/v1/responses', 'body': {'model': 'gpt-5.4-mini',\n      'input': f"질문: {case['question']}\\n응답: {case['response']}"}})\nout.parent.mkdir(exist_ok=True)\nout.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\\n' for x in rows))\nprint('저장:', out.name, '행:', len(rows))""",
"""loaded = [json.loads(line) for line in out.read_text().splitlines()]\nids = [row['custom_id'] for row in loaded]\nchecks = {\n 'json_rows': len(loaded) == len(rows),\n 'unique_custom_id': len(ids) == len(set(ids)),\n 'post_only': all(x['method'] == 'POST' for x in loaded),\n 'responses_endpoint': all(x['url'] == '/v1/responses' for x in loaded),\n 'body_fields': all(x['body'].get('model') and x['body'].get('input') for x in loaded),\n}\nprint(checks)\nassert all(checks.values())""",
"""mock_results = [\n {'custom_id': ids[0]}, {'custom_id': ids[1]},\n {'custom_id': ids[1]}, {'custom_id': 'judge-UNKNOWN'},\n]\nresult_ids = [row['custom_id'] for row in mock_results]\nmissing = sorted(set(ids) - set(result_ids))\nunknown = sorted(set(result_ids) - set(ids))\nduplicates = sorted({value for value in result_ids if result_ids.count(value) > 1})\nprint({'누락': missing, '알 수 없는 ID': unknown, '중복': duplicates})\nprint('실제 업로드·완료·할인 청구: 미확인')\nassert missing and unknown and duplicates"""],
}


def markdown(text: str, lesson_part: str | None = None) -> dict:
    meta = {} if lesson_part is None else {"lesson_part": lesson_part}
    return {"cell_type": "markdown", "id": "", "metadata": meta, "source": text.splitlines(keepends=True)}


COMMENTS = {
    "01-실패-로그와-평가-대상": ["프로젝트 루트를 찾아 Ch12 검색 설정 36행과 Ch15 제공 답변 기록을 읽습니다.", "시험 결과에서 정답 문서가 1위가 아닌 검색 순위 사례만 고릅니다.", "준비 단계에서 실제 생성해 저장한 답변의 모델과 프롬프트 버전을 확인합니다."],
    "02-4대-RAG-평가자": ["평가자마다 비교하는 두 대상과 정답 답변 필요 여부를 표로 정리합니다.", "Q002의 질문·응답 단어와 출처 ID를 사용해 코드 평가 구조를 확인합니다.", "실제 judge 출력과 고정한 실행 모델·프롬프트 버전을 읽습니다."],
    "03-judge-프롬프트와-편향": ["첫 후보만 고르는 잘못된 판정기로 위치 편향이 생기는 구조를 재현합니다.", "judge 모델·온도·프롬프트 해시·출력 형식을 하나의 사양으로 묶습니다.", "세 사례의 실제 judge 기록과 운영 모델 미정 상태를 확인합니다."],
    "04-제시-라벨과-일치율": ["작성자 기준과 judge 예시 라벨 여섯 쌍을 교육용 입력으로 준비합니다.", "전체 여섯 사례를 분모로 정확 일치율과 혼동 행렬을 계산합니다.", "사례별 일치 여부를 출력하고 운영에는 독립 검토가 필요함을 표시합니다."],
    "05-로컬-트레이싱과-지연": ["한 대화의 재작성·검색·리랭킹·생성 구간을 밀리초 단위로 기록합니다.", "생성 시작 시각을 기준으로 TTFT를, 요청 시작을 기준으로 total을 계산합니다.", "입출력 토큰과 캐시 read·creation 토큰을 서로 다른 필드로 보존합니다."],
    "06-대화당-비용-백분위수": ["대부분 낮고 일부 높은 대화당 교육용 비용 100개를 준비합니다.", "정렬한 비용에서 가장 가까운 순위 방식으로 p50·p95·p99를 계산합니다.", "p99와 p50의 비율로 긴 꼬리 비용이 존재하는지 확인합니다."],
    "07-회귀-스위트": ["평균 기준만 사용했을 때 Q090의 핵심 실패를 놓치는지 확인합니다.", "사례별 품질과 지연·비용 상한을 모두 검사하는 gate 함수를 정의합니다.", "Q090을 수정한 결과가 같은 고정 기준을 통과하는지 검사합니다."],
    "08-Batch-평가-입력": ["세 평가 사례를 Responses endpoint용 Batch JSONL 행으로 변환해 저장합니다.", "각 JSONL 행의 식별자·method·endpoint·body 필드를 제출 전에 검사합니다.", "로컬에서 실행한 범위와 실제 업로드·완료·청구 미확인 범위를 구분합니다."],
}


def code(text: str, lesson_part: str | None = None, comment: str | None = None) -> dict:
    meta = {} if lesson_part is None else {"lesson_part": lesson_part}
    source = ((f"# {comment}\n" if comment else "") + text)
    return {"cell_type": "code", "execution_count": None, "id": "", "metadata": meta, "outputs": [], "source": source.splitlines(keepends=True)}


def notebook(title: str, slug: str, fmt: str) -> dict:
    blocks = NOTEBOOK_CODE[slug]
    comments = COMMENTS[slug]
    labels = NOTEBOOK_TEXT[slug]
    install = "# 실습 환경에서 사용하는 보조 패키지 버전을 고정합니다.\n%pip install -q python-dotenv==1.2.3"
    intro = f"# {title}\n\nPython 3.12 새 커널에서 {labels[0]}부터 확인합니다."
    cells = [markdown(intro), markdown("## Python 3.12 패키지 버전 고정"), code(install), markdown(f"## {labels[0]}"), code(blocks[0], comment=comments[0])]
    if fmt == "paired":
        cells += [markdown(f"## {labels[1]}", "before"), code(blocks[1], "before", comments[1]), markdown(f"## {labels[2]}", "after"), code(blocks[2], "after", comments[2])]
    else:
        cells += [markdown(f"## {labels[1]}"), code(blocks[1], comment=comments[1]), markdown(f"## {labels[2]}"), code(blocks[2], comment=comments[2])]
    for i, cell in enumerate(cells, 1):
        cell["id"] = f"cell-{i:02d}"
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.12"}, "lesson_format": fmt}, "nbformat": 4, "nbformat_minor": 5}


def quiz_html(items):
    return "".join(f'<details class="quiz"><summary>{i}. 복습</summary><p class="quiz-q">{q}</p><p class="quiz-a">{a} <b>오답 시 다시 볼 곳:</b> 핵심 개념과 실행 예제</p></details>' for i, (q, a) in enumerate(items, 1))


def source(slug: str, title: str, fmt: str) -> str:
    c = CONTENT[slug]
    goals = "".join(f"<li>{x}</li>" for x in c["goals"])
    limits = "".join(f"<li>{x}</li>" for x in c["limits"])
    token = f"{{{{notebook:{slug}}}}}" if fmt == "experiment" else f"{{{{notebook:{slug}|example}}}}"
    heading = "실험 결과 해석" if fmt == "experiment" else "일부러 실패해 보기"
    failure = "" if fmt == "experiment" else f"{{{{notebook:{slug}|failure}}}}"
    summary = "".join(f"<li>{item}</li>" for item in SUMMARIES[slug])
    return f'''<!--meta: 강의 1h | 실습 1h | 코드 Jupyter Notebook | 새 용어 4 -->
<h2 id="b1"><span class="no">1</span>학습 목표</h2><div class="goal"><ul>{goals}</ul></div>
<h2 id="b2"><span class="no">2</span>이 내용을 배우는 이유</h2><p>{c['why']}</p>
<h2 id="b3"><span class="no">3</span>앞에서 배운 내용</h2><p>{c['prior']}</p>
<h2 id="b4"><span class="no">4</span>핵심 개념</h2><h3>쉬운 예</h3><p>{ANALOGY[slug]}</p><h3>정의</h3><p>{c['concept']}</p><h3>도식 읽기</h3>{{{{svg:{slug[:2]}-평가-흐름}}}}<p>{FIGURE_READ[slug]}</p>
<h2 id="b5"><span class="no">5</span>실행 예제</h2><p>{c['observe']}</p>{token}<p class="look"><b>확인할 점</b> — {LOOK[slug]}</p>
<h2 id="b6"><span class="no">6</span>{heading}</h2>{failure}<p>{RESULTS[slug]}</p>
<h2 id="b7"><span class="no">7</span>주의할 점과 실무 메모</h2><ul>{limits}</ul>
<h2 id="b8"><span class="no">8</span>정리와 다음 절</h2><ul>{summary}</ul><p><strong>다음 학습과 이어지는 지점</strong> — {c['next']}</p>
<h2 id="b9"><span class="no">9</span>복습 문제</h2>{quiz_html(c['quiz'])}
<h2 id="b10"><span class="no">10</span>참고 자료</h2><ul>{REFERENCES[slug]}</ul>
'''


def figure(slug: str, title: str) -> tuple[str, dict]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" role="img" aria-labelledby="title desc"><title id="title">{title} 평가 흐름</title><desc id="desc">입력, 실행, 측정, 확인 경계를 왼쪽에서 오른쪽으로 보여 줍니다.</desc><rect width="900" height="260" rx="24" fill="#f8fafc"/><g font-family="Arial, sans-serif" font-size="18" text-anchor="middle"><rect x="45" y="85" width="160" height="90" rx="16" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/><text x="125" y="137">입력·버전</text><rect x="265" y="85" width="160" height="90" rx="16" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/><text x="345" y="137">실행 기록</text><rect x="485" y="85" width="160" height="90" rx="16" fill="#fef3c7" stroke="#d97706" stroke-width="3"/><text x="565" y="137">측정값</text><rect x="705" y="85" width="150" height="90" rx="16" fill="#fee2e2" stroke="#dc2626" stroke-width="3"/><text x="780" y="127">확인 필요</text><text x="780" y="151">경계</text><path d="M205 130H265M425 130H485M645 130H705" stroke="#475569" stroke-width="4" marker-end="url(#a)"/><defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#475569"/></marker></defs></g></svg>'''
    drawing = {"type": "excalidraw", "version": 2, "source": "ch15-author", "elements": [{"id": f"{slug}-1", "type": "rectangle", "x": 45, "y": 85, "width": 160, "height": 90}, {"id": f"{slug}-2", "type": "rectangle", "x": 265, "y": 85, "width": 160, "height": 90}, {"id": f"{slug}-3", "type": "rectangle", "x": 485, "y": 85, "width": 160, "height": 90}, {"id": f"{slug}-4", "type": "rectangle", "x": 705, "y": 85, "width": 150, "height": 90}], "appState": {"viewBackgroundColor": "#f8fafc"}, "files": {}}
    return svg, drawing


def main() -> None:
    config = {"part": 4, "part_title": "Part 4 · 그래프 · 평가 · 안정화", "chapter": "ch15-evaluation-advanced", "title": "평가 심화 — judge · 트레이싱 · 회귀", "hours": "총 16h · 강의 8h · 실습 8h", "objectives": ["실제 RAG 실패에서 필요한 평가자만 선택할 수 있습니다.", "평가 모델 편향과 사람 라벨 일치율을 구분해 기록할 수 있습니다.", "실행 추적의 첫 토큰 도착 시간·전체 지연·캐시 사용량과 대화당 비용 백분위수를 계산할 수 있습니다.", "회귀 스위트와 Batch 입력으로 반복 평가를 준비할 수 있습니다."], "lab_path": "labs/part4/ch15-evaluation-advanced", "sections": [{"slug": s, "title": t, "format": f} for s, t, f in SECTIONS]}
    (HERE / "chapter.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    for slug, title, fmt in SECTIONS:
        (HERE / "_src" / f"{slug}.html").write_text(source(slug, title, fmt))
        (LAB / "notebooks" / f"{slug}.ipynb").write_text(json.dumps(notebook(title, slug, fmt), ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
