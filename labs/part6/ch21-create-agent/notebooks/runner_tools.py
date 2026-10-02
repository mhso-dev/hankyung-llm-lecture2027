"""Ch 21 create_agent — 앞 챕터와 앞 절에서 배운 평범한 함수를 모아 둔 도구 파일입니다.

노트북은 이 파일의 함수를 `from runner_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 챕터의 어느 절에서 배웠는지 적었습니다.
Ch 20 도구 파일 graph_tools.py에서 이 챕터 노트북이 쓰는 함수만 본문을 글자 그대로 옮겼습니다.
05절부터 쓰는 검색 함수 다섯은 Ch 14 도구 파일 rag_tools.py에서 본문을 글자 그대로 옮겼습니다(벡터 계산은 NumPy — Ch 5 02절).
06절부터 쓰는 정답 자리 함수 하나와 판정 함수 둘은 Ch 15 도구 파일 rag_tools.py에서 본문을 글자 그대로 옮겼습니다.
이 챕터 01절 노트북에서 처음 적은 함수(agent_row)도 02절부터 쓰므로 본문을 글자 그대로 옮겼습니다.
02절 노트북에서 처음 적은 함수(print_branches)도 03절부터 쓰므로 본문을 글자 그대로 옮겼습니다.
노트북에서 만든 이름을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
도구를 만드는 @tool 줄과 에이전트를 만드는 create_agent 줄은 이 파일에 두지 않고 노트북에 둡니다.
"""

import json

import numpy as np


# Ch 19 04절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다
# 모델 응답 하나에서 도구 호출 목록의 도구 이름만 모아 목록으로 내놓습니다(도구를 고르지 않았으면 빈 목록)
def tool_call_names(response):
    names = []
    for call in response.tool_calls:
        names.append(call["name"])
    return names


# Ch 19 06절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다
# 메시지 목록을 차례로 보며 종류 이름을 출력하고, 응답(AIMessage)이면 도구 호출 요청 이름을,
# 도구 메시지(ToolMessage)면 결과 상태(status)와 내용을 함께 출력합니다(내놓는 값 없음)
def show_messages(messages):
    for message in messages:
        kind = type(message).__name__
        if kind == "HumanMessage":
            print(kind)
        if kind == "AIMessage":
            print(kind, "| 도구 호출 요청:", tool_call_names(message))
        if kind == "ToolMessage":
            print(kind, "| 결과 상태:", message.status, "| 내용:", message.content)


# Ch 19 05절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다
# 메시지 목록에서 모델 응답(AIMessage)만 골라 요청 수와 입력·출력 토큰을 더해 딕셔너리로 내놓습니다
# 토큰 칸 이름은 usage_metadata와 같아서, 결과를 estimate_cost에 그대로 넘길 수 있습니다(캐시 입력 칸은 없음)
def sum_usage(messages):
    total = {"requests": 0, "input_tokens": 0, "output_tokens": 0}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            usage = message.usage_metadata
            total["requests"] = total["requests"] + 1
            total["input_tokens"] = total["input_tokens"] + usage["input_tokens"]
            total["output_tokens"] = total["output_tokens"] + usage["output_tokens"]
    return total


# Ch 6 06절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다
# 사용량 딕셔너리와 세 요금(100만 토큰당 달러)으로 요청 한 번의 예상 비용(달러)을 계산합니다
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


# Ch 20 01절에서 배웠습니다 — Ch 20 도구 파일 graph_tools.py의 같은 이름 함수를 옮겼습니다
# 메시지 목록에서 도구 호출 요청의 id 목록과 도구 메시지의 호출 ID 목록을 모아 내놓습니다
def call_id_lists(messages):
    lists = {"요청 id": [], "호출 ID": []}
    for message in messages:
        if type(message).__name__ == "AIMessage":
            for call in message.tool_calls:
                lists["요청 id"].append(call["id"])
        if type(message).__name__ == "ToolMessage":
            lists["호출 ID"].append(message.tool_call_id)
    return lists


# Ch 21 01절에서 배웠습니다 — 01절 노트북 10절의 같은 이름 함수를 옮겼습니다
# 에이전트 그래프 실행 결과 하나를 기록 한 줄(칸 넷을 담은 딕셔너리)로 만듭니다
# 모델 요청 수는 응답(AIMessage) 수이고, 첫 칸 이름표(question_name)는 질문 이름이나 설정 이름을 받습니다
def agent_row(question_name, result):
    ids = call_id_lists(result["messages"])
    usage = sum_usage(result["messages"])
    row = {"질문": question_name}
    row["모델 요청 수"] = usage["requests"]
    row["도구 메시지 수"] = len(ids["호출 ID"])
    row["호출 ID 짝"] = ids["요청 id"] == ids["호출 ID"]
    return row


