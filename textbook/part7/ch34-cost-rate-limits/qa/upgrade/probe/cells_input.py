# 노트북 2절 셀과 같은 글(작성 뒤 author_02.py에 글자 그대로 옮기고, 입력 파일 바이트를 대조함)
INQUIRIES = r'''# 일괄 처리로 맡길 문의 글 다섯을 목록에 담습니다(첫째·셋째는 01절의 문의 글입니다)
inquiries = [
    "주문한 책이 일주일째 오지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "결제 창에서 카드 번호를 넣었는데 다음 단계로 넘어가지 않습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "받은 책이 찢어져 있어 돈을 되찾고 싶습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "주문한 책을 받을 주소를 회사로 바꾸고 싶습니다. 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
    "결제 수단을 카드에서 계좌 이체로 바꿀 수 있나요? 이 문의의 종류를 배송, 환불, 결제 가운데 한 낱말로 답하세요.",
]
print("문의 글 수:", len(inquiries))'''

NAMES = r'''# 요청마다 붙일 요청 이름표 다섯을, 문의 글과 같은 차례로 적습니다
request_names = ["inquiry-1", "inquiry-2", "inquiry-3", "inquiry-4", "inquiry-5"]
print("요청 이름표:", request_names)'''

SETTINGS = r'''# 요청 주소와, 요청 본문에 넣을 과정 표준 모델 설정을 정합니다(Ch 15 08절과 같은 값입니다)
url = "/v1/chat/completions"
settings = {"model": "gpt-5.4-mini", "temperature": 0, "reasoning_effort": "none"}
print("요청 주소:", url)
print("모델 설정:", settings)'''

THINKING = r'''# 둘째 문의에만 쓸 설정을 만듭니다: 생각하는 단계를 조금 쓰게 low로 바꾸고, temperature 0은 그대로 둡니다
thinking_settings = settings.copy()
thinking_settings["reasoning_effort"] = "low"
print("둘째 문의의 설정:", thinking_settings)'''

BUILD = r'''# 문의마다 요청 한 줄을 만듭니다(이름표 inquiry-2 줄만 바꾼 설정을 씁니다)
batch_lines = []
for number in range(len(inquiries)):
    line_settings = settings
    if request_names[number] == "inquiry-2":
        line_settings = thinking_settings
    batch_lines.append(make_batch_line(request_names[number], url, line_settings, inquiries[number]))
print("만든 요청 줄 수:", len(batch_lines))
print("둘째 줄의 요청 본문 설정:", batch_lines[1]["body"]["reasoning_effort"], batch_lines[1]["body"]["temperature"])'''

WRITE = r'''# 운영체제 임시 폴더에 새 폴더를 만들고, 요청 다섯 줄을 입력 파일로 씁니다(실습 폴더에는 쓰지 않습니다)
input_folder = tempfile.mkdtemp(prefix="ch34-02-")
input_path = os.path.join(input_folder, "batch-input.jsonl")
write_jsonl(input_path, batch_lines)
input_rows = read_jsonl(input_path)
print("다시 읽은 줄 수:", len(input_rows))
print("쓴 목록과 다시 읽은 목록이 같은가:", input_rows == batch_lines)
print("입력 파일의 크기(바이트):", os.path.getsize(input_path))'''

CELLS = [INQUIRIES, NAMES, SETTINGS, THINKING, BUILD, WRITE]

# Ch 15 08절 노트북 셀 글(make_batch_line·write_jsonl) — 도구 파일로 옮길 판과 같은 본문
TOOLS = r'''
import json

def make_batch_line(custom_id, url, settings, prompt_text):
    body = settings.copy()
    body["messages"] = [{"role": "user", "content": prompt_text}]
    line = {"custom_id": custom_id, "method": "POST", "url": url, "body": body}
    return line

def write_jsonl(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(json.dumps(line, ensure_ascii=False) + "\n")

def read_jsonl(file_path):
    with open(file_path, encoding="utf-8") as file:
        text_lines = file.read().split("\n")
    rows = []
    for text_line in text_lines:
        if text_line != "":
            rows.append(json.loads(text_line))
    return rows
'''


def build(namespace):
    import os
    import tempfile
    namespace["os"] = os
    namespace["tempfile"] = tempfile
    exec(TOOLS, namespace)
    for cell in CELLS:
        exec(cell, namespace)
    return namespace["input_path"]
