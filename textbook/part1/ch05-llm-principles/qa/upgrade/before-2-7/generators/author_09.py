"""Ch 05 09절(챕터 끝 실습 절) 노트북 생성기 (QUALITY-UPGRADE.md §2·§6·§7-2).

사용: python3 author_09.py  → labs/part1/ch05-llm-principles/notebooks/09-LLM-동작-원리-실습.ipynb 를 새로 쓴다(출력 없음).
이후 run_section.sh 가 새 커널 실행 → 그림 첨부 → 빌드 → 게이트를 이어서 한다.
주의: 이 파일을 다시 실행하면 노트북 출력이 지워진다. 설명만 고칠 때는 mdpatch.py → run_section.sh --no-exec.
새 절이라 수정 전 원본은 없다. 인터넷 서비스의 모델을 부르지 않는다(API 키 불필요).
내 컴퓨터에서 Qwen2.5-0.5B-Instruct generate() 4번(질문 2개 × 실행 2번, do_sample=False, 출력 몫 64),
MiniLM encode() 5번(문서 목록 1번 + 질문 4번).

주제: 문서를 골라 넣고 답 점검하기. 창구 문서 세 개(04절 환불 문장, 07절 노을 워커 3 배터리·해바라기 연구소 초록 패스)에서
02절 유사도로 질문과 가장 가까운 문서를 고르고(pick_document), 04절 채팅 템플릿으로 시스템 지시·문서·질문을 합쳐
조각 수와 남는 칸을 세고, 05·06절 뽑기를 끈 설정으로 답을 받고(ask_model), 07절 판정 규칙(새 숫자·보류 문장)으로 점검한다.
조립 함수 run_check(question, system_text) 하나로 잇고, 기록장 칸 일곱 개를 Ch 2 13절·Ch 4 06절 print_report()로 출력한다.
실행 1: system_text = 04절 「주어진 문서 범위에서만 답하세요.」, 실행 2: 07절 9절 보류 지시(값 하나만 바꿈).
질문: 「환불은 며칠 이내에 신청하나요?」(04·08절, 문서에 답 있음), 「노을 워커 3의 무게는 몇 g인가요?」(새 질문, 문서에 답 없음).

가져온 이름(새 문법·새 API 없음):
01절 tokenizer.encode()로 조각 수 / 02절 SentenceTransformer(이름, revision=)·get_sentence_embedding_dimension()·
encode(목록, normalize_embeddings=True)·.shape·dot_product(first, second)·「길이 1인 벡터끼리는 점곱 = 코사인 유사도」·round(값, 4) /
03절 largest_position()처럼 for+if로 가장 큰 값 찾기(함수는 쓰지 않음) / 04절 max_position_embeddings·practice_window 512·
output_budget 64·input_budget = practice_window - output_budget·남는 칸·시스템 지시 / 05·07·08절 ask_model(input_text) 같은 코드 /
06절 뽑기를 끈 설정 / 07절 make_input(system_text, user_text)·find_numbers(text)·find_new_numbers(answer, source_text)·
abstain_sentence·보류 지시 문장 / 08절 두 모델을 한 커널에 올리기·튜플 반환·Qwen 선택 /
Ch 2 13절·Ch 4 06절 print_report(report)·기록장 딕셔너리·칸별 비교 셀.
03절 어텐션 비중, 06절 뽑기를 켠 생성(set_seed·temperature)은 쓰지 않는다.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "textbook/_notebook/upgrade"))
from nbkit import RUN_DATE, code, md, setup, write_notebook  # noqa: E402

LAB = ROOT / "labs/part1/ch05-llm-principles/notebooks"


def section_09() -> tuple[str, str, list[dict]]:
    cells = [
        md("""# LLM 동작 원리 실습: 문서를 골라 넣고 답 점검하기

**이 노트북에서 할 일**

1. 01~08절의 함수와 모델을 이어, 질문과 가까운 문서를 골라 넣고 답을 받는 흐름을 조립합니다.
2. 04절 시스템 지시로 질문 두 개를 묻고, 조각 수와 판정 결과를 기록장에 적습니다(실행 1).
3. 시스템 지시 하나만 07절 보류 지시로 바꿔 같은 질문을 묻고, 두 기록장을 비교합니다(실행 2).

