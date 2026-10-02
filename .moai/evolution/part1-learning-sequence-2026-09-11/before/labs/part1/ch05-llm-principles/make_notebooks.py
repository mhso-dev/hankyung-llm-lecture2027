"""Create the eight independent Ch 5 notebooks from reviewed cell sources."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "notebooks"


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

# GPT-2용 BPE와 한국어 BERT용 WordPiece를 로컬에 받아 사용합니다.
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


lessons = {
"01-토큰화와-한국어-효율": notebook("토큰화와 한국어 효율", "같은 뜻을 담은 한국어와 영어 문장은 토큰화 방식에 따라 몇 개의 토큰이 될까요?", [
    md("## 두 토큰화기 준비\n\n어휘와 분할 규칙이 다른 두 토큰화기를 준비합니다."), code(TOKEN_SETUP),
    md("## Ch 4 파싱 텍스트 읽기\n\nCh 4의 HTML에서 추출해 보존한 기사 텍스트와 출처 필드를 읽습니다."),
    code('''import json
from pathlib import Path

root = next(path for path in (Path.cwd(), *Path.cwd().parents)
            if (path / "labs/part1/ch04-data-tools/data/article-text.json").exists())
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
    md("## 교재용 가중 평균\n\n아래 숫자는 실제 모델의 어텐션 값이 아니며, '관련 있는 단어에 더 큰 비중을 두는' 계산을 보이는 교재용 예시입니다."),
    code('''tokens = ["상품", "A는", "파란색이고", "상품", "B는", "빨간색입니다."]
weights_for_b = [0.05, 0.05, 0.05, 0.30, 0.45, 0.10]
print("질문: 상품 B의 색은?")
for token, weight in zip(tokens, weights_for_b):
    print(f"{token:12} {weight:.2f} " + "■" * int(weight * 20))
print("합계:", sum(weights_for_b))'''),
    md("## 질문이 바뀌면 비중도 바뀍니다\n\n같은 문장에서 상품 A를 물으면 교재용 비중을 다르게 둡니다."),
    code('''weights_for_a = [0.30, 0.45, 0.10, 0.05, 0.05, 0.05]
for token, before, after in zip(tokens, weights_for_b, weights_for_a):
    print(f"{token:12} B질문={before:.2f} A질문={after:.2f}")
print("이 비교는 개념 설명용이며 실제 모델을 측정하지 않았습니다.")'''),
]),
"04-컨텍스트-윈도": notebook("컨텍스트 윈도", "모델에 넣을 수 있는 토큰 예산은 입력과 출력 사이에서 어떻게 나눌까요?", [
    md("## 입력 토큰 세기\n\nQwen2.5 로컬 토큰화기로 시스템 지시, 문서, 질문을 함께 세어 봅니다."),
    code('''from transformers import AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision="7ae557604adf67be50417f59c2c2f167def9a775")
parts = {
    "시스템": "주어진 문서 범위에서만 답하세요.",
    "문서": "환불은 결제일로부터 7일 이내에 신청합니다. " * 20,
    "질문": "환불은 며칠 이내에 신청하나요?",
}
counts = {name: len(tokenizer.encode(text)) for name, text in parts.items()}
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
    md("## 로컬 생성 모델 준비"), code(GEN_SETUP), code(GEN_FN),
    md("## 위치와 길이를 바꾸는 실험\n\n질문과 정답 기준은 고정하고, 근거 위치와 주변의 무관한 문장 수만 바꾸어 각 2회 실행합니다."),
    code('''fact = "해바라기 작전의 확인 코드는 314159입니다."
filler = "주문 조회 화면에는 결제 상태와 배송 상태가 표시됩니다."
question = "해바라기 작전의 확인 코드만 답하세요."
conditions = []
for repeats in [2, 20, 60]:
    for position in ["start", "middle", "end"]:
        items = [filler] * repeats
        index = {"start": 0, "middle": repeats // 2, "end": repeats}[position]
        items.insert(index, fact)
        conditions.append((repeats, position, "\\n".join(items) + "\\n\\n" + question))

observations = []
for repeats, position, prompt in conditions:
    outputs = [generate(prompt, temperature=0, seed=seed, max_new_tokens=20) for seed in [1, 2]]
    hits = sum("314159" in output for output in outputs)
    messages = [{"role": "user", "content": prompt}]
    templated = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    tokens = len(tokenizer.encode(templated))
    observations.append({"repeats": repeats, "position": position, "tokens": tokens, "outputs": outputs})
    print(f"filler={repeats:2} position={position:6} tokens={tokens:4} hits={hits}/2 outputs={outputs}")'''),
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
    answers = [answer for t, _, answer in records if t == temperature]
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
    code('''from transformers import AutoModelForCausalLM, AutoTokenizer

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
    md("## 필수 조건으로 후보 거르기\n\n생성 작업과 Apache-2.0 라이선스를 필수 조건으로 두면 조건을 충족하는 후보만 남습니다."),
    code('''required_task = "text-generation"
required_license = "apache-2.0"
eligible = [item for item in candidates if item["task"] == required_task and item["license"] == required_license]
print("eligible:", eligible)
print("선택 전에는 자체 질의셋으로 품질과 속도를 추가 측정해야 합니다.")'''),
]),
}


VALIDATIONS = {
    "01-토큰화와-한국어-효율": 'assert handoff["schema_version"] == "ch04-parsed-article-v1"\nassert handoff["record"]["id"] == "A10" and article_text == handoff["record"]["text"]\nassert len(gpt2.encode(pairs[0][0])) > len(ko_tokenizer.encode(pairs[0][0], add_special_tokens=False))\nassert len(gpt2.encode(base)) > 0\nprint("검증: Ch 4 파싱 텍스트와 두 토큰화기의 한·영 문장 분할을 확인했습니다.")',
    "02-임베딩과-의미-유사도": 'assert vectors.shape == (4, 384) and np.isfinite(vectors).all()\nassert scores[0, 3] > scores[0, 1] > scores[0, 2]\nassert float(vectors[0] @ changed) > scores[0, 2]\nprint("검증: 벡터 구조와 본문의 유사도 순서를 확인했습니다.")',
    "03-어텐션-직관": 'assert abs(sum(weights_for_a) - 1.0) < 1e-9 and abs(sum(weights_for_b) - 1.0) < 1e-9\nassert weights_for_b.index(max(weights_for_b)) == 4\nassert weights_for_a.index(max(weights_for_a)) == 1\nprint("검증: 질문 대상에 따라 큰 교재용 비중의 위치가 이동했습니다.")',
    "04-컨텍스트-윈도": 'assert sum(counts.values()) == 387 and actual_input == 400\nassert full_counts[20] <= 448 < full_counts[40]\nprint("검증: 채팅 템플릿 입력과 20/40회 반복의 한도 분류를 확인했습니다.")',
    "05-컨텍스트-로트": 'assert len(observations) == 9\nassert all(len(item["outputs"]) == 2 for item in observations)\nprint("검증: 3개 길이 × 3개 위치의 중복 출력을 확인했습니다.")',
    "06-temperature와-샘플링": 'assert len(records) == 6\nassert {t for t, _, _ in records} == {0.3, 1.0}\nprint("검증: 2개 temperature × 동일한 3개 시드의 출력을 확인했습니다.")',
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
    data["cells"][-2]["id"] = f"cell-{len(data['cells'])-1:02d}"
    data["cells"][-1]["id"] = f"cell-{len(data['cells']):02d}"
    (OUT / f"{slug}.ipynb").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", slug)
