"""Create the eight independent Ch 5 notebooks from reviewed cell sources."""

from __future__ import annotations
# 사용 중지(2026-09-16, Ch05 검토 1차 C-1): 실행하면 개선본 _src·노트북을 개선 전 글로 덮어씁니다.
# 품질 개선본은 qa/upgrade/author_NN.py(노트북)와 textbook/_notebook/upgrade/mdpatch.py(설명 수정)로 고칩니다.
raise SystemExit("사용 중지: 개선 전 생성기입니다. textbook/part1/ch05-llm-principles/qa/upgrade/author_NN.py를 쓰세요.")

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("CH05_NOTEBOOK_OUT", HERE / "notebooks"))


def md(text: str) -> dict:
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code", "execution_count": None, "id": "", "metadata": {},
        "outputs": [], "source": text.splitlines(keepends=True),
    }


def notebook(title: str, question: str, cells: list[dict]) -> dict:
    all_cells = [md(f"# {title}\n\n{question}\n\nPython 3.12와 잠긴 패키지를 사용합니다. 첫 실행에서는 로컬 모델을 다운로드합니다.")] + cells
    for i, cell in enumerate(all_cells, 1):
        cell["id"] = f"cell-{i:02d}"
    return {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "lesson_format": "experiment",
        },
        "nbformat": 4, "nbformat_minor": 5,
    }


TOKEN_SETUP = '''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
from transformers import AutoTokenizer

# 모델 ID와 고정 revision에 맞는 두 토큰화기를 로컬에 받아 사용합니다.
gpt2 = AutoTokenizer.from_pretrained("openai-community/gpt2", revision="607a30d783dfa663caf39e06633721c8d4cfcd7e")
ko_tokenizer = AutoTokenizer.from_pretrained("klue/bert-base", revision="77c8b3d707df785034b4e50f2da5d37be5f0f546")
print("GPT-2 어휘 크기:", gpt2.vocab_size)
print("KLUE BERT 어휘 크기:", ko_tokenizer.vocab_size)'''

GEN_SETUP = '''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, logging, set_seed

logging.set_verbosity_error()

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=REVISION)
model.eval()
print("model:", MODEL_ID)
print("parameters:", f"{model.num_parameters():,}")'''

GEN_FN = '''def generate(prompt: str, *, temperature: float = 0.7, seed: int = 0, max_new_tokens: int = 48) -> str:
    # 채팅 템플릿을 적용한 뒤 새로 생성된 토큰만 복원합니다.
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt")
    set_seed(seed)
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            top_p=0.9 if temperature > 0 else None,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = output[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()'''

GEN_SETUP_DETERMINISTIC = '''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, logging

logging.set_verbosity_error()

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=REVISION)
model.eval()
print("model:", MODEL_ID)
print("parameters:", f"{model.num_parameters():,}")'''

GEN_FN_DETERMINISTIC = '''def generate(prompt: str, *, max_new_tokens: int = 48) -> str:
    # 샘플링을 끈 결정적 생성으로 새 토큰만 복원합니다.
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = output[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()'''


