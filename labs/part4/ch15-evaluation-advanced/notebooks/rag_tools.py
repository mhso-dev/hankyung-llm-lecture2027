"""Ch 15 평가 심화 — 앞 챕터와 이 챕터 앞 절에서 배운 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from rag_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""

import json
import math


# Ch 11 01절에서 배웠습니다 — 검색 항목에서 문서 ID를 순서대로 모으고 처음 나온 것만 남긴 고유 문서 목록을 만듭니다
def unique_doc_ids(hit_list):
    doc_ids = []
    for hit in hit_list:
        if hit["doc_id"] not in doc_ids:
            doc_ids.append(hit["doc_id"])
    return doc_ids


# Ch 11 01절에서 배웠습니다 — 고유 문서 목록에서 정답 문서 ID가 몇 번째 자리인지 찾습니다(찾지 못하면 0)
def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank


# Ch 11 04절에서 배웠습니다 — 자리 번호를 받아 그 자리의 무게를 냅니다(자리 1이 가장 크고 뒤로 갈수록 작아집니다)
def rank_weight(rank):
    return 1 / math.log2(rank + 1)


# Ch 11 05절에서 배웠습니다 — 정답 문서 자리를 보고 오류 이름 셋 가운데 하나를 고릅니다
# 자리 0은 후보 밖, 자르는 자리보다 뒤는 뒤로 밀림, 그 안은 앞자리 안입니다
def error_name(gold_rank, cutoff):
    if gold_rank == 0:
        return "후보 밖"
    if gold_rank > cutoff:
        return "뒤로 밀림"
    return "앞자리 안"


# Ch 15 02절에서 배웠습니다 — 판정 머리글 뒤에 견줄 두 칸을 이름과 함께 이어 붙여 판정 요청 글 하나를 만듭니다
def build_judge_prompt(judge_head, pair, case):
    prompt_text = judge_head + "\n\n"
    for label in pair:
        field = pair[label]
        prompt_text = prompt_text + label + ":\n" + case[field] + "\n\n"
    return prompt_text


# Ch 15 02절에서 배웠습니다 — 판정 요청 글 하나를 평가 모델에 보내고 받은 JSON 글을 딕셔너리로 읽습니다
def judge_once(judge_model, prompt_text):
    reply = judge_model.invoke(prompt_text)
    verdict = json.loads(reply.text)
    return verdict


# Ch 15 03절에서 배웠습니다 — 판정 머리글 하나로 사례 여러 건의 판정을 받아 질문 번호별로 모읍니다(사례 한 건에 모델 요청 1번)
def score_cases(judge_model, judge_head, pair, case_list):
    verdicts = {}
    for case in case_list:
        prompt_text = build_judge_prompt(judge_head, pair, case)
        verdicts[case["qid"]] = judge_once(judge_model, prompt_text)
    return verdicts


# Ch 6 06절에서 배웠습니다 — 사용량 딕셔너리와 세 요금(100만 토큰당 달러)으로 요청 한 번의 예상 비용(달러)을 계산합니다
# 사용량이 None이면 비용도 None을 내고, 입력 토큰 가운데 캐시 입력을 뺀 나머지를 일반 입력으로 봅니다
def estimate_cost(usage, input_rate, cached_input_rate, output_rate):
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


# Ch 15 04절에서 배웠습니다 — 이름별 판정 딕셔너리에서 점수만 꺼내 이름별 점수 딕셔너리를 만듭니다
def scores_of(verdicts):
    scores = {}
    for name in verdicts:
        scores[name] = verdicts[name]["score"]
    return scores


# Ch 15 06절에서 배웠습니다 — 값 목록을 모두 더해 값의 수로 나눈 평균을 냅니다(여섯째 자리에서 반올림합니다)
def average(values):
    total = 0
    for value in values:
        total = total + value
    return round(total / len(values), 6)


# Ch 15 07절에서 배웠습니다 — 평균만 보는 검사입니다: 이후 판 평균이 이전 판 평균보다 낮지 않으면 통과로 봅니다
def check_by_average(old_scores, new_scores):
    old_values = list(old_scores.values())
    new_values = list(new_scores.values())
    return average(new_values) >= average(old_values)


# Ch 15 07절에서 배웠습니다 — 기준선에서 1이던 사례 가운데 이후 판에서 0이 된 사례의 질문 번호를 모읍니다
def broken_cases(old_scores, new_scores):
    broken = []
    for qid in old_scores:
        if old_scores[qid] == 1 and new_scores[qid] == 0:
            broken.append(qid)
    return broken


# Ch 15 07절에서 배웠습니다 — 사례마다 짝지어 보는 검사입니다: 평균이 낮지 않고 깨진 사례도 없어야 통과로 봅니다
def check_by_case(old_scores, new_scores):
    average_ok = check_by_average(old_scores, new_scores)
    broken = broken_cases(old_scores, new_scores)
    return average_ok and len(broken) == 0


# Ch 15 08절에서 배웠습니다 — JSONL 파일을 읽어 빈 줄을 뺀 줄마다 JSON으로 읽고 딕셔너리 목록을 만듭니다
def read_jsonl(file_path):
    with open(file_path, encoding="utf-8") as file:
        text_lines = file.read().split("\n")
    rows = []
    for text_line in text_lines:
        if text_line != "":
            rows.append(json.loads(text_line))
    return rows


# Ch 15 08절에서 배웠습니다 — 첫째 목록에는 있고 둘째 목록에는 없는 이름을 첫째 목록 차례대로 모읍니다
def ids_not_in(first_ids, second_ids):
    missing = []
    for custom_id in first_ids:
        if custom_id not in second_ids:
            missing.append(custom_id)
    return missing