**준비물** — API 키는 필요 없습니다. 인터넷 서비스의 모델을 부르지 않고, 내 컴퓨터에서 작은 모델 두 개를 실행합니다.
그래서 비용은 들지 않습니다. 언어 모델이 답을 만드는 계산은 모두 4번 합니다.

실행 시간은 1분 안팎입니다. 모델 파일은 02절 임베딩 모델과 03~08절 언어 모델을 그대로 씁니다.
캐시에 없으면 두 모델 합쳐 약 1.4GB를 Hugging Face 사이트에서 내려받습니다.
노트북과 같은 계산을 스크립트로 실행했을 때 Python이 쓴 메모리는 최대 약 3.2GB였습니다.

**기준 버전** — 실습 폴더에 고정한 torch 2.8.0과 transformers 4.56.2를 씁니다. 임베딩 모델에는 sentence-transformers 5.1.1을 씁니다.
모델 `Qwen/Qwen2.5-0.5B-Instruct`는 판 번호 `7ae557604adf67be50417f59c2c2f167def9a775`로 받습니다.
모델 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`는 판 번호 `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`로 받습니다.

교재 출력은 Linux(aarch64)의 Python 3.12.13과 CPU용 torch(2.8.0+cpu)로 만들었습니다. 다른 버전, GPU, Windows·macOS에서는 이번에 실행하지 않았습니다.

실습 폴더 `labs/part1/ch05-llm-principles`에서 01절과 같은 `.venv` 커널을 고른 뒤 첫 셀부터 순서대로 실행합니다.
새 문법과 새 라이브러리 기능은 없습니다. 강사와 함께 셀을 차례로 실행하며, 따로 내는 과제는 없습니다.""", html="skip"),
        md("""## 오늘 볼 그림

![초록 상자 질문과 문서 세 개가 파란 상자 pick_document를 지나고, 초록 상자 시스템 지시와 함께 파란 상자 make_input과 encode로 들어간 뒤, 보라 상자 언어 모델 ask_model, 파란 상자 find_new_numbers와 보류 문장 확인을 거쳐 노란 상자 기록장으로 가는 조립도](attachment:09-1-조립도.png)

위에서 아래로 읽습니다. 초록 상자는 노트북에서 정한 질문·문서와, 실행 1·2에서 바꾸는 시스템 지시입니다.
파란 상자는 노트북에서 정의한 함수이고, 보라 상자는 답을 만드는 언어 모델입니다. 맨 아래 노란 상자가 칸 일곱 개의 기록장입니다.""", html="skip"),
        md("""## 1. 준비

이 절은 파일을 읽거나 만들지 않습니다. 준비 셀에서는 02절의 sentence-transformers와 03~08절의 transformers를 함께 불러옵니다.

함수 `warnings.filterwarnings()` 줄은 01·02절처럼 진행 표시 위젯이 없다는 경고 한 줄을 끕니다.
함수 `transformers.logging.set_verbosity_error()`는 04절처럼, 생성 셀에서 나오는 오류가 아닌 안내를 화면에 내지 않게 합니다."""),
        setup(r'''# 두 패키지를 불러오고, 오류가 아닌 안내 경고를 줄인 뒤 버전을 확인합니다
import warnings

# 진행 표시 위젯이 없다는 경고(TqdmWarning)는 계산과 관계없어 화면에 내지 않습니다
warnings.filterwarnings("ignore", message="IProgress not found")

import sentence_transformers
import transformers
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

# 생성 셀의 안내(오류 아님)를 화면에 내지 않습니다
transformers.logging.set_verbosity_error()
print("sentence-transformers 버전:", sentence_transformers.__version__)
print("transformers 버전:", transformers.__version__)'''),
        md("""**결과 읽기** — 출력 줄은 `sentence-transformers 버전: 5.1.1`과 `transformers 버전: 4.56.2`입니다. 준비물에 적은 기준 버전과 같습니다."""),
        md("""## 2. 실습 주제 — 문서를 골라 넣고 답 점검하기

작은 상담 창구를 떠올립니다. 창구에는 앞 절에서 쓴 문서 세 개가 있습니다.
04절 환불 문장, 07절 노을 워커 3 배터리 문장, 07절 해바라기 연구소 초록 패스 문장입니다.

질문이 오면 02절 유사도로 질문과 가장 가까운 문서 하나를 고릅니다. 고른 문서와 질문을 04절 채팅 템플릿으로 합쳐 모델에 넣습니다.
받은 답은 07절 판정 규칙으로 점검합니다. 확인한 값은 Ch 4 06절처럼 기록장 딕셔너리에 적습니다.

질문은 두 개입니다. 첫 질문 「환불은 며칠 이내에 신청하나요?」는 문서에 답이 있습니다.
둘째 질문 「노을 워커 3의 무게는 몇 g인가요?」는 세 문서 어디에도 답이 없습니다.

실행 1은 04절 시스템 지시 「주어진 문서 범위에서만 답하세요.」로 묻습니다. 실행 2는 시스템 지시 하나만 07절 보류 지시로 바꿔 같은 질문을 묻습니다.

언어 모델은 08절에서 선택 기준으로 고른 Qwen입니다. 03절 어텐션 비중과 06절 뽑기를 켠 생성은 이번 실습에서 쓰지 않습니다."""),
        md("""## 3. 재료 만들기 — 두 모델 불러오기

언어 모델은 03~08절과 같은 Qwen2.5-0.5B-Instruct입니다. 임베딩 모델은 02절과 같은 multilingual MiniLM입니다.
두 모델 모두 01절처럼 판 번호(revision)를 고정해 받습니다.

함수 `ask_model()`은 바깥 이름 `model`을 읽습니다. 그래서 02절에서 `model`에 담았던 임베딩 모델을 이번에는 `embedding_model`에 담습니다.
08절처럼 모델 두 개를 한 커널에 올리므로, 메모리가 작은 컴퓨터에서는 다른 노트북의 커널을 먼저 종료합니다.

실행 전에 예상합니다. 컨텍스트 한도는 04절의 32768, 임베딩 벡터 길이는 02절의 384일 것입니다."""),
        code(r'''# 03~08절 언어 모델과 토큰화기를 먼저 받고, 02절 임베딩 모델을 받습니다
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
model_revision = "7ae557604adf67be50417f59c2c2f167def9a775"
tokenizer = AutoTokenizer.from_pretrained(model_name, revision=model_revision)
model = AutoModelForCausalLM.from_pretrained(model_name, revision=model_revision)
# ask_model() 함수가 읽는 이름 model과 겹치지 않게, 임베딩 모델은 embedding_model에 담습니다
embedding_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
embedding_revision = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
embedding_model = SentenceTransformer(embedding_name, revision=embedding_revision)
print("컨텍스트 한도:", model.config.max_position_embeddings)
print("임베딩 벡터 길이:", embedding_model.get_sentence_embedding_dimension())'''),
        md(f"""**결과 읽기** — 출력 줄은 `컨텍스트 한도: 32768`과 `임베딩 벡터 길이: 384`입니다. 예상과 같습니다.

이 노트북의 출력은 {RUN_DATE}에 이 두 모델과 판 번호로 실행한 결과입니다. 실행 환경이나 버전이 바뀌면 답 문장이 달라질 수 있습니다."""),
        md("""## 4. 재료 만들기 — 문서 세 개

창구의 문서 세 개를 목록에 담습니다. 04·08절 환불 문장, 07·08절 배터리 문장과 초록 패스 문장입니다.

문서마다 01절처럼 Qwen 토큰화기로 조각 수를 셉니다. 이어서 02절처럼 `normalize_embeddings=True`를 주어 길이 1로 맞춘 벡터로 바꿉니다.
02절에서 본 것처럼, 길이가 1인 벡터끼리는 점곱이 곧 코사인 유사도입니다.

실행 전에 예상합니다. 배터리 문장은 08절과 같은 23조각이고, 벡터 모양은 문서 3개에 숫자 384개씩일 것입니다.
여러 줄로 나오는 표라서 라벨 줄을 먼저 출력합니다."""),
        code(r'''# 문서 세 개를 목록에 담고, 조각 수를 센 뒤 길이 1로 맞춘 벡터로 바꿉니다
documents = [
    "환불은 결제일로부터 7일 이내에 신청합니다.",
    "노을 워커 3의 배터리 용량은 4200mAh입니다.",
    "해바라기 연구소의 초록 패스 제도는 2026년에 연구자 한 명당 300만 원을 지원합니다.",
]
print("문서 번호 | 조각 수 | 문서")
for number in range(len(documents)):
    token_ids = tokenizer.encode(documents[number])
    print(number, "|", len(token_ids), "|", documents[number])
# normalize_embeddings=True를 주면 벡터마다 길이가 1이 되도록 나눈 값을 반환합니다
document_vectors = embedding_model.encode(documents, normalize_embeddings=True)
print("문서 벡터 모양:", document_vectors.shape)'''),
        md("""**결과 읽기** — 라벨 줄 아래 세 줄은 `0 | 17 |`, `1 | 23 |`, `2 | 37 |`로 시작합니다. 마지막 줄은 `문서 벡터 모양: (3, 384)`입니다.

배터리 문장 23조각은 08절 5절의 한국어 문장 조각 수와 같습니다. 문서가 길수록 조각이 많아, 04절 연습용 한도에서 입력이 차지하는 칸도 늘어납니다."""),
        md("""## 5. 재료 만들기 — 질문 두 개와 정해 둘 값

질문 두 개와, 실행 1·2에서 바꾸지 않을 값을 정합니다. 연습용 한도 512와 출력 몫 64는 04절 값입니다.
입력 한도는 04절 식 `입력 한도 = 전체 한도 - 출력 몫`으로 구합니다.

보류 문장은 07절에서 정한 글 「제공된 정보로는 확인할 수 없습니다」입니다. 07절 판정 규칙은 답에 이 글이 들어 있으면 보류한 답으로 봅니다.

실행 전에 예상합니다. 입력 한도는 04절처럼 448일 것입니다."""),
        code(r'''# 질문 두 개, 04절 연습용 한도와 출력 몫, 07절 보류 문장을 정합니다
questions = ["환불은 며칠 이내에 신청하나요?", "노을 워커 3의 무게는 몇 g인가요?"]
practice_window = 512
output_budget = 64
input_budget = practice_window - output_budget
abstain_sentence = "제공된 정보로는 확인할 수 없습니다"
print("질문 수:", len(questions))
print("입력 한도:", input_budget)'''),
        md("""**결과 읽기** — 출력 줄은 `질문 수: 2`와 `입력 한도: 448`입니다. 예상과 같습니다.

첫 질문은 04·08절과 같은 질문이고, 둘째 질문은 이 실습에서 새로 만든 질문입니다. 둘째 질문의 제품 이름은 07절에서 교재가 지어낸 이름입니다."""),
        md("""## 6. 부품 준비 — 가장 가까운 문서 고르기

첫 부품은 질문과 가장 가까운 문서를 고르는 함수입니다. 먼저 02절과 같은 코드의 점곱 함수를 정의합니다.
같은 자리의 숫자끼리 곱해 모두 더한 값을 반환합니다. 이 셀은 함수를 정의만 합니다."""),
        code(r'''# 두 벡터의 점곱(같은 자리 숫자끼리 곱해 모두 더한 값)을 반환하는 함수를 정의합니다(02절과 같은 코드)
def dot_product(first, second):
    total = 0
    # 반복 번호 i로 두 벡터의 같은 자리 숫자를 짝지어 곱하고 더합니다
    for i in range(len(first)):
        total = total + first[i] * second[i]
    return total'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

다음 함수 `pick_document()`는 질문을 길이 1로 맞춘 벡터로 바꾸고, 문서 벡터 세 개와 점곱을 차례로 계산합니다.
문서마다 유사도를 출력하고, 유사도가 가장 큰 문서와 그 유사도를 반환합니다. 반환값이 두 개라서 08절처럼 튜플로 받습니다.

가장 큰 값은 03절 `largest_position()`처럼 `for`와 `if`로 찾습니다. 코사인 유사도는 -1과 1 사이라서, 기준값을 가장 작은 값 -1.0에서 시작합니다.
함수 안에서 바깥 이름 `embedding_model`, `documents`, `document_vectors`를 읽습니다. 이 셀도 정의만 합니다."""),
        code(r'''# 질문과 문서 세 개의 유사도를 출력하고, 가장 큰 문서와 그 유사도를 반환하는 함수를 정의합니다
def pick_document(question):
    # 02절처럼 목록으로 넣고, 길이 1로 맞춘 질문 벡터를 받습니다
    question_vectors = embedding_model.encode([question], normalize_embeddings=True)
    best_number = 0
    best_similarity = -1.0
    for number in range(len(documents)):
        # 길이 1인 벡터끼리는 점곱이 곧 코사인 유사도입니다
        similarity = dot_product(question_vectors[0], document_vectors[number])
        print("문서", number, "유사도:", round(similarity, 4))
        if similarity > best_similarity:
            best_number = number
            best_similarity = similarity
    return documents[best_number], round(best_similarity, 4)'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

## 7. 부품 준비 — 입력을 만들고 답 받기

둘째 부품은 07·08절과 같은 코드의 입력 함수입니다. 인자 `system_text`가 빈 글이 아니면 그 글을 시스템 메시지로 앞에 넣습니다.
이번 실습은 두 실행 모두 시스템 지시를 넣습니다. 이 셀은 함수를 정의만 합니다."""),
        code(r'''# 시스템 지시와 사용자 글을 받아, 채팅 템플릿으로 합친 입력 글을 반환하는 함수를 정의합니다(07·08절과 같은 코드)
def make_input(system_text, user_text):
    message_list = []
    # 시스템 지시가 빈 글이 아닐 때만 시스템 메시지를 먼저 넣습니다
    if system_text != "":
        message_list.append({"role": "system", "content": system_text})
    message_list.append({"role": "user", "content": user_text})
    return tokenizer.apply_chat_template(message_list, tokenize=False, add_generation_prompt=True)'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

다음은 05·07·08절과 같은 코드의 `ask_model()` 함수입니다. 06절에서 본 뽑기를 끈 설정(`do_sample=False`)으로 답을 만듭니다.
05절에서는 같은 기기에서 같은 입력을 다시 넣었을 때 같은 답이 나왔습니다. 이 셀도 정의만 합니다."""),
        code(r'''# 입력 글을 받아, 출력 몫 안에서 모델이 만든 새 조각만 글로 바꿔 반환하는 함수를 정의합니다(05·07·08절과 같은 코드)
def ask_model(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    # do_sample=False는 05~08절처럼 다음 조각을 무작위로 뽑지 않는 설정입니다
    output_ids = model.generate(input_ids=input_ids, max_new_tokens=output_budget, do_sample=False)
    all_ids = output_ids[0].tolist()
    # 입력 조각 수만큼 건너뛴 뒤가 새 조각입니다
    input_length = len(input_ids[0])
    new_ids = all_ids[input_length:len(all_ids)]
    return tokenizer.decode(new_ids)'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

## 8. 부품 준비 — 07절 판정 규칙

셋째 부품은 07절 판정 규칙입니다. 먼저 07절과 같은 코드의 숫자 찾기 함수를 정의합니다.
글에서 이어진 숫자 글자를 찾아 숫자 글 목록으로 반환합니다. 이 셀은 함수를 정의만 합니다."""),
        code(r'''# 글에서 이어진 숫자 글자를 찾아, 숫자 글 목록으로 반환하는 함수를 정의합니다(07절과 같은 코드)
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
    return numbers'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

다음은 07절과 같은 코드의 `find_new_numbers()` 함수입니다. 답의 숫자 가운데 인자 `source_text`의 글에 없던 숫자만 모아 반환합니다.
07절은 이 목록을 새 숫자라고 불렀습니다.

이번 실습은 `source_text`에 모델이 받은 입력 글 전체를 넣습니다. 입력 글은 시스템 지시, 고른 문서, 질문을 채팅 템플릿으로 합친 글입니다.
그래서 새 숫자는 모델이 받은 글 어디에도 없던 숫자입니다. 이 셀도 정의만 합니다."""),
        code(r'''# 답의 숫자 가운데, 기준 글에 없던 숫자만 모아 반환하는 함수를 정의합니다(07절과 같은 코드)
def find_new_numbers(answer, source_text):
    source_numbers = find_numbers(source_text)
    new_numbers = []
    for number_text in find_numbers(answer):
        # 질문이나 문서에 없던 숫자만 모읍니다
        if number_text not in source_numbers:
            new_numbers.append(number_text)
    return new_numbers'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다.

## 9. 기록 장치 — 기록장 출력 함수

두 실행을 비교하려면 결과를 같은 칸에 적어 둬야 합니다. Ch 2 13절과 Ch 4 06절처럼 딕셔너리를 기록장으로 씁니다.
기록장을 칸마다 한 줄씩 출력하는 함수는 Ch 4 06절의 `print_report()`를 그대로 가져옵니다. 이 셀은 함수를 정의만 합니다."""),
        code(r'''# Ch 2 13절·Ch 4 06절 함수: 기록장 딕셔너리의 칸을 한 줄에 하나씩 출력합니다
def print_report(report):
    # items()는 키와 값의 짝을 차례로 내놓습니다
    for key, value in report.items():
        print(key, "|", value)'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다. 이 함수는 실행 1과 실행 2에서 질문마다 부릅니다.

## 10. 조립하기 — 질문에서 기록장까지

조립 함수 `run_check()`는 질문과 시스템 지시를 받아, 부품을 차례로 부르고 기록장을 반환합니다. 주석마다 그 줄이 쓰는 절을 적었습니다.

기록장 칸은 일곱 개입니다. 고른 문서, 유사도, 입력 조각 수, 남는 칸, 답, 새 숫자, 보류 문장 있음입니다.
남는 칸은 04절처럼 입력 한도에서 실제 입력 조각 수를 뺀 값입니다. 답은 05절처럼 줄바꿈을 빈칸으로 바꿔 한 줄로 적습니다.

함수 안에서 바깥 이름 `tokenizer`, `input_budget`, `abstain_sentence`를 읽습니다. 이 셀은 함수를 정의만 합니다."""),
        code(r'''# 조립: 문서 고르기 → 입력 만들기 → 답 받기 → 판정까지 기록장에 적습니다
def run_check(question, system_text):
    # 02절 유사도로 가장 가까운 문서 고르기
    document, similarity = pick_document(question)
    # 04절 채팅 템플릿으로 시스템 지시·문서·질문을 합치고, 01절처럼 조각으로 나누기
    input_text = make_input(system_text, document + "\n" + question)
    input_ids = tokenizer.encode(input_text)
    # 05·06절 뽑기를 끈 설정으로 답 받기
    answer = ask_model(input_text)
    report = {"고른 문서": document, "유사도": similarity, "입력 조각 수": len(input_ids)}
    # 04절 입력 한도에서 실제 입력을 빼고 남는 칸
    report["남는 칸"] = input_budget - len(input_ids)
    report["답"] = answer.replace("\n", " ")
    # 07절 판정 규칙: 입력에 없던 숫자와 보류 문장
    report["새 숫자"] = find_new_numbers(answer, input_text)
    report["보류 문장 있음"] = abstain_sentence in answer
    return report'''),
        md("""**결과 읽기** — 정의만 하는 셀이라 출력이 없습니다. 조립이 끝났으니, 이제 질문과 시스템 지시만 넣어 부르면 됩니다.

## 11. 실행 1 — 04절 시스템 지시

변수 `system_text`에 04절 시스템 지시를 담고, 질문 두 개로 조립 함수를 차례로 부릅니다.
기록장은 질문마다 칸별로 출력하고, 비교하려고 목록 `reports_1`에 모읍니다. 언어 모델은 질문마다 한 번씩, 모두 2번 답을 만듭니다.

실행 전에 예상합니다. 첫 질문은 환불 문서를, 둘째 질문은 제품 이름이 같은 배터리 문서를 고를 것입니다.
첫 질문은 문서 범위에서만 답하라고 했으니 7일이라고 답할 것입니다. 둘째 질문은 문서에 무게가 없으니, 모른다고 하거나 숫자를 지어낼 것입니다."""),
        code(r'''# 실행 1: 04절 시스템 지시로 질문 두 개를 차례로 점검합니다
system_text = "주어진 문서 범위에서만 답하세요."
reports_1 = []
for question in questions:
    print("질문:", question)
    report = run_check(question, system_text)
    reports_1.append(report)
    print("기록장:")
    print_report(report)'''),
        md("""**결과 읽기** — 첫 질문은 `문서 0 유사도: 0.7636`인 환불 문서를 골랐고, `입력 조각 수 | 57`, `남는 칸 | 391`입니다. 답은 `환불은 결제일로부터 14일 이내에 신청합니다.<|im_end|>`이고 `새 숫자 | ['14']`입니다.

둘째 질문은 `문서 1 유사도: 0.5174`인 배터리 문서를 골랐고, `입력 조각 수 | 66`입니다. 답은 `노을 워커 3의 무게는 약 150g 입니다.<|im_end|>`이고 `새 숫자 | ['150']`입니다.

예상과 달리 첫 답은 문서의 7일을 14일로 바꿨습니다. 08절에서 시스템 메시지 없이 같은 문서와 질문을 넣었을 때도 답에 14일이 나왔습니다.
두 답 모두 `보류 문장 있음 | False`입니다. 07절 새 숫자 규칙이 입력에 없던 14와 150을 잡았습니다.

둘째 질문의 유사도 0.5174는 첫 질문의 0.7636보다 낮지만, 세 문서 가운데서는 가장 컸습니다. 가장 가까운 문서를 골라도, 그 문서에 답이 있다는 보장은 없습니다.
모델은 배터리 문서를 받고도 문서에 없는 무게를 적었습니다."""),
        md("""## 12. 실행 2 — 시스템 지시 하나만 바꾸기

바꾸는 값은 시스템 지시 `system_text` 하나입니다. 07절 9절의 보류 지시로 바꾸고, 같은 질문 두 개로 같은 조립 함수를 부릅니다.
문서, 질문, 출력 몫, 판정 규칙은 그대로입니다.

실행 전에 예상합니다. 고른 문서와 유사도는 시스템 지시를 쓰지 않으니 실행 1과 같을 것입니다. 보류 지시가 04절 지시보다 길어서, 입력 조각 수는 늘고 남는 칸은 줄 것입니다.

07절에서는 보류 지시를 넣자 문서 없는 질문은 보류했지만, 문서가 있는 질문 하나도 보류했습니다.
그래서 둘째 질문은 보류하고, 첫 질문도 보류할 수 있다고 예상합니다."""),
        code(r'''# 실행 2: 시스템 지시 하나만 07절 보류 지시로 바꾸고, 같은 질문 두 개를 점검합니다
system_text = "주어진 질문에 정답 근거가 없으면 추측하지 말고 '제공된 정보로는 확인할 수 없습니다'라고 답하세요."
reports_2 = []
for question in questions:
    print("질문:", question)
    report = run_check(question, system_text)
    reports_2.append(report)
    print("기록장:")
    print_report(report)'''),
        md("""**결과 읽기** — 유사도 줄은 실행 1과 같고, 입력 조각 수는 `입력 조각 수 | 79`와 `입력 조각 수 | 88`, 남는 칸은 `남는 칸 | 369`와 `남는 칸 | 360`입니다.
첫 질문의 답은 `7일 이내에<|im_end|>`이고 `새 숫자 | []`입니다. 둘째 질문의 답은 `제공된 정보로는 확인할 수 없습니다.<|im_end|>`이고 `보류 문장 있음 | True`입니다.

예상대로 입력은 질문마다 22조각 늘었습니다. 문서와 질문이 같으니, 늘어난 조각은 두 시스템 지시의 길이 차이입니다.

예상과 달리 첫 질문은 보류하지 않고, 문서의 7일을 적었습니다. 07절에서 문서가 있는데도 보류한 질문과는 결과가 달랐습니다.
질문 두 개로 한 번 본 결과라서, 보류 지시가 늘 답을 고친다고 말할 수는 없습니다."""),
        md("""## 13. 두 기록장 비교하기

두 실행의 기록장을 질문마다 같은 키끼리 비교합니다. Ch 4 06절 비교 셀과 같은 모양이고, 기호 `!=`는 「두 값이 다른가」 비교입니다.
바깥 `for`는 질문 번호를 하나씩 바꾸고, 안쪽 `for`는 기록장의 칸을 차례로 읽습니다.

검사 줄 `assert`는 두 실행의 고른 문서가 같은지 확인합니다. 문서 고르기는 시스템 지시를 쓰지 않으므로 매번 같아야 하는 값입니다.

실행 전에 예상합니다. 고른 문서와 유사도는 같고, 입력 조각 수·남는 칸·답·새 숫자는 달라질 것입니다. 보류 문장 칸은 둘째 질문에서만 달라질 것입니다."""),
        code(r'''# 두 실행의 기록장을 질문마다 칸별로 비교하고, 달라진 칸의 수를 셉니다
changed_count = 0
for number in range(len(questions)):
    print("질문 번호:", number)
    for key, value_1 in reports_1[number].items():
        value_2 = reports_2[number][key]
        if value_1 != value_2:
            print("달라짐 |", key, "|", value_1, "->", value_2)
            changed_count = changed_count + 1
        else:
            print("같음 |", key, "|", value_1)
    # 문서 고르기는 시스템 지시를 쓰지 않으므로 두 실행이 같아야 합니다
    assert reports_1[number]["고른 문서"] == reports_2[number]["고른 문서"]
print("달라진 칸 수:", changed_count)'''),
        md("""**결과 읽기** — 마지막 줄은 `달라진 칸 수: 9`입니다. 첫 질문은 네 칸, 둘째 질문은 다섯 칸이 달라졌고, 검사 줄 `assert`도 멈추지 않았습니다.
두 질문 모두 고른 문서와 유사도(`같음 | 유사도 | 0.7636`, `같음 | 유사도 | 0.5174`)가 같았습니다. 첫 질문은 `같음 | 보류 문장 있음 | False`도 같았습니다.

바꾼 값은 시스템 지시 하나이고, 문서 고르기는 그대로였습니다. 지시가 들어간 입력부터 조각 수와 답이 달라졌습니다.
실행 1에서 잡힌 새 숫자 두 개는 실행 2에서 나오지 않았습니다. 이 결과는 질문 두 개와 모델 하나로 한 번 본 것입니다."""),
        md("""## 정리

- 02절 유사도, 04절 입력 한도, 05·06절 뽑기를 끈 답, 07절 판정 규칙을 조립 함수 하나로 이었습니다.
- 실행 1(04절 지시)에서 환불 답은 문서의 7일을 14일로 바꿨습니다. 무게 답은 150g을 지어냈고, 새 숫자 규칙이 두 숫자를 잡았습니다.
- 실행 2(07절 보류 지시)에서 입력은 22조각 늘었고, 환불 답은 7일, 무게 질문은 보류 문장이었습니다. 질문 두 개로 한 번 본 결과입니다.

이 절로 Ch 5가 끝납니다. Ch 6에서는 인터넷 서비스의 모델을 LangChain의 공통 방식으로 부릅니다.
Ch 9에서는 이 실습의 문서 고르기를, 질문과 가까운 문서 덩어리(청크)를 가져오는 검색 단계로 다시 배웁니다."""),
    ]
    return "09-LLM-동작-원리-실습", "experiment", cells


if __name__ == "__main__":
    slug, lesson_format, cells = section_09()
    write_notebook(LAB, "09", slug, lesson_format, cells)