lessons = {
"01-토큰화와-한국어-효율": notebook("토큰화와 한국어 효율", "같은 뜻을 담은 한국어와 영어 문장은 토큰화 방식에 따라 몇 개의 토큰이 될까요?", [
    md("## 두 토큰화기 준비\n\n어휘와 분할 규칙이 다른 두 토큰화기를 준비합니다."), code(TOKEN_SETUP),
    md("## Ch 4 파싱 텍스트 읽기\n\nCh 4의 HTML에서 추출해 보존한 기사 텍스트와 출처 필드를 읽습니다."),
    code('''import json
from pathlib import Path

search_paths = [Path.cwd()]
for parent in Path.cwd().parents:
    search_paths.append(parent)

root = None
for path in search_paths:
    candidate = path / "labs/part1/ch04-data-tools/data/article-text.json"
    if candidate.exists():
        root = path
        break
if root is None:
    raise FileNotFoundError("Ch 4 article-text.json을 찾지 못했습니다.")
handoff_path = root / "labs/part1/ch04-data-tools/data/article-text.json"
handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
article_text = handoff["record"]["text"]
print("schema:", handoff["schema_version"])
print("source:", handoff["source"])
print("article:", handoff["record"]["id"], repr(article_text))
print("GPT-2:", len(gpt2.encode(article_text)), "| KLUE:", len(ko_tokenizer.tokenize(article_text)))'''),
    md("## 한·영 문장 비교\n\n뜻이 같은 짧은 문장의 토큰 수와 분할 결과를 그대로 출력합니다."),
    code('''pairs = [
    ("오늘 주문 상태를 확인해 주세요.", "Please check today's order status."),
    ("환불 기준은 결제일로부터 7일입니다.", "The refund period is seven days from payment."),
]
for korean, english in pairs:
    print("\\nKorean:", korean)
    print(" GPT-2:", len(gpt2.encode(korean)), gpt2.tokenize(korean))
    print(" KLUE :", len(ko_tokenizer.tokenize(korean)), ko_tokenizer.tokenize(korean))
    print("English:", english)
    print(" GPT-2:", len(gpt2.encode(english)), gpt2.tokenize(english))
    print(" KLUE :", len(ko_tokenizer.tokenize(english)), ko_tokenizer.tokenize(english))'''),
    md("## 문장 길이와 토큰 수\n\n문장 길이가 배로 늘어나면 토큰 수도 정확히 배가 되는지 확인합니다."),
    code('''base = "한국어 토큰 효율을 측정합니다."
for repeat in [1, 2, 4, 8]:
    text = " ".join([base] * repeat)
    print(repeat, "문장 | 문자", len(text), "| GPT-2", len(gpt2.encode(text)), "| KLUE", len(ko_tokenizer.tokenize(text)))'''),
]),
"02-임베딩과-의미-유사도": notebook("임베딩과 의미 유사도", "단어가 다르더라도 뜻이 비슷한 문장을 숫자로 비교할 수 있을까요?", [
    md("## 다국어 문장 임베딩\n\n문장을 384개 숫자로 바꾸는 로컬 모델을 불러옵니다."),
    code('''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_ID, revision="e8f8c211226b894fcb81acc59f3b34ba3efd5f42")
sentences = [
    "주문한 상품을 취소하고 싶습니다.",
    "구매를 취소하려면 어떻게 하나요?",
    "내일 서울은 비가 옵니다.",
    "I want to cancel my order.",
]
vectors = model.encode(sentences, normalize_embeddings=True)
print("shape:", vectors.shape)
print("첫 문장 앞 5개 값:", np.round(vectors[0, :5], 4))'''),
    md("## 코사인 유사도 비교\n\n정규화된 벡터의 점곱은 코사인 유사도와 같습니다."),
    code('''scores = vectors @ vectors.T
for i in range(1, len(sentences)):
    print(f"0 vs {i}: {scores[0, i]:.4f} | {sentences[i]}")
nearest = np.argsort(-scores[0])[1:]
print("\\n유사도 순서:", nearest.tolist())'''),
    md("## 단어 하나 바꾸기\n\n'취소'를 '반품'으로 바꿔 유사도가 어떻게 달라지는지 봅니다."),
    code('''changed = model.encode(["주문한 상품을 반품하고 싶습니다."], normalize_embeddings=True)[0]
print("취소 문장 vs 반품 문장:", round(float(vectors[0] @ changed), 4))
print("취소 문장 vs 날씨 문장:", round(float(vectors[0] @ vectors[2]), 4))'''),
]),
"03-어텐션-직관": notebook("어텐션 직관", "모델은 다음 토큰을 예측할 때 입력의 어느 부분을 관련 있다고 볼까요?", [
    md("## 교재용 가중 평균\n\n아래 여섯 조각은 실제 tokenizer의 출력이 아니라 설명을 위해 토큰이라고 가정한 조각입니다. 가중치도 실제 모델의 어텐션 값이 아니며, 질문 대상과 색상 표현에 더 큰 비중을 두는 모습을 보이려고 정했습니다. `zip(tokens, weights_for_b)`는 같은 위치의 토큰과 가중치를 한 쌍씩 반환합니다. 출력의 `{token:12}`는 토큰을 12칸에 맞추고, `{weight:.2f}`는 가중치를 소수점 둘째 자리까지 표시합니다. `int(weight * 20)`은 가중치를 막대 칸 수로 바꿉니다."),
    code('''tokens = ["상품", "A는", "파란색이고", "상품", "B는", "빨간색입니다."]
weights_for_b = [0.05, 0.05, 0.05, 0.10, 0.30, 0.45]
print("질문: 상품 B의 색은?")
for token, weight in zip(tokens, weights_for_b):
    print(f"{token:12} {weight:.2f} " + "■" * int(weight * 20))
print("합계:", sum(weights_for_b))'''),
    md("## 질문이 바뀌면 비중도 바뀝니다\n\n같은 문장에서 상품 A를 물으면 교재용 비중을 다르게 둡니다."),
    code('''weights_for_a = [0.10, 0.30, 0.45, 0.05, 0.05, 0.05]
for token, before, after in zip(tokens, weights_for_b, weights_for_a):
    print(f"{token:12} B질문={before:.2f} A질문={after:.2f}")
print("이 비교는 개념 설명용이며 실제 모델을 측정하지 않았습니다.")'''),
]),
"04-컨텍스트-윈도": notebook("컨텍스트 윈도", "모델에 넣을 수 있는 토큰 예산은 입력과 출력 사이에서 어떻게 나눌까요?", [
    md("## 입력 토큰 세기\n\nQwen2.5 로컬 토큰화기로 시스템 지시, 문서, 질문을 함께 세어 봅니다."),
    code('''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
from transformers import AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision="7ae557604adf67be50417f59c2c2f167def9a775")
parts = {
    "시스템": "주어진 문서 범위에서만 답하세요.",
    "문서": "환불은 결제일로부터 7일 이내에 신청합니다. " * 20,
    "질문": "환불은 며칠 이내에 신청하나요?",
}


counts = {}
for name, text in parts.items():
    counts[name] = len(tokenizer.encode(text))
print(counts)
print("raw 텍스트 합계:", sum(counts.values()))
messages = [
    {"role": "system", "content": parts["시스템"]},
    {"role": "user", "content": parts["문서"] + "\\n\\n" + parts["질문"]},
]
actual_input = len(tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))
print("채팅 템플릿 적용 입력:", actual_input)'''),
    md("## 출력 공간 예약\n\n실습용 작은 한도를 정하고 출력에 남겨 둘 토큰을 계산합니다."),
    code('''window = 512
for output_budget in [32, 64, 128]:
    input_budget = window - output_budget
    remaining = input_budget - actual_input
    print(f"출력 {output_budget:3}개 예약 -> 입력 한도 {input_budget:3}개, 남은 입력 {remaining:3}개")'''),
    md("## 문서 길이 비교\n\n동일한 문장을 늘려 언제 실습용 한도를 넘는지 관찰합니다."),
    code('''full_counts = {}
for repeat in [10, 20, 40, 80]:
    document = "환불은 결제일로부터 7일 이내에 신청합니다. " * repeat
    messages = [
        {"role": "system", "content": parts["시스템"]},
        {"role": "user", "content": document + "\\n\\n" + parts["질문"]},
    ]
    used = len(tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))
    full_counts[repeat] = used
    print(repeat, "반복:", used, "토큰 | 448 이하:", used <= 448)'''),
]),
"05-컨텍스트-로트": notebook("컨텍스트 로트", "근거 문장의 위치와 주변 문장 수가 답에 어떤 차이를 만들까요?", [
    md("## 로컬 생성 모델 준비"), code(GEN_SETUP_DETERMINISTIC), code(GEN_FN_DETERMINISTIC),
    md("## 비교 조건 준비\n\n질문과 정답 기준은 고정하고, 무관한 문장 수와 근거 위치를 조합한 아홉 개의 프롬프트를 만듭니다."),
    code('''fact = "해바라기 작전의 확인 코드는 314159입니다."
filler = "주문 조회 화면에는 결제 상태와 배송 상태가 표시됩니다."
question = "해바라기 작전의 확인 코드만 답하세요."
model_limit = model.config.max_position_embeddings
max_new_tokens = 20
print("model max_position_embeddings:", model_limit)
conditions = []
for repeats in [2, 20, 60]:
    for position in ["start", "middle", "end"]:
        items = [filler] * repeats
        index = {"start": 0, "middle": repeats // 2, "end": repeats}[position]
        items.insert(index, fact)
        prompt = "\\n".join(items) + "\\n\\n" + question
        conditions.append((repeats, position, prompt))'''),
    md("## 아홉 조건 실행\n\n각 프롬프트를 같은 결정적 생성 방식으로 두 번 호출합니다. 두 번은 확률 표본이 아니라 같은 설정에서 출력이 반복되는지 확인하는 실행 횟수입니다."),
    code('''observations = []
for repeats, position, prompt in conditions:
    outputs = []
    for _ in [1, 2]:
        output = generate(prompt, max_new_tokens=max_new_tokens)
        outputs.append(output)
    hits = 0
    for output in outputs:
        if "314159" in output:
            hits += 1
    messages = [{"role": "user", "content": prompt}]
    templated = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    tokens = len(tokenizer.encode(templated))
    fits = tokens + max_new_tokens <= model_limit
    observations.append({"repeats": repeats, "position": position, "tokens": tokens, "outputs": outputs})
    print(f"filler={repeats:2} position={position:6} tokens={tokens:4} + output={max_new_tokens} <= {model_limit}: {fits} hits={hits}/2 outputs={outputs}")'''),
]),
"06-temperature와-샘플링": notebook("temperature와 샘플링", "같은 프롬프트에서 temperature를 바꾸면 반복 출력의 다양성이 어떻게 달라질까요?", [
    md("## 로컬 생성 모델 준비"), code(GEN_SETUP), code(GEN_FN),
    md("## temperature별 반복 생성\n\n프롬프트, top-p, 최대 생성 길이를 고정하고 temperature와 난수 시드를 바꾸어 실제 출력을 모두 보존합니다."),
    code('''prompt = "오프라인 서점의 가을 행사 이름을 한국어 5어절 이내로 하나 제안하세요."
records = []
for temperature in [0.3, 1.0]:
    for seed in [11, 22, 33]:
        answer = generate(prompt, temperature=temperature, seed=seed, max_new_tokens=24)
        records.append((temperature, seed, answer))
        print(f"T={temperature:.1f} seed={seed}: {answer}")'''),
    md("## 서로 다른 출력 수\n\n문자열이 정확히 같은지만 세어, 표현의 다양성을 제한적으로 관찰합니다."),
    code('''for temperature in [0.3, 1.0]:
    answers = []
    for recorded_temperature, _, answer in records:
        if recorded_temperature == temperature:
            answers.append(answer)
    print(f"T={temperature:.1f} unique={len(set(answers))}/3")
print("문자열 종류 수는 제안의 품질이나 창의성을 직접 측정하지 않습니다.")'''),
]),
"07-환각의-구조적-원인": notebook("환각의 구조적 원인", "모델이 알지 못하는 고유 사실을 물었을 때, 왜 그럴듯한 문장을 이어 말할 수 있을까요?", [
    md("## 로컬 생성 모델 준비"), code(GEN_SETUP), code(GEN_FN),
    md("## 근거가 없는 고유 정보 질문\n\n실습을 위해 만든 기관과 정책을 묻습니다. 질문 문장에는 정답 근거가 없습니다."),
    code('''questions = [
    "2026년 가상 기관 '해바라기 연구소'의 초록 패스 제도 지원금은 얼마인가요?",
    "가상 제품 '노을 워커 3'의 배터리 용량은 몇 mAh인가요?",
]
without_context = []
for question in questions:
    print("Q:", question)
    answer = generate(question, temperature=0, max_new_tokens=64)
    without_context.append(answer)
    print("A:", answer)'''),
    md("## 답변 제약을 추가한 비교\n\n정보가 주어지지 않으면 알 수 없다고 답하도록 제약을 추가합니다. 이 제약이 항상 정확한 답을 보장하지는 않습니다."),
    code('''instruction = "주어진 질문에 정답 근거가 없으면 추측하지 말고 '제공된 정보로는 확인할 수 없습니다'라고 답하세요.\\n\\n"
with_constraint = []
for question in questions:
    print("Q:", question)
    answer = generate(instruction + question, temperature=0, max_new_tokens=64)
    with_constraint.append(answer)
    print("A:", answer)'''),
]),
"08-모델-선택-기준": notebook("모델 선택 기준", "정확도, 속도, 메모리, 라이선스 조건이 다를 때 어떻게 모델 후보를 비교할까요?", [
    md("## 비교표 만들기\n\n아래 값은 본 실습에서 사용한 모델 카드의 공개 정보와 현재 환경의 파라미터 수입니다."),
    code('''import warnings
warnings.filterwarnings("ignore", message="IProgress not found")
from transformers import AutoModelForCausalLM, AutoTokenizer

candidates = [
    {"id": "Qwen/Qwen2.5-0.5B-Instruct", "task": "text-generation", "license": "apache-2.0"},
    {"id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "task": "sentence-similarity", "license": "apache-2.0"},
    {"id": "klue/bert-base", "task": "fill-mask", "license": "CC-BY-SA-4.0"},
]
for item in candidates:
    print(item)'''),
    md("## 현재 환경에서 실행 가능성 확인\n\n생성 모델을 로드하여 파라미터 수와 토큰화 시간을 측정합니다. 이 시간은 현재 컴퓨터의 캐시 상태에만 해당합니다."),
    code('''import time
model_id = candidates[0]["id"]
revision = "7ae557604adf67be50417f59c2c2f167def9a775"
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
start = time.perf_counter()
model = AutoModelForCausalLM.from_pretrained(model_id, revision=revision)
load_seconds = time.perf_counter() - start
text = "한국어 문장을 토큰화합니다. " * 100
start = time.perf_counter()
ids = tokenizer.encode(text)
tokenize_ms = (time.perf_counter() - start) * 1000
print("parameters:", f"{model.num_parameters():,}")
print("cached load seconds:", round(load_seconds, 3))
print("tokenize:", len(ids), "tokens in", round(tokenize_ms, 3), "ms")'''),
    md("## 필수 조건으로 후보 거르기\n\n`for item in candidates`는 후보 사전을 하나씩 `item`에 넣습니다. 두 비교 결과를 `task_matches`와 `license_matches`에 참 또는 거짓으로 저장하고, `and`로 둘 다 참인지 확인합니다. 조건을 만족하면 `eligible.append(item)`이 그 후보를 결과 목록 끝에 추가합니다. 자체 질의셋은 서비스에서 실제로 들어올 대표 질문과 질문별 정답 기준을 함께 모은 평가 자료를 뜻합니다."),
    code('''required_task = "text-generation"
required_license = "apache-2.0"
eligible = []
for item in candidates:
    task_matches = item["task"] == required_task
    license_matches = item["license"] == required_license
    if task_matches and license_matches:
        eligible.append(item)
print("eligible:", eligible)
print("선택 전에는 실제 대표 질문과 정답 기준으로 품질과 속도를 추가 측정해야 합니다.")'''),
]),
}


