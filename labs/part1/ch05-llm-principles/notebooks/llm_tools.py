"""Ch 5 LLM 동작 원리 — 앞 절에서 배운 함수를 모아 둔 도구 파일입니다.

뒤 절 노트북은 이 파일의 함수를 `from llm_tools import 함수이름` 한 줄로 가져와 씁니다.
노트북과 같은 폴더(notebooks/)에 두어야 가져올 수 있습니다.
함수마다 바로 위 주석에 어느 절에서 배웠는지 적었습니다.
노트북에서 만든 이름(model, tokenizer 등)을 함수 안에서 바로 읽지 않고, 필요한 값은 모두 인자로 받습니다.
"""
import numpy as np


# 03절에서 배웠습니다 — 점수 목록을 모두 0보다 크고 합이 1인 비중(확률)으로 바꿉니다
def softmax(scores):
    # np.exp()는 점수마다 e(약 2.718)를 그 점수만큼 거듭제곱한 배열을 반환합니다
    powers = np.exp(scores)
    # 거듭제곱을 모두 더한 값으로 나누면 합이 1이 됩니다
    return powers / powers.sum()


# 05절에서 배웠습니다 — 입력 글을 받아, 출력 몫 안에서 모델이 만든 새 조각만 글로 바꿔 반환합니다
# 05절 판은 바깥 이름 model·tokenizer·output_budget을 읽었고, 이 판은 세 값을 인자로 받습니다
def ask_model(model, tokenizer, input_text, output_budget):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    # do_sample=False는 다음 조각을 무작위로 뽑지 않는 설정입니다(05·06절)
    output_ids = model.generate(input_ids=input_ids, max_new_tokens=output_budget, do_sample=False)
    all_ids = output_ids[0].tolist()
    # 입력 조각 수만큼 건너뛴 뒤가 새 조각입니다
    input_length = len(input_ids[0])
    new_ids = all_ids[input_length:len(all_ids)]
    return tokenizer.decode(new_ids)


# 07절에서 배웠습니다 — 시스템 지시와 사용자 글을 채팅 템플릿으로 합친 입력 글을 반환합니다
# 07절 판은 바깥 이름 tokenizer를 읽었고, 이 판은 첫 인자로 받습니다
def make_input(tokenizer, system_text, user_text):
    message_list = []
    # 시스템 지시가 빈 글이 아닐 때만 시스템 메시지를 먼저 넣습니다
    if system_text != "":
        message_list.append({"role": "system", "content": system_text})
    message_list.append({"role": "user", "content": user_text})
    return tokenizer.apply_chat_template(message_list, tokenize=False, add_generation_prompt=True)


# 07절에서 배웠습니다 — 글에서 이어진 숫자 글자를 찾아, 숫자 글 목록으로 반환합니다
def find_numbers(text):
    numbers = []
    current = ""
    # 글 끝에 빈칸을 붙여, 마지막 숫자도 숫자가 아닌 글자를 만나게 합니다
    for letter in text + " ":
        if letter.isdigit():
            current = current + letter
        # 숫자가 끝난 자리에서 모은 숫자를 목록에 넣고 비웁니다
        elif current != "":
            numbers.append(current)
            current = ""
    return numbers


# 07절에서 배웠습니다 — 답의 숫자 가운데 기준 글에 없던 숫자(새 숫자)만 모아 반환합니다
def find_new_numbers(answer, source_text):
    source_numbers = find_numbers(source_text)
    new_numbers = []
    for number_text in find_numbers(answer):
        # 기준 글(질문이나 문서)에 없던 숫자만 모읍니다
        if number_text not in source_numbers:
            new_numbers.append(number_text)
    return new_numbers


# Ch 2 13절·Ch 4 06절에서 배웠습니다 — 기록장 딕셔너리의 칸을 한 줄에 하나씩 출력합니다
def print_report(report):
    # items()는 키와 값의 짝을 차례로 내놓습니다
    for key, value in report.items():
        print(key, "|", value)
