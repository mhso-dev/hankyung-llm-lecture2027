from __future__ import annotations

# 사용 중지(2026-09-17, Ch07 01절 품질 개선 시작, 규격 §8·PLAYBOOK §2-1): 실행하면 개선본 노트북을 개선 전 셀로 덮어씁니다.
# 품질 개선본은 textbook/part2/ch07-prompt-engineering/qa/upgrade/author_NN.py(노트북)와 textbook/_notebook/upgrade/mdpatch.py(설명 수정)로 고칩니다.
# 챕터 마감 때 textbook/part2/ch07-prompt-engineering/qa/upgrade/before/generators/로 옮깁니다(삭제 아님).
raise SystemExit("사용 중지: 개선 전 생성기입니다. textbook/part2/ch07-prompt-engineering/qa/upgrade/author_NN.py를 쓰세요.")

import json
from pathlib import Path

ROOT = Path(__file__).parent
NOTEBOOKS = ROOT / "notebooks"

INSTALL = "%pip install -q langchain==1.4.0 langchain-openai==1.6.0 python-dotenv==1.2.3"

ENV_MODEL = '''import json, os, time
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model

env_path = find_dotenv(usecwd=True)
if env_path:
    load_dotenv(env_path)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("프로젝트 루트의 .env에 OPENAI_API_KEY가 필요합니다.")
model = init_chat_model("openai:gpt-5.4-mini", max_tokens=220)'''

TASK_INPUT = '''TASK = """고객 문의: 어제 받은 텀블러 뚜껑이 깨졌습니다. 주문번호는 A-1042입니다.
새 상품으로 바꾸고 싶습니다. 회사 규정상 교환 접수에는 파손 사진이 필요합니다.
답변에는 분류, 필요한 다음 행동, 고객에게 보낼 한 문장을 포함하세요."""
MENTIONS = ["교환", "A-1042", "사진"]'''

HELPERS = '''# 모델 응답의 원문, 사용량, 경과 시간을 한 레코드로 보존합니다.
def run(messages):
    started = time.perf_counter()
    answer = model.invoke(messages)
    return {"text": answer.text, "usage": answer.usage_metadata,
            "latency_s": round(time.perf_counter() - started, 3)}

def mention_flags(text):
    return {word: word in text for word in MENTIONS}'''


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text: str) -> dict:
    notes = [
        ("%pip", "현재 커널에 수업 기준 패키지 버전을 설치합니다."),
        ("from dotenv", "find_dotenv는 실행 폴더부터 상위 폴더의 .env를 찾고 키 값은 출력하지 않습니다."),
        ("TASK =", "TASK는 모든 비교에서 바꾸지 않는 합성 문의이고 MENTIONS는 품질 점수가 아닙니다."),
        ("role_text =", "역할 문구와 제약 문구를 분리해 두 조건에 같은 글자를 재사용합니다."),
        ("layered =", "같은 두 문구를 system과 developer로 나누고 고객 문의는 user에 둡니다."),
        ("comparison =", "두 응답의 단어 표시, 사용량, 지연 시간을 조건 이름별 딕셔너리로 묶습니다."),
        ("persona =", "페르소나만 둔 기준 응답의 원문과 사용량을 보존합니다."),
        ("bounded =", "같은 페르소나에 세 줄 형식과 금지 조건을 추가합니다."),
        ("zero =", "입출력 예시가 없는 기준 응답을 먼저 저장합니다."),
        ("relevant_example =", "관련 예시와 관련 없는 예시는 한 개씩 두고 현재 질문은 고정합니다."),
        ("ChatPromptTemplate", "optional placeholder는 기록이 없는 첫 요청에서도 메시지 틀을 완성합니다."),
        ("first = run", "기록 없음과 한 턴 기록의 완성 메시지를 각각 호출합니다."),
        ("direct =", "내부 추론 전문을 요구하지 않고 필요한 최종 필드만 요청합니다."),
        ("evidence =", "공개 가능한 짧은 근거 한 줄과 최종 답을 요청합니다."),
        ("messages =", "LABEL 첫 줄 형식을 고정한 같은 프롬프트를 세 번 독립 호출합니다."),
        ("allowed =", "LABEL 접두어와 열거형을 정확히 검사하고 전체 표본의 엄격 과반수만 합의로 인정합니다."),
        ("token_values =", "사용량이 하나라도 없으면 0으로 바꾸지 않고 전체 토큰을 None으로 남깁니다."),
        ("prompts =", "질문은 고정하고 JSON 지시의 구체성만 세 단계로 바꿉니다."),
        ("diagnostics =", "json.loads 파싱 성공과 필요한 영문 필드 존재를 별도로 기록합니다."),
        ("versions =", "v3는 v2 제약을 유지한 채 관련 예시만 추가합니다."),
        ("runs =", "세 버전을 같은 system 메시지와 모델 설정으로 한 번씩 실행합니다."),
        ("table =", "usage_metadata의 토큰과 지연, 단어 표시 수를 버전별 행으로 만듭니다."),
        ("from pathlib import Path", "프롬프트 원문과 raw 응답을 UTF-8 JSON으로 저장한 뒤 다시 읽어 확인합니다."),
        ("user_only", "같은 문구를 합친 조건과 역할별로 나눈 조건의 측정 레코드를 나란히 출력합니다."),
        ("task_constraints", "페르소나 조건과 구체 제약 조건의 글자 수·토큰·지연을 원문 이름과 연결합니다."),
        ("zero_shot", "예시 없음·관련 예시·관련 없는 예시의 raw 응답을 모두 출력합니다."),
        ("history_empty", "기록 없음과 한 턴 기록의 응답 원문과 사용량을 메시지 수와 함께 비교합니다."),
        ("brief_evidence", "최종 답만 요청한 조건과 짧은 근거를 추가한 조건의 길이·사용량을 비교합니다."),
        ("for name, result", "각 조건의 raw 응답을 생략하지 않고 단어 표시와 사용량 옆에 출력합니다."),
    ]
    if not text.startswith("#"):
        note = next((note for marker, note in notes if marker in text),
                    "조건별 원문과 측정값을 이름과 함께 출력하여 비교합니다.")
        text = f"# {note}\n{text}"
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text}