NOTEBOOK_GUIDANCE = {
    "01-토큰화와-한국어-효율": {
        "## 두 토큰화기 준비": """## 두 토큰화기 준비

`AutoTokenizer.from_pretrained(model_id, revision=...)`는 모델 ID와 고정 revision을 입력받아 해당 파일을 불러오고 tokenizer 객체를 반환합니다. revision은 같은 이름의 모델 파일이 나중에 바뀌어도 이 실습에서 확인한 버전을 다시 받기 위한 식별자입니다. `vocab_size`는 tokenizer 어휘에 등록된 토큰 ID 개수를 정수로 반환합니다. 어휘 크기가 크다는 사실만으로 한국어가 더 적은 토큰으로 나뉜다고 판단할 수는 없습니다.

토큰화기의 입력은 사람이 읽는 문자열입니다. `tokenize(text)`는 토큰 문자열 목록을, `encode(text)`는 토큰 ID의 정수 목록을 반환합니다. 반환은 함수가 계산한 값을 호출한 코드에 넘긴다는 뜻입니다. 아래 셀은 두 tokenizer 객체와 각각의 어휘 크기를 출력합니다.""",
        "## 한·영 문장 비교": """## 한·영 문장 비교

같은 문장 쌍을 두 토큰화기의 `encode()`와 `tokenize()`에 입력합니다. `len()`은 반환된 목록의 항목 수를 셉니다. 출력은 `언어 → 토큰 수 → 실제 조각 목록` 순서입니다. 먼저 한국어 첫 문장이 GPT-2에서 몇 조각으로 나뉘는지 읽고, 같은 문장의 KLUE 결과와 비교합니다.""",
        "## Ch 4 파싱 텍스트 읽기": """## Ch 4 파싱 텍스트 읽기

현재 작업 폴더를 `search_paths` 목록에 먼저 넣고, 부모 폴더를 하나씩 순회하며 `append()`로 추가합니다. 다음 `for` 반복문은 이 목록에서 Ch 4 파일이 있는 경로를 찾습니다. 파일을 찾으면 `break`로 탐색을 마치고, 끝까지 찾지 못하면 오류를 발생시킵니다. 찾은 JSON의 기사 문자열을 두 토큰화기에 입력합니다.""",
    },
    "02-임베딩과-의미-유사도": {
        "## 다국어 문장 임베딩": """## 다국어 문장 임베딩

벡터는 순서가 있는 숫자 목록입니다. 문장 네 개가 **입력**입니다. `model.encode()`는 각 문장을 384개의 실수로 바꾸어 NumPy 배열로 **반환**합니다. `shape`의 `(4, 384)`는 4개 행이 문장 네 개에, 384개 열이 각 문장의 숫자 표현에 대응한다는 뜻입니다. `vectors[0, :5]`는 구조를 확인하려고 첫 문장의 앞 다섯 값만 고릅니다.""",
        "## 코사인 유사도 비교": """## 코사인 유사도 비교

실제 문장 벡터는 길이 1로 정규화되어 있습니다. `vectors.T`는 행과 열을 바꾸고, `@`는 행렬 곱을 수행합니다. 따라서 `vectors @ vectors.T`는 모든 문장 쌍의 점곱, 곧 코사인 유사도를 4×4 배열로 반환합니다. 0번 문장을 자기 자신과 비교한 값도 1이므로 후보 순서를 만들 때는 0번을 명시적으로 제외합니다. `np.argsort(-scores[0])`는 0번 행의 유사도를 큰 값부터 정렬한 인덱스를 반환하고, 뒤의 `[1:]`이 첫 인덱스 0을 제외합니다. `nearest`는 NumPy 배열이며 `nearest.tolist()`는 출력하기 쉬운 Python 목록으로 변환합니다. 출력의 `0 vs i`는 항상 0번 취소 문장을 기준으로 읽습니다.""",
    },
    "03-어텐션-직관": {
        "## 교재용 가중 평균": """## 교재용 가중치 읽기

**입력**은 설명을 위해 토큰이라고 가정한 문자열 목록과 같은 길이의 비중 목록입니다. `zip()`은 같은 위치의 토큰과 비중을 한 쌍씩 반환합니다. `{token:12}`는 토큰을 12칸에 맞추고 `{weight:.2f}`는 비중을 소수점 둘째 자리까지 표시합니다. `"■" * int(weight * 20)`은 비중을 막대 칸 수로 바꿉니다. `sum()`은 비중의 합을 반환합니다. 이 값은 실제 모델에서 추출한 어텐션이 아니라 가중치를 읽는 법을 익히는 교재용 예입니다.""",
        "## 질문이 바뀌면 비중도 바뀝니다": """## 질문이 바뀌면 비중도 바뀝니다

문장 토큰은 그대로 두고 질문 대상을 B에서 A로 바꾼 상황을 나타냅니다. 처리 조건이 바뀌면 큰 비중의 위치도 바뀐다는 점을 두 열에서 비교합니다. 이 셀의 화면 출력으로 실제 Qwen의 답이나 내부 어텐션을 설명할 수는 없습니다.""",
    },
    "04-컨텍스트-윈도": {
        "## 입력 토큰 세기": """## 입력 토큰 세기

시스템 지시, 문서, 질문 문자열이 **입력**입니다. `parts`는 이 세 문자열을 이름과 본문으로 묶은 사전입니다. `messages`는 `role`과 `content`를 가진 사전의 목록이며, `system` 역할에는 지시를, `user` 역할에는 문서와 질문을 넣습니다. `encode()`는 각 문자열의 토큰 ID 목록을 반환합니다. `apply_chat_template(..., tokenize=True, add_generation_prompt=True)`는 역할 표시와 모델이 답을 시작할 표시까지 추가한 토큰 ID 목록을 반환합니다. 출력의 원시 텍스트 합계와 채팅 템플릿 적용 입력을 비교합니다.""",
        "## 출력 공간 예약": """## 출력 공간 예약

512는 계산 구조를 보기 위한 실습용 전체 한도입니다. 처리식 `input_budget = window - output_budget`은 출력에 남긴 수를 전체에서 빼고 입력 한도를 반환합니다. 각 출력 줄에서 예약한 출력 수, 계산된 입력 한도, 현재 입력을 넣고 남은 수를 차례로 읽습니다. 음수는 현재 입력이 한도를 초과했다는 뜻입니다.""",
    },
    "05-컨텍스트-로트": {
        "## 로컬 생성 모델 준비": """## 로컬 생성 모델 준비

고정 revision의 사전학습 모델과 tokenizer를 로컬에서 불러옵니다. `generate()`는 프롬프트 문자열과 최대 생성 토큰 수를 입력받습니다. 모델은 샘플링을 끈 같은 생성 방식으로 새 토큰 ID를 만들고, 함수는 새 부분만 문자열로 복원해 반환합니다. 모델 구조를 구현하거나 학습하는 셀이 아닙니다.""",
        "## 비교 조건 준비": """## 비교 조건 준비

`model.config.max_position_embeddings`가 반환한 모델의 위치 한도를 출력합니다. 정답 근거와 질문은 고정하고 무관한 문장 수를 2·20·60개로, 근거 위치를 시작·중간·끝으로 바꿉니다. 이 조합으로 아홉 개의 프롬프트를 만들어 `conditions` 목록에 추가합니다.""",
        "## 아홉 조건 실행": """## 아홉 조건 실행

준비한 프롬프트를 같은 결정적 생성 방식으로 두 번씩 호출합니다. `for _ in [1, 2]`의 밑줄은 실행 횟수 값 자체를 이후 계산에 사용하지 않는다는 뜻입니다. 각 조건에서 `입력 토큰 수 + 최대 생성 20토큰`이 한도 이하인지 검사하고, 반환 문자열에 `314159`가 있으면 적중으로 셉니다. `hits=0/2`는 두 실행 모두 코드 문자열을 출력하지 않았다는 뜻이며 모델 전체의 실패율을 뜻하지 않습니다.""",
    },
    "06-temperature와-샘플링": {
        "## 로컬 생성 모델 준비": """## 로컬 생성 모델 준비

고정 revision의 사전학습 모델을 불러옵니다. `AutoTokenizer.from_pretrained()`는 문자열과 토큰 ID를 서로 바꾸는 tokenizer 객체를 반환하고, `AutoModelForCausalLM.from_pretrained()`는 다음 토큰을 생성하는 모델 객체를 반환합니다. 두 객체를 준비한 뒤 로짓과 확률의 관계부터 확인합니다.""",
        "## temperature별 반복 생성": """## temperature별 반복 생성

프롬프트, top-p, 최대 생성 길이와 시드 세 개는 고정하고 temperature만 0.3과 1.0으로 바꿉니다. 각 줄은 `temperature → seed → 반환 문자열` 순서입니다. 같은 시드끼리 두 temperature 결과를 대응해 읽은 뒤, 세 번 전체의 문자열 차이를 확인합니다.""",
    },
    "07-환각의-구조적-원인": {
        "## 로컬 생성 모델 준비": """## 로컬 생성 모델 준비

사전학습 모델은 학습이 끝난 파라미터를 저장해 둔 모델입니다. 이 노트북은 모델을 새로 학습하거나 내부 구조를 구현하지 않습니다. 질문 문자열을 입력하고 모델이 반환한 답변 문자열에서 근거가 필요한 주장을 찾습니다.""",
        "## 근거가 없는 고유 정보 질문": """## 근거가 없는 고유 정보 질문

입력은 실습을 위해 만든 기관·제도와 제품에 관한 두 질문입니다. 정답 자료는 제공하지 않습니다. 각 반환 문자열에서 금액·날짜·절차·제품 사양처럼 외부 확인이 필요한 주장을 먼저 표시하고, 입력에 그 근거가 있었는지 확인합니다. 자연스러운 문장인지 여부는 사실 판정 기준이 아닙니다.""",
    },
    "08-모델-선택-기준": {
        "## 비교표 만들기": """## 비교표 만들기

**입력**은 모델 ID, 대표 작업, 라이선스를 담은 사전 세 개입니다. `task`는 실습에서 사용할 입력·출력 목적이고 `license`는 모델 카드에 표시된 사용 조건입니다. 이 셀은 후보 정보를 한 줄씩 출력할 뿐 성능을 비교하지 않습니다.""",
        "## 현재 환경에서 실행 가능성 확인": """## 현재 환경에서 실행 가능성 확인

`AutoTokenizer.from_pretrained()`는 모델 ID에 맞는 tokenizer 객체를 반환하고, `AutoModelForCausalLM.from_pretrained()`는 다음 토큰 생성용 모델 객체를 반환합니다. `num_parameters()`는 파라미터 수를 정수로 반환합니다. 출력의 로딩 시간과 토큰화 시간은 현재 캐시와 CPU에서 측정한 값이며 생성 답변의 지연시간이 아닙니다.""",
        "## 필수 조건으로 후보 거르기": """## 필수 조건으로 후보 거르기

생성 작업과 Apache-2.0을 필수 조건으로 입력합니다. 빈 목록 `eligible`을 만든 뒤 `for` 반복문이 후보 사전을 하나씩 꺼냅니다. 작업 일치 여부와 라이선스 일치 여부를 각각 불리언 값으로 계산하고, 두 값이 모두 `True`일 때만 `append()`로 후보를 목록 끝에 추가합니다. 반복이 끝나면 `eligible`에는 두 조건을 모두 통과한 사전만 남습니다. 후보 하나가 남았다는 사실은 그 후보가 가장 정확하다는 뜻이 아닙니다.""",
    },
}

