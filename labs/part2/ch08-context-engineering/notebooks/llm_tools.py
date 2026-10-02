"""Ch 8 컨텍스트 엔지니어링 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from llm_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(encoding, persona_text, task_text, closure_keep_words 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""


# 01절에서 배웠습니다 — 수업 예산에서 출력 예약분과 여유분을 빼, 입력에 쓸 수 있는 토큰 수를 반환합니다
def input_budget(total_budget, output_reserve, safety_margin):
    available = total_budget - output_reserve - safety_margin
    return available


# 01절에서 배웠습니다 — 토큰화 규칙 객체로 글 하나를 토큰 번호 목록으로 바꾸고, 그 개수(토큰 수)를 반환합니다
# 01절 판은 바깥 이름 encoding을 읽었고, 이 판은 토큰화 규칙 객체를 첫 인자로 받습니다
def count_tokens(encoding, text):
    token_ids = encoding.encode(text)
    return len(token_ids)


# 02절에서 배웠습니다 — 답 글에 출처 표시가 들어 있는 기록만 골라 목록으로 반환합니다
def find_cited_notes(answer_text, notes):
    cited = []
    for note in notes:
        mark = "[" + note["출처"] + "]"
        if mark in answer_text:
            cited.append(note)
    return cited


# 03절에서 배웠습니다 — 글에 들어 있지 않은 지킬 말만 모아 목록으로 반환합니다
def find_missing_words(text, words):
    missing = []
    for word in words:
        if word not in text:
            missing.append(word)
    return missing


# 04절에서 배웠습니다 — 기록 목록과 질문 하나로 Ch 7 모양의 메시지 목록(system·developer·user)을 만들어 반환합니다
# 04절 판은 바깥 이름 persona_text·task_text를 읽었고, 이 판은 두 글을 앞의 두 인자로 받습니다
def build_notes_messages(persona_text, task_text, notes, question):
    evidence_text = ""
    for note in notes:
        evidence_text = evidence_text + "[" + note["출처"] + "] " + note["내용"] + "\n"
    user_text = evidence_text + "\n" + "질문: " + question
    messages = [
        ("system", persona_text),
        ("developer", task_text),
        ("user", user_text),
    ]
    return messages


# 04절에서 배웠습니다 — 답의 출처 표시와 같은 기록의 출처, 답에서 빠진 지킬 말을 딕셔너리로 반환합니다
# 04절 판은 바깥 이름 closure_keep_words를 읽었고, 이 판은 지킬 말 목록을 셋째 인자로 받습니다
def check_answer(answer_text, notes, keep_words):
    cited = find_cited_notes(answer_text, notes)
    cited_sources = []
    for note in cited:
        cited_sources.append(note["출처"])
    missing = find_missing_words(answer_text, keep_words)
    check = {"답의 출처 표시와 같은 기록": cited_sources, "답에서 빠진 지킬 말": missing}
    return check


# 05절에서 배웠습니다 — 답 글을 출처 표시로 나눈 조각 수에서 1을 빼, 표시가 몇 번 들어 있는지 반환합니다
def count_marks(answer_text, mark):
    pieces = answer_text.split(mark)
    mark_count = len(pieces) - 1
    return mark_count


# 06절에서 배웠습니다 — 문서 목록에서 출처가 같은 문서를 찾아 반환합니다(없으면 None)
def open_document(document_list, source):
    for document in document_list:
        if document["출처"] == source:
            return document
    return None


# Ch 7 08절에서 배웠습니다 — 사용량과 세 요금(기본값 mini 요금, 100만 토큰당 달러)으로 요청 한 번의 예상 비용(달러)을 반환합니다
def estimate_openai_cost(usage, input_rate=0.75, cached_input_rate=0.075, output_rate=4.50):
    if usage is None:
        return None
    # 캐시 입력 키가 없으면 할인 없이 모두 입력 요금으로 계산합니다
    details = usage.get("input_token_details", {})
    cache_read = details.get("cache_read", 0)
    normal_input = usage["input_tokens"] - cache_read
    input_cost = normal_input * input_rate + cache_read * cached_input_rate
    output_cost = usage["output_tokens"] * output_rate
    price_unit = 1000000
    return (input_cost + output_cost) / price_unit