def notebook(title: str, question: str, cells: list[dict]) -> dict:
    return {
        "cells": [
            md(f"# {title}\n\n{question}"),
            md("## 패키지 준비\n\n첫 실행에서 수업 기준 버전을 설치합니다."),
            code(INSTALL),
            md("## API 키와 모델 준비\n\n상위 폴더의 `.env`를 찾고 키의 존재만 확인합니다."),
            code(ENV_MODEL),
            md("## 고정 과제\n\n모든 절에서 같은 고객 문의와 확인 단어를 사용합니다."),
            code(TASK_INPUT),
            md('## 측정 함수\n\n단어 포함 표시는 원문 정독을 돕는 표시이며 품질 점수가 아닙니다.\n\n`run(messages)`는 이 노트북에서 작성하는 보조 함수입니다. 역할·내용 목록을 받아 `model.invoke()`를 한 번 실행하고, 답 문자열·사용량·경과 초를 담은 딕셔너리를 반환합니다. `def` 셀은 함수를 정의할 뿐이며 뒤에서 `run(...)`을 호출할 때 모델 요청이 시작됩니다. `mention_flags(text)`는 지정 단어가 문자열에 있는지 표시한 딕셔너리를 반환합니다. 답의 뜻을 판단하는 모델 호출은 포함하지 않습니다.'),
            code(HELPERS),
            *cells,
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": "experiment",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


LESSONS: dict[str, dict] = {
    "01-역할별-메시지와-제약": notebook(
        "역할별 메시지와 제약",
        "같은 내용을 사용자 메시지 하나에 넣을 때와 역할별로 나눌 때 응답을 어떻게 비교할 수 있을까요?",
        [
            md('## 사용자 메시지 하나로 실행\n\n업무 규칙과 질문을 한 메시지에 합칩니다.\n\n`run(messages)`는 바로 앞에서 정의한 함수입니다. 메시지 목록을 받아 모델을 한 번 호출하고 `text`, `usage`, `latency_s`를 가진 딕셔너리를 반환합니다. 함수 정의는 요청하지 않으며, 아래 `run(...)` 호출이 실제 실행 시점입니다.\n\n`role_text`는 담당 역할, `constraint_text`는 답변의 제약, `TASK`는 고객 원문입니다. `+ "\n" +`는 문장을 줄바꿈으로 이어 붙입니다. 다음 조건은 같은 문구를 서로 다른 메시지 역할에 배치하므로 새로운 지시가 추가된 비교와 구분됩니다.\n\n번역 규칙은 유지하고 번역 대상만 바꾸는 경우에도 같은 구조를 사용할 수 있습니다. 역할을 나누면 교체할 위치가 보이지만 실제 답이 더 나아졌는지는 응답 원문으로 판단해야 합니다.'),
            code('role_text = "당신은 전자상거래 고객 지원 분류기입니다."\nconstraint_text = "근거 없는 보상은 약속하지 말고 세 항목을 짧게 답하세요."\nflat = run([("user", role_text + "\\n" + constraint_text + "\\n" + TASK)])\nprint(json.dumps(flat, ensure_ascii=False, indent=2))'),
            md("## 역할별 메시지로 실행\n\n공통 행동은 system, 과업 제약은 developer, 사례는 user에 둡니다. developer 역할은 제공자별 지원 차이를 확인해야 합니다."),
            code('layered = run([\n    ("system", role_text),\n    ("developer", constraint_text),\n    ("user", TASK),\n])\nprint(json.dumps(layered, ensure_ascii=False, indent=2))'),
            md("## 고정 루브릭으로 비교\n\n문장 취향이 아니라 미리 정한 세 항목으로 두 원문을 확인합니다."),
            code('comparison = {\n    "user_only": {**mention_flags(flat["text"]), "usage": flat["usage"], "latency_s": flat["latency_s"]},\n    "role_split": {**mention_flags(layered["text"]), "usage": layered["usage"], "latency_s": layered["latency_s"]},\n}\nprint(json.dumps(comparison, ensure_ascii=False, indent=2))'),
        ],
    ),
    "02-페르소나와-과업-제약": notebook(
        "페르소나와 과업 제약",
        "페르소나 이름만 주는 것과 수행할 일·금지 사항·출력 형식을 함께 주는 것은 어떤 차이를 만들까요?",
        [
            md('## 페르소나만 지정\n\n친절한 상담원이라는 성격만 지정합니다.\n\n페르소나는 답하는 사람의 역할·말투·관점을 지정한 설명입니다. 아래 첫 조건의 “친절한 고객 상담원”은 태도에 관한 문장이고, 다음 조건의 세 줄 형식과 규정 밖 약속 금지는 수행 조건입니다. 두 번째 조건이 더 길다는 사실 자체를 품질 개선으로 해석하지 않습니다.\n\n회의록 정리에서는 “숙련된 비서”라는 역할에 결정 사항·담당자·기한을 추출하라는 과업과 미정 기한을 추측하지 말라는 조건을 따로 붙일 수 있습니다. 같은 구분을 고객 문의에 적용해 말투, 필수 정보, 금지 사항, 출력 배열을 각각 읽습니다.\n\n`persona`와 `bounded`는 함수가 아니라 `run()`이 반환한 결과 딕셔너리입니다. `result["text"]`는 모델이 생성한 원문이고 `len(...)`은 그 문자열의 글자 수입니다. 요청에 쓴 글자 수나 토큰 수와 구분합니다.'),
            code('persona = run([("system", "당신은 친절한 고객 상담원입니다."), ("user", TASK)])\nprint(json.dumps(persona, ensure_ascii=False, indent=2))'),
            md("## 과업과 제약을 함께 지정\n\n누구인지에 더해 무엇을 어떤 범위에서 답할지 적습니다."),
            code('bounded = run([\n    ("system", "당신은 친절한 고객 상담원입니다."),\n    ("user", "세 줄로 답하세요. 1) 분류 2) 다음 행동 3) 고객 문장. "\n             "규정에 없는 환불이나 보상을 약속하지 마세요.\\n" + TASK),\n])\nprint(json.dumps(bounded, ensure_ascii=False, indent=2))'),
            md("## 결과 비교\n\n같은 세 평가 항목과 응답 길이를 함께 확인합니다."),
            code('for name, result in {"persona": persona, "task_constraints": bounded}.items():\n    print(name, mention_flags(result["text"]), "글자 수", len(result["text"]),\n          "토큰", result["usage"], "지연", result["latency_s"])'),
        ],
    ),
    "03-Few-shot-예시-선택": notebook(
        "Few-shot 예시 선택",
        "예시가 없을 때, 관련 예시가 있을 때, 형식만 비슷한 관련 없는 예시가 있을 때 결과는 어떻게 달라질까요?",
        [
            md("## 예시 없이 실행\n\n출력 형식만 설명합니다."),
            code('zero = run([("system", "분류/다음 행동/고객 문장 형식으로 답하세요."), ("user", TASK)])\nprint(json.dumps(zero, ensure_ascii=False, indent=2))'),
            md('## 관련 예시와 관련 없는 예시 비교\n\n두 조건 모두 예시는 하나이며, 현재 질문과의 관련성만 다릅니다.\n\nFew-shot은 예시 입력과 예시 답의 대응을 현재 요청에 함께 넣는 방식입니다. `relevant_example`과 `irrelevant_example`은 준비된 문자열이며 현재 질문 `TASK` 앞에 연결됩니다. 별도의 모델 훈련은 수행하지 않습니다. 고정된 작은 예시를 직접 고르는 방식이며 자동 예시 선택기는 사용하지 않습니다.\n\n감정 분류에서는 칭찬과 불만이 함께 있는 문장이 경계 예시가 될 수 있습니다. 상담에서는 상품명보다 파손 사실과 사진 확인이라는 판단 구조가 관련성을 결정합니다. 예시 수뿐 아니라 어떤 구분을 보여 주는지를 확인합니다.\n\n예시의 B-203은 현재 문의의 주문번호가 아닙니다. 현재 A-1042를 그대로 유지하면서 예시의 분류 방식만 적용했는지 원문을 읽습니다. 아래 단어 포함 표시는 형식·사실·규정 준수 전체의 점수가 아닙니다.'),
            code('relevant_example = """예시 문의: 셔츠 단추가 떨어졌습니다. 주문번호 B-203입니다.\n예시 답: 분류=교환 / 다음 행동=하자 사진과 주문번호 확인 / 고객 문장=사진을 첨부해 주세요."""\nirrelevant_example = """예시 문의: 뉴스레터 글꼴을 바꾸고 싶습니다.\n예시 답: 분류=설정 / 다음 행동=설정 메뉴 확인 / 고객 문장=글꼴 메뉴를 선택해 주세요."""\nfew = run([("system", "분류/다음 행동/고객 문장 형식으로 답하세요."),\n           ("user", relevant_example + "\\n\\n" + TASK)])\noff = run([("system", "분류/다음 행동/고객 문장 형식으로 답하세요."),\n           ("user", irrelevant_example + "\\n\\n" + TASK)])'),
            md('## 세 조건의 원문과 확인 표시\n\n예시가 정답을 보장하는지, 입력 토큰이 얼마나 늘었는지도 확인합니다.'),
            code('for name, result in {"zero_shot": zero, "relevant": few, "unrelated": off}.items():\n    print("\\n", name, json.dumps(mention_flags(result["text"]), ensure_ascii=False),\n          result["usage"], result["latency_s"])\n    print(result["text"])'),
        ],
    ),
    "04-ChatPromptTemplate과-MessagesPlaceholder": notebook(
        "ChatPromptTemplate과 MessagesPlaceholder",
        "메시지 틀과 선택적 대화 기록을 사용하면 같은 프롬프트 구조를 어떻게 재사용할 수 있을까요?",
        [
            md('## 메시지 템플릿 만들기\n\n`MessagesPlaceholder(optional=True)`는 기록이 없는 첫 요청도 같은 틀로 처리합니다.\n\n`from_messages()`는 고정 메시지와 빈칸으로 템플릿을 만드는 클래스 메서드입니다. `{format_rule}`와 `{question}`은 실행 때 값으로 채울 변수 자리입니다. `base_values`가 같은 이름의 키로 값을 제공합니다. 여기서는 문자열 앞에 `f`가 없으므로 Python이 미리 값을 채우는 방식이 아닙니다.\n\n`prompt.invoke(base_values)`는 완성한 `ChatPromptValue`를 만들고 `.to_messages()`가 역할 있는 메시지 객체 목록으로 바꿉니다. 이 단계는 모델을 호출하지 않습니다. 다음 `run(first_messages)`의 내부에서 `model.invoke()`를 실행할 때 요청이 발생합니다.\n\n`MessagesPlaceholder("history", optional=True)`는 과거 메시지 목록을 삽입할 자리입니다. 기억을 저장하는 기능이 아니며 값이 없으면 빈 목록으로 처리합니다. 다음 셀은 human 질문과 ai 답이라는 메시지 두 개로 한 턴을 추가합니다. `{**base_values, "history": ...}`는 기존 딕셔너리 항목을 펼친 새 딕셔너리에 history를 추가하는 Python 표기입니다.'),
            code('from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder\n\nprompt = ChatPromptTemplate.from_messages([\n    ("system", "고객 지원 답변을 {format_rule} 형식으로 작성하세요."),\n    MessagesPlaceholder("history", optional=True),\n    ("human", "{question}"),\n])\nbase_values = {"format_rule": "분류/다음 행동/고객 문장", "question": TASK}\nfirst_messages = prompt.invoke(base_values).to_messages()\nprint([(m.type, m.text[:80]) for m in first_messages])'),
            md("## 기록 없음과 한 건 있음 비교\n\n과거 고객 요청 한 건만 추가하고 현재 질문과 평가 기준은 유지합니다."),
            code('first = run(first_messages)\nwith_history = prompt.invoke({**base_values, "history": [\n    ("human", "답변을 세 줄 이내로 써 주세요."),\n    ("ai", "알겠습니다. 이후 답변을 세 줄 이내로 작성하겠습니다."),\n]}).to_messages()\nsecond = run(with_history)\nprint("메시지 수:", len(first_messages), len(with_history))'),
            md("## 실행 결과 확인\n\n템플릿에 채워진 메시지와 모델 응답을 구분하여 읽습니다."),
            code('for name, result in {"history_empty": first, "history_one_turn": second}.items():\n    print("\\n", name, mention_flags(result["text"]), result["usage"], result["latency_s"])\n    print(result["text"])'),
        ],
    ),
    "05-CoT와-ReAct의-경계": notebook(
        "CoT와 ReAct의 경계",
        "내부 추론 전문을 요구하지 않고도 결론과 확인 가능한 근거를 받는 프롬프트를 어떻게 설계할까요?",
        [
            md("## 짧은 최종 답 요청\n\n세부 내부 추론은 요청하지 않고 필요한 결과만 지정합니다."),
            code('direct = run([\n    ("system", "고객 지원 요청을 분류하세요."),\n    ("user", "최종 답만 분류/다음 행동/고객 문장 형식으로 쓰세요.\\n" + TASK),\n])\nprint(json.dumps(direct, ensure_ascii=False, indent=2))'),
            md('## 확인 가능한 근거를 한 줄 추가\n\n숨은 사고 과정을 요구하는 대신 입력에서 확인한 사실을 짧게 쓰게 합니다.\n\n공개 근거는 독자가 입력에서 다시 찾을 수 있는 사실이나 기준을 짧게 적은 문장입니다. 모델 내부의 비공개 추론 기록과 구분합니다. 이번 입력에서는 뚜껑 파손과 사진 제출 규정을 각각 근거 문장의 내용과 대조할 수 있습니다.\n\n“조회하겠습니다”라는 문장이 나왔다고 조회 코드가 실행된 것은 아닙니다. ReAct의 행동·관찰 반복에는 실제 도구 호출과 결과 전달이 필요하지만 이 절은 각 조건에서 텍스트 응답을 한 번 받습니다.\n\n영수증에서 수량과 단가를 근거로 표시하는 것과 계산 함수를 실행해 합계를 검증하는 것도 다른 단계입니다. 아래 결과는 입력의 사실을 얼마나 읽기 좋게 제시했는지 확인할 자료이며 실제 도구 실행이나 내부 추론의 증거로 쓰지 않습니다.'),
            code('evidence = run([\n    ("system", "고객 지원 요청을 분류하세요."),\n    ("user", "내부 판단 과정은 공개하지 말고, 결론과 입력에서 확인한 근거 한 줄을 쓴 뒤 "\n             "분류/다음 행동/고객 문장을 제시하세요.\\n" + TASK),\n])\nprint(json.dumps(evidence, ensure_ascii=False, indent=2))'),
            md("## A/B 결과 비교\n\nReAct의 행동 루프는 구현하지 않습니다. 이 절에서는 텍스트 계획과 최종 답의 경계만 확인합니다."),
            code('for name, result in {"direct": direct, "brief_evidence": evidence}.items():\n    print(name, mention_flags(result["text"]), "글자 수", len(result["text"]),\n          result["usage"], result["latency_s"])'),
        ],
    ),
    "06-Self-Consistency와-표본-합의": notebook(
        "Self-Consistency와 표본 합의",
        "같은 질문을 독립적으로 여러 번 실행한 최종 답을 어떻게 모으고, 합의 결과의 한계를 어떻게 기록할까요?",
        [
            md('## 반복 조건 고정\n\n모델, 질문, 프롬프트와 평가 기준을 유지한 채 세 번 호출합니다.\n\nSelf-Consistency는 다양한 추론 경로를 표집한 뒤 각 경로의 최종 답을 집계하는 기법입니다. 이 노트북은 내부 추론을 수집하지 않고 최종 라벨만 반복 생성·집계하는 축소 실습으로, 원 기법의 전체 절차를 재현하지 않습니다.'),
            code('messages = [\n    ("system", "첫 줄에 LABEL: 배송, LABEL: 교환, LABEL: 환불 중 하나만 쓰고 "\n               "둘째 줄에 확인 근거를 쓰세요."),\n    ("user", TASK),\n]\nsamples = [run(messages) for _ in range(3)]\nfor index, item in enumerate(samples, 1):\n    print(f"표본 {index}:", item["text"], item["usage"], item["latency_s"])'),
            md('## 최종 답에서 분류 추출\n\n공개된 최종 답의 분류 단어만 집계합니다. 내부 추론은 수집하지 않습니다.\n\n`splitlines()`는 응답 문자열을 줄 목록으로 나누고 `[0]`은 첫 줄을 선택합니다. `startswith("LABEL: ")`로 접두어를 검사한 뒤 그 길이 이후의 부분을 슬라이스하여 라벨을 읽습니다. `allowed`는 허용한 라벨의 집합이며 포함되지 않은 값은 형식 오류로 기록합니다.\n\n이 코드의 과반 기준은 유효 응답 수가 아니라 전체 표본 수입니다. `count > len(samples) // 2`이므로 세 번 중 같은 유효 라벨이 두 번 이상 있어야 합니다. 교환·형식 오류·형식 오류라면 한 건만 유효해도 합의 없음입니다. `next(..., "합의 없음")`는 조건을 만족하는 라벨이 없을 때 사용할 값을 지정합니다.\n\nSelf-Consistency의 원 기법은 여러 추론 경로를 표집하고 최종 답을 집계합니다. 여기서는 최종 라벨 합의만 읽는 축소 실습이므로 추론 경로 표집을 구현하지 않습니다. 별도 호출이어도 같은 모델의 편향이 반복될 수 있으며 다수결이 사실 확인을 대신하지 않습니다.'),
            code('allowed = {"배송", "교환", "환불"}\nlabels = []\nfor item in samples:\n    first_line = item["text"].splitlines()[0].strip()\n    has_prefix = first_line.startswith("LABEL: ")\n    label = first_line[len("LABEL: "):].strip() if has_prefix else "형식 오류"\n    labels.append(label if label in allowed else "형식 오류")\nvalid = [label for label in labels if label in allowed]\ncounts = {label: valid.count(label) for label in sorted(set(valid))}\nconsensus = next((label for label, count in counts.items()\n                  if count > len(samples) // 2), "합의 없음")\nprint("표본 분류:", labels, "빈도:", counts, "합의:", consensus)'),
            md("## 품질과 비용 함께 확인\n\n합의 여부와 별개로 각 원문이 고정 루브릭을 충족했는지 확인합니다."),
            code('token_values = [item["usage"].get("total_tokens") if item["usage"] else None\n                for item in samples]\nsummary = {\n    "sample_count": len(samples),\n    "unanimous": len(set(labels)) == 1 and "형식 오류" not in labels,\n    "mention_flags": [mention_flags(item["text"]) for item in samples],\n    "total_tokens": sum(token_values) if all(v is not None for v in token_values) else None,\n    "total_latency_s": round(sum(item["latency_s"] for item in samples), 3),\n}\nprint(json.dumps(summary, ensure_ascii=False, indent=2))'),
        ],
    ),
    "07-구조화-출력-프롬프트-진단": notebook(
        "구조화 출력 프롬프트 진단",
        "같은 JSON 요구를 세 가지 프롬프트로 표현했을 때 파싱과 필드 존재 여부는 어떻게 달라질까요?",
        [
            md("## 세 프롬프트 조건 준비\n\n질문과 필요한 필드는 같고 JSON 지시의 구체성만 다릅니다."),
            code('prompts = {\n    "brief": "JSON으로 답하세요. " + TASK,\n    "fields": "JSON 객체로 답하세요. 필드는 category, next_action, customer_message입니다. " + TASK,\n    "schema": "설명이나 코드 울타리 없이 JSON 객체 하나만 답하세요. "\n              "category는 배송/교환/환불 중 하나이고 모든 필드는 문자열입니다. "\n              "필드: category, next_action, customer_message. " + TASK,\n}\nresults = {name: run([("system", "고객 지원 데이터를 만듭니다."), ("user", text)])\n           for name, text in prompts.items()}'),
            md('## 실제 파싱과 필드 검사\n\n파싱 실패를 가정하지 않고 각 원문에 `json.loads`를 실제 적용합니다.\n\n`json.loads()`의 입력은 응답 문자열이고 반환값은 JSON 내용에 대응하는 Python 값입니다. JSON 객체는 딕셔너리, 배열은 목록이 됩니다. 파싱 성공만으로 원하는 객체나 필드를 받았다고 볼 수 없습니다. 이번에 저장된 세 응답은 객체이지만 일반 입력에 대한 자료형 검증까지 이 코드가 수행하는 것은 아닙니다.\n\n`{f: f in parsed for f in fields}`는 필요한 필드별로 키가 있는지 표시하는 사전 표현식입니다. 키 값의 타입·허용값·빈 문자열·업무 사실은 검사하지 않습니다. 예를 들어 빈 category도 키 자체가 있으면 이 검사에서는 참입니다.\n\n일정 자료의 “일시”를 프로그램이 기대하는 `starts_at`으로 바꾸는 문제와 날짜가 실제로 맞는지 확인하는 문제도 다릅니다. 아래 결과에서는 파싱 성공과 영문 필드 충족부터 따로 읽고, 전체 검증이 끝났다고 해석하지 않습니다.'),
            code('diagnostics = {}\nfor name, result in results.items():\n    try:\n        parsed = json.loads(result["text"])\n        fields = ["category", "next_action", "customer_message"]\n        diagnostics[name] = {"parsed": True, "fields": {f: f in parsed for f in fields}}\n    except (json.JSONDecodeError, TypeError) as error:\n        diagnostics[name] = {"parsed": False, "error": type(error).__name__}\nprint(json.dumps(diagnostics, ensure_ascii=False, indent=2))'),
            md("## 원문·사용량·진단 함께 보기\n\n모두 성공했다면 이번 표본에서 파싱 실패를 관찰하지 못했다고 기록합니다."),
            code('for name, result in results.items():\n    print("\\n", name, diagnostics[name], result["usage"], result["latency_s"])\n    print(result["text"])'),
        ],
    ),
    "08-프롬프트-버전과-AB-비교": notebook(
        "프롬프트 버전과 A/B 비교",
        "같은 과제를 세 가지 프롬프트 전략으로 실행하고 토큰·지연·단어 포함 표시를 한 표에 어떻게 기록할까요?",
        [
            md('## Ch 6 측정 기록 연결\n\nCh 6이 저장한 제공자 측정 기록을 읽고 공통 필드와 파일 지문을 확인합니다.\n\n`run_id`는 실행을 구분하는 이름이고 SHA-256은 파일 내용을 바이트로 읽어 계산한 지문입니다. `read_text()`는 텍스트를, `read_bytes()`는 바이트를 읽습니다. `hexdigest()`는 계산된 지문을 16진수 문자열로 표현합니다. 이 값은 내용 변경을 비교하는 데 쓰며 사실 정확성을 평가하는 점수는 아닙니다.\n\n`next((path for path in ... if ...), None)`는 조건에 맞는 첫 경로를 찾고 없으면 `None`을 반환합니다. `[Path.cwd(), *Path.cwd().parents]`에서 별표는 상위 경로들을 목록 안에 펼칩니다. 현재 폴더부터 상위 폴더를 찾는 준비 코드이며 모델 입력을 만드는 단계와 구분합니다.\n\n`required <= ch06_record.keys()`는 필요한 키 집합이 저장 기록의 키에 모두 포함되는지 검사합니다. 이어지는 기록은 같은 필드 형식을 참고하지만 고객 문의와 Ch 6의 질문이 다르므로 두 실행 수치를 성능 변화로 비교하지 않습니다.'),
            code('from hashlib import sha256\nfrom pathlib import Path\n\ncourse_root = next((path for path in [Path.cwd(), *Path.cwd().parents]\n                    if (path / "labs/part2/ch06-langchain-start").is_dir()), None)\nif course_root is None:\n    raise FileNotFoundError("실습 묶음의 labs/part2 폴더를 찾지 못했습니다.")\nch06_relative = Path("labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json")\nch06_path = course_root / ch06_relative\nif not ch06_path.exists():\n    raise FileNotFoundError("Ch 6의 06 노트북을 먼저 실행하세요.")\nch06_record = json.loads(ch06_path.read_text(encoding="utf-8"))\nch06_sha256 = sha256(ch06_path.read_bytes()).hexdigest()\nrequired = {"run_id", "run_date", "source_chapter", "conditions", "pricing", "records"}\nassert required <= ch06_record.keys()\nassert ch06_record["pricing"]["openai"] == {"ordinary_input": 0.75, "cached_input": 0.075, "output": 4.50}\nprint("Ch 6 기록:", ch06_record["run_id"], ch06_sha256[:12])'),
            md("## 버전과 변경 이유 기록\n\n버전마다 바꾼 조건을 한 가지 전략으로 설명합니다."),
            code('versions = {\n    "v1-direct": "답하세요. " + TASK,\n    "v2-constraints": "분류/다음 행동/고객 문장 세 줄로 답하고 규정 밖 약속은 하지 마세요. " + TASK,\n    "v3-example": "예시: 파손 상품은 교환으로 분류하고 사진과 주문번호를 확인합니다. "\n                  "분류/다음 행동/고객 문장 세 줄로 답하고 규정 밖 약속은 하지 마세요. " + TASK,\n}\nchange_log = {"v1-direct": "기준선", "v2-constraints": "형식·금지 조건",\n              "v3-example": "v2 조건 유지·관련 예시 추가"}\nprint(json.dumps(change_log, ensure_ascii=False, indent=2))'),
            md("## 세 전략 실행\n\n모델, 질문, 생성 상한과 평가 기준을 고정합니다."),
            code('runs = {}\nfor version, prompt_text in versions.items():\n    runs[version] = run([("system", "고객 지원 요청을 처리하세요."),\n                         ("user", prompt_text)])\n    print(version, runs[version]["text"])'),
            md("## 토큰·지연·자동 확인 결과\n\n단어 포함 수 동점도 결과입니다. 한 번의 실행으로 전략 전체의 우열을 확정하지 않습니다."),
            code('def estimate_openai_cost(usage):\n    input_tokens = usage.get("input_tokens")\n    output_tokens = usage.get("output_tokens")\n    if input_tokens is None or output_tokens is None:\n        return None\n    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0\n    normal_input = input_tokens - cache_read\n    return (normal_input * 0.75 + cache_read * 0.075 + output_tokens * 4.50) / 1_000_000\n\ntable = []\nfor version, result in runs.items():\n    usage = result["usage"] or {}\n    cache_read = (usage.get("input_token_details") or {}).get("cache_read") or 0\n    cost = estimate_openai_cost(usage)\n    table.append({"version": version, "change": change_log[version],\n                  "input_tokens": usage.get("input_tokens"), "output_tokens": usage.get("output_tokens"),\n                  "cache_read_tokens": cache_read,\n                  "estimated_cost_usd": None if cost is None else round(cost, 8),\n                  "latency_ms": round(result["latency_s"] * 1000, 1),\n                  "mention_count": sum(mention_flags(result["text"]).values()),\n                  "generation_evaluation": "human_review_required"})\nprint(json.dumps(table, ensure_ascii=False, indent=2))'),
            md("## 버전 기록 저장과 재확인\n\n프롬프트 원문, 고정 조건, 원문 응답을 상대 경로의 JSON 파일에 함께 저장합니다."),
            code('from datetime import datetime, timezone\n\nrun_at = datetime.now(timezone.utc)\nsession_id = run_at.strftime("%Y%m%dT%H%M%S%fZ")\nrecord = {"run_id": f"ch07-prompt-ab-{session_id}", "run_date": run_at.date().isoformat(),\n          "source_chapter": "ch07", "source_record": {"path": str(ch06_relative), "sha256": ch06_sha256, "run_id": ch06_record["run_id"]},\n          "model": "openai:gpt-5.4-mini", "settings": {"max_tokens": 220, "repetitions": 1,\n          "pricing_date": ch06_record["pricing"]["date"],\n          "pricing_usd_per_million": ch06_record["pricing"]["openai"]},\n          "input": TASK, "mention_screen": MENTIONS,\n          "comparison_policy": "mention_count는 원문 정독 보조이며 생성 답변 품질 점수가 아님",\n          "versions": {name: {"prompt": versions[name], "change": change_log[name],\n                               "result": runs[name], "metrics": table[index]}\n                       for index, name in enumerate(versions)}}\nruns_dir = course_root / "labs/part2/ch07-prompt-engineering/runs"\nrecord_path = runs_dir / "prompt-ab-continuity.json"\nsession_path = runs_dir / "continuity" / session_id / record_path.name\nsession_path.parent.mkdir(parents=True, exist_ok=False)\npayload = json.dumps(record, ensure_ascii=False, indent=2)\nrecord_path.write_text(payload, encoding="utf-8")\nsession_path.write_text(payload, encoding="utf-8")\nprint(record_path.relative_to(course_root), "보존 사본:", session_path.relative_to(course_root))'),
        ],
    ),
}


for slug, data in LESSONS.items():
    for index, cell in enumerate(data["cells"], start=1):
        cell["id"] = f"cell-{index:02d}"
    path = NOTEBOOKS / f"{slug}.ipynb"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", path.name)