for slug, heading_map in NOTEBOOK_GUIDANCE.items():
    for cell in lessons[slug]["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        heading = "".join(cell["source"]).splitlines()[0]
        if heading in heading_map:
            cell["source"] = heading_map[heading].splitlines(keepends=True)

# 02절은 NumPy와 점곱을 선수 지식으로 가정하지 않습니다. 실제 384차원 벡터를
# 비교하기 전에 두 숫자 벡터로 shape, 정규화, 전치, @ 연산을 확인합니다.
toy_cells = [
    md("""## 두 숫자 벡터로 표기 읽기

벡터는 순서가 있는 숫자 목록입니다. `[3, 4]`와 `[4, 3]`을 두 행으로 담습니다. `shape`는 행과 열의 수를 반환합니다. `axis=1`은 열 방향으로 각 행의 값을 묶어 벡터마다 길이 하나를 계산하라는 뜻입니다. `keepdims=True`는 결과를 `(2,)`가 아닌 `(2, 1)` 열 모양으로 유지하여 각 행을 자기 길이로 나눌 수 있게 합니다. `ravel()`은 출력할 때 이 열 모양을 1차원 `[5, 5]`로 펼칩니다. 각 행을 길이로 나눈 뒤 `T`로 행과 열을 바꾸고 `@`를 적용하면 모든 행 쌍의 점곱 표가 반환됩니다."""),
    code('''import numpy as np

toy = np.array([[3.0, 4.0], [4.0, 3.0]])
lengths = np.linalg.norm(toy, axis=1, keepdims=True)
normalized_toy = toy / lengths
toy_scores = normalized_toy @ normalized_toy.T
print("shape:", toy.shape)
print("lengths:", lengths.ravel())
print("normalized:\\n", normalized_toy)
print("cosine table:\\n", toy_scores)'''),
]
lessons["02-임베딩과-의미-유사도"]["cells"][1:1] = toy_cells

# 로짓과 확률을 생성 API에 숨겨 둔 채 temperature만 사용하지 않도록 작은 숫자로
# 변환 과정을 먼저 관찰합니다. 이는 Transformer 구현이 아니라 출력 설정 읽기입니다.
logit_cells = [
    md("""## 로짓을 확률로 바꾸기

로짓은 모델이 다음 토큰 후보마다 계산한 변환 전 점수입니다. 아래의 세 값은 설명을 위해 정한 예이며 실제 Qwen에서 추출한 값이 아닙니다. `torch.tensor([2.0, 1.0, 0.0])`는 세 후보 점수를 담은 1차원 PyTorch 숫자 배열을 만듭니다. `dim=0`은 이 1차원 배열의 후보 축 전체에 softmax를 적용한다는 뜻입니다. 로짓을 temperature로 나눈 뒤 softmax를 적용하면 합이 1인 확률이 반환됩니다. 두 출력에서 가장 큰 후보는 유지되는지, 후보 사이의 확률 차이는 어떻게 달라지는지 읽습니다."""),
    code('''toy_logits = torch.tensor([2.0, 1.0, 0.0])
for temperature in [0.5, 1.0]:
    probabilities = torch.softmax(toy_logits / temperature, dim=0)
    rounded = []
    for probability in probabilities.tolist():
        rounded.append(round(probability, 4))
    print(f"T={temperature:.1f} probabilities:", rounded)
    print("합계:", round(float(probabilities.sum()), 4))'''),
]
generate_explanation = md("""## 생성 도우미의 입력과 반환

`generate()`는 프롬프트 문자열, temperature, 난수 시드, 최대 생성 토큰 수를 입력받고 새로 생성된 답변 문자열을 반환합니다. `messages`는 사용자 역할과 프롬프트를 묶습니다. `apply_chat_template(..., tokenize=False)`는 역할 표시가 포함된 문자열을 반환하고, tokenizer의 `return_tensors="pt"`는 모델에 전달할 PyTorch 텐서를 반환합니다.

`set_seed()`는 난수 시작 상태를 정합니다. `model.generate()`는 입력 텐서와 생성 옵션을 호출 시점에 받아 새 토큰 ID를 만듭니다. `do_sample`은 temperature가 0보다 클 때만 샘플링을 켭니다. 이 실습은 샘플링 조건에서 `top_p=0.9`를 고정합니다. `pad_token_id`는 길이를 맞추는 패딩 위치에 종료 토큰 ID를 사용하도록 지정합니다.

모델 반환값에는 입력 ID와 새 출력 ID가 함께 있습니다. `output[0, inputs["input_ids"].shape[1]:]`는 입력 길이까지를 제외하고 새 ID만 고릅니다. `decode(..., skip_special_tokens=True)`는 특수 토큰 표시를 빼고 문자열로 바꾸며, `strip()`은 문자열 양끝의 공백을 제거합니다.""")
lessons["06-temperature와-샘플링"]["cells"][3:3] = [*logit_cells, generate_explanation]

VALIDATIONS = {
    "01-토큰화와-한국어-효율": 'assert root is not None and handoff_path.exists()\nassert handoff["schema_version"] == "ch04-parsed-article-v1"\nassert handoff["record"]["id"] == "A10" and article_text == handoff["record"]["text"]\nassert len(gpt2.encode(pairs[0][0])) > len(ko_tokenizer.encode(pairs[0][0], add_special_tokens=False))\nassert len(gpt2.encode(base)) > 0\nprint("검증: Ch 4 파싱 텍스트와 두 토큰화기의 한·영 문장 분할을 확인했습니다.")',
    "02-임베딩과-의미-유사도": 'assert toy.shape == (2, 2) and np.allclose(lengths.ravel(), [5.0, 5.0])\nassert np.allclose(np.diag(toy_scores), [1.0, 1.0])\nassert vectors.shape == (4, 384) and np.isfinite(vectors).all()\nassert scores[0, 3] > scores[0, 1] > scores[0, 2]\nassert float(vectors[0] @ changed) > scores[0, 2]\nprint("검증: 2차원 표기, 384차원 벡터 구조와 본문의 유사도 순서를 확인했습니다.")',
    "03-어텐션-직관": 'assert abs(sum(weights_for_a) - 1.0) < 1e-9 and abs(sum(weights_for_b) - 1.0) < 1e-9\nassert weights_for_b.index(max(weights_for_b)) == 5\nassert weights_for_a.index(max(weights_for_a)) == 2\nprint("검증: 질문 대상에 따라 큰 교재용 비중의 위치가 이동했습니다.")',
    "04-컨텍스트-윈도": 'assert sum(counts.values()) == 387 and actual_input == 400\nassert full_counts[20] <= 448 < full_counts[40]\nprint("검증: 채팅 템플릿 입력과 20/40회 반복의 한도 분류를 확인했습니다.")',
    "05-컨텍스트-로트": 'assert len(observations) == 9\nassert model_limit == 32_768\nlongest_input = 0\nall_have_two_outputs = True\nfor item in observations:\n    longest_input = max(longest_input, item["tokens"])\n    if len(item["outputs"]) != 2:\n        all_have_two_outputs = False\nassert longest_input + max_new_tokens <= model_limit\nassert all_have_two_outputs\nprint("검증: 3개 길이 × 3개 위치가 모델 한도 안이며 중복 출력이 있음을 확인했습니다.")',
    "06-temperature와-샘플링": 'assert torch.isclose(torch.softmax(toy_logits, dim=0).sum(), torch.tensor(1.0))\nassert len(records) == 6\ntemperatures = set()\nfor temperature, _, _ in records:\n    temperatures.add(temperature)\nassert temperatures == {0.3, 1.0}\nprint("검증: 로짓의 확률 변환과 2개 temperature × 동일한 3개 시드의 출력을 확인했습니다.")',
    "07-환각의-구조적-원인": 'assert len(without_context) == 2 and len(with_constraint) == 2\nprint("검증: 근거 제약 전·후의 응답을 각각 2개 확인했습니다.")',
    "08-모델-선택-기준": 'assert len(candidates) == 3 and len(eligible) == 1\nassert model.num_parameters() == 494_032_768\nprint("검증: 필수 조건으로 3개 후보 중 1개를 걸렀습니다.")',
}

OUT.mkdir(parents=True, exist_ok=True)
for slug, data in lessons.items():
    # 모든 코드 셀에 실행 의도를 설명하는 한국어 주석을 둡니다.
    for cell in data["cells"]:
        if cell["cell_type"] == "code" and not any(line.lstrip().startswith("#") for line in cell["source"]):
            cell["source"] = ["# 위 설명의 조건을 실행하고 실제 출력을 확인합니다.\n"] + cell["source"]
    data["cells"].extend([md("## 구조 검증\n\n예상한 실험 조건과 출력 구조가 유지되었는지 확인합니다."), code(VALIDATIONS[slug])])
    for index, cell in enumerate(data["cells"], 1):
        cell["id"] = f"cell-{index:02d}"
    (OUT / f"{slug}.ipynb").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", slug)
