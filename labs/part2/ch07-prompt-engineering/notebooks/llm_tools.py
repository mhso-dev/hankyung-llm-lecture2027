"""Ch 7 프롬프트 엔지니어링 — 앞 절과 앞 챕터에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from llm_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(model, required_keys, allowed_labels 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
import json
import time


# Ch 6 06절에서 배웠습니다 — 모델 객체로 메시지 목록을 보내고, 응답 객체와 걸린 초를 튜플로 반환합니다
def timed_invoke(run_model, input_messages):
    start_time = time.perf_counter()
    run_response = run_model.invoke(input_messages)
    run_elapsed = time.perf_counter() - start_time
    return run_response, run_elapsed


# 01절에서 배웠습니다 — 조건 이름·응답 객체·걸린 초로 기록 한 줄(딕셔너리)을 만듭니다
def make_prompt_record(condition, run_response, run_elapsed):
    run_usage = run_response.usage_metadata
    record = {
        "조건": condition,
        "답": run_response.text,
        "입력 토큰 수": run_usage["input_tokens"],
        "출력 토큰 수": run_usage["output_tokens"],
        "끝난 이유": run_response.response_metadata["finish_reason"],
        "걸린 초": round(run_elapsed, 2),
    }
    return record


# 07절에서 배웠습니다 — 답 글을 JSON으로 읽어, 읽은 값과 읽기 결과(읽음·구문 오류)를 튜플로 반환합니다
def parse_json_answer(answer_text):
    parsed_value = None
    parse_result = "읽음"
    try:
        parsed_value = json.loads(answer_text)
    except json.JSONDecodeError:
        parse_result = "구문 오류"
    return parsed_value, parse_result


# 07절에서 배웠습니다 — 읽은 딕셔너리에 없는 키 이름을 목록으로 반환합니다
# 07절 판은 바깥 이름 required_keys를 읽었고, 이 판은 둘째 인자로 받습니다
def find_missing_keys(parsed_value, required_keys):
    missing_keys = []
    for key in required_keys:
        if key not in parsed_value:
            missing_keys.append(key)
    return missing_keys


# 07절에서 배웠습니다 — 필요한 키의 값이 글인지, category 값이 허용 이름인지 보고 문제 목록을 반환합니다
# 07절 판은 바깥 이름 required_keys·allowed_labels를 읽었고, 이 판은 두 목록을 인자로 받습니다
def find_value_problems(parsed_value, required_keys, allowed_labels):
    value_problems = []
    for key, key_value in parsed_value.items():
        if key in required_keys and type(key_value).__name__ != "str":
            value_problems.append(key + " 값이 글이 아님")
    if "category" in parsed_value and parsed_value["category"] not in allowed_labels:
        value_problems.append("category 값이 허용 이름 밖")
    return value_problems


# 07절에서 배웠습니다 — 세 함수로 답 글을 층마다 검사하고, 결과를 딕셔너리 한 줄로 반환합니다
# 07절 판은 인자가 답 글 하나였고, 이 판은 필요한 키 목록과 허용 이름 목록을 함께 받아 두 함수에 넘깁니다
def check_layers(answer_text, required_keys, allowed_labels):
    parsed_value, parse_result = parse_json_answer(answer_text)
    layer_record = {
        "JSON 읽기": parse_result,
        "값 종류": type(parsed_value).__name__,
        "없는 키": "검사 안 함",
        "값 규칙 문제": "검사 안 함",
    }
    if layer_record["값 종류"] == "dict":
        layer_record["없는 키"] = find_missing_keys(parsed_value, required_keys)
        layer_record["값 규칙 문제"] = find_value_problems(parsed_value, required_keys, allowed_labels)
    return layer_record