# Ch 21 02절에서 배웠습니다 — 02절 노트북 6절의 같은 이름 함수를 옮겼습니다
# 에이전트 그래프 하나를 받아, 조건부 엣지마다 적은 노드·조건 함수 이름·갈 수 있는 곳을 한 줄씩 출력합니다(내놓는 값 없음)
def print_branches(graph_agent):
    branches = graph_agent.builder.branches
    for source in branches:
        specs = branches[source]
        for name in specs:
            # 속성 ends는 이름표와 갈 곳을 이은 딕셔너리라, 값만 모으면 갈 수 있는 곳입니다
            ends = list(specs[name].ends.values())
            print(source, "| 조건 함수:", name, "| 갈 수 있는 곳:", ends)


# Ch 5 02절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 두 벡터의 코사인 유사도(점곱을 두 길이의 곱으로 나눈 값)를 NumPy로 계산합니다
def cosine_similarity(first, second):
    first_array = np.array(first)
    second_array = np.array(second)
    # 기호 @는 두 배열의 점곱을, np.linalg.norm(배열)은 벡터의 길이를 계산합니다
    dot = first_array @ second_array
    length_product = np.linalg.norm(first_array) * np.linalg.norm(second_array)
    return dot / length_product


# Ch 12 01절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 코사인 유사도를 가장 큰 값 1에서 빼 코사인 거리(작을수록 가까움)로 바꿉니다
def cosine_distance(first, second):
    similarity_top = 1
    similarity = cosine_similarity(first, second)
    return similarity_top - similarity


# Ch 12 01절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 질문 벡터 하나를 문서 벡터 모두와 코사인 거리로 재어, 거리가 작은 순서로 앞 top_count개를 냅니다
# 거리는 소수 둘째 자리까지 남기고, 차례는 반올림하기 전 거리로 정합니다
def rank_by_distance(question_vector, doc_vectors, doc_ids, top_count):
    distances = []
    for doc_vector in doc_vectors:
        distances.append(cosine_distance(question_vector, doc_vector))
    hit_list = []
    # np.argsort(목록)는 값이 작은 것부터 그 자리 번호를 차례로 담은 배열을 냅니다
    for position in np.argsort(distances)[:top_count]:
        hit_list.append({"doc_id": doc_ids[position], "거리": round(distances[position], 2)})
    return hit_list


# Ch 12 05절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 순위 목록을 순위·문서 ID·값 세 칸으로 출력합니다(값 칸 이름을 인자로 받습니다)
def print_ranked(hit_list, value_name):
    print("순위 | 문서 ID |", value_name)
    for rank_number in range(len(hit_list)):
        row = hit_list[rank_number]
        print(rank_number + 1, "|", row["doc_id"], "|", row[value_name])


# Ch 14 06절에서 배웠습니다 — Ch 14 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 질문 하나를 벡터로 바꿔 거리 순위 목록(문서 ID와 거리)을 만듭니다(부를 때마다 임베딩 요청 1번)
# Ch 14 06절 노트북 판은 바깥 이름을 읽었고, 이 판은 임베딩 모델·문서 벡터·문서 ID·자를 개수를 인자로 받습니다
def search_hits(embedding_model, question, doc_vectors, doc_ids, top_count):
    question_vector = embedding_model.embed_query(question)
    hit_list = rank_by_distance(question_vector, doc_vectors, doc_ids, top_count)
    return hit_list


# Ch 11 01절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 고유 문서 목록에서 정답 문서 ID가 몇 번째 자리인지 찾습니다(찾지 못하면 0)
def find_gold_rank(doc_ids, gold_doc_ids):
    gold_rank = 0
    for position in range(len(doc_ids)):
        if doc_ids[position] in gold_doc_ids:
            gold_rank = position + 1
            break
    return gold_rank


# Ch 15 02절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 판정 머리글 뒤에 견줄 두 칸을 이름과 함께 이어 붙여 판정 요청 글 하나를 만듭니다
def build_judge_prompt(judge_head, pair, case):
    prompt_text = judge_head + "\n\n"
    for label in pair:
        field = pair[label]
        prompt_text = prompt_text + label + ":\n" + case[field] + "\n\n"
    return prompt_text


# Ch 15 02절에서 배웠습니다 — Ch 15 도구 파일 rag_tools.py의 같은 이름 함수를 옮겼습니다
# 판정 요청 글 하나를 평가 모델에 보내고 받은 JSON 글을 딕셔너리로 읽습니다
def judge_once(judge_model, prompt_text):
    reply = judge_model.invoke(prompt_text)
    verdict = json.loads(reply.text)
    return verdict
