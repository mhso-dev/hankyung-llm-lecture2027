# 01-토큰화와-한국어-효율 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/01-concept.*`).
생성기: `qa/upgrade/author_01.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 01`(환경 변수 없이, 아래 「실행 환경」).
챕터 첫 절이라 작업 전에 `upgrade_gates.py … --label before`로 챕터 전체 수정 전 기록 `gates-before.json`을 남겼습니다(8절 합계 262건, 01절 31건).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 7 | 0 |
| G3 | 2 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 12 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 5 | 12 (준비 1 + 본문 11, 주석 뺀 코드 최대 13줄 = 9절 JSON 읽기 셀) |
| 검사한 문장 | 105 | 344 (`gates-wip-01.json`) |
| 모델 호출 | 0 | 0 (API 키 불필요. 토큰화기 파일만 Hugging Face에서 받음) |

새 커널 실행 PASS(`PASS 01-토큰화와-한국어-효율.ipynb: 12 cells`, Linux aarch64, Python 3.12.13, transformers 4.56.2, tokenizers 0.22.2, huggingface-hub 0.36.2, 2026-09-16). `verify.py --chapter` `PASS 8 sections / 44 code cells (max 25 lines)`(25줄은 개선 전 다른 절). `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-01/vis`에서 require 경로와 브라우저 경로만 바꾼 사본으로 실행, 공용 도구는 고치지 않음).

## 실행 환경 (검토에서 볼 곳)

- **2026-09-16 02절 작업 때 새 환경으로 다시 실행했습니다.** 실습 폴더 잠금 파일 전체를 설치한 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, tokenizers 0.22.2, sentence-transformers 5.1.1, numpy 2.3.3, huggingface-hub 0.36.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`를 `run_section.sh`가 자동으로 씁니다. `UV_NO_SYNC`·`TRANSFORMERS_NO_ADVISORY_WARNINGS`는 주지 않았습니다. 토큰화기 두 개(`openai-community/gpt2`·`klue/bert-base`, 고정 revision)는 이 실행에서 새 캐시로 다시 받았습니다.
- 결과: `PASS 01-토큰화와-한국어-효율.ipynb: 12 cells`, 코드 셀 출력 `outputs_sha256` `060a9d48…`이 처음 실행(torch 없는 부분 설치)과 같고 stderr 출력도 없습니다. 그래서 본문·결과 읽기·그림 라벨 인용은 고치지 않았습니다. `verify.py --chapter` PASS, 게이트 G1~G7 0.
- (처음 실행 기록) 기기 루트 디스크 여유가 약 730MB라 `/tmp/venv-ch05-llm-principles`에 torch 계열 13개를 뺀 고정 버전 68개만 `uv pip install --no-deps`로 넣고, `UV_NO_SYNC=1 TRANSFORMERS_NO_ADVISORY_WARNINGS=1`로 실행했습니다. torch가 없을 때만 나오는 transformers 조언 경고를 끄려던 변수라, 새 환경에서는 필요하지 않습니다. 노트북 코드에는 넣지 않았습니다.
- 커널 작업 폴더 두 경우를 모두 실행(처음 실행 때): `run_section.sh`(프로젝트 맨 위, 긴 경로 분기)와 `/tmp` 사본을 `execute.py --cwd labs/part1/ch05-llm-principles/notebooks`로 실행(`../../ch04-data-tools` 분기) → 두 실행의 코드 셀 출력과 `outputs_sha256`이 같음.
- 뒤 절(02~08)은 같은 새 환경에서 실행합니다(02 sentence-transformers, 04~08 Qwen2.5-0.5B-Instruct).

## Ch 4 전달 파일 `data/article-text.json`

- 경로·칸 이름·바이트를 바꾸지 않았습니다. 실행 뒤 SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`(Ch 4 요약에 적힌 값과 같음). 노트북은 읽기만 합니다.
- 읽는 칸은 개선 전과 같은 `schema_version`·`source`·`record.id`·`record.text` 네 개(Ch 4 05-4 그림 캡션과 06 b8 문장 「두 토큰화기로 나눠 토큰 수를 셉니다」와 맞음). 기사 글 토큰 수는 개선 전 `GPT-2: 81 | KLUE: 17`과 같은 81·17입니다.

## 수정 전 주요 문제

- 셀 4(Ch 4 파일 읽기)가 Ch 1~4에서 가르치지 않은 `from pathlib import Path`·`Path.cwd().parents`·`Path / "…"`·`exists()`·`read_text()`·`raise FileNotFoundError`·`json.loads()`(설명 없음)·`repr()`를 씀. 셀 10은 `assert A and B`. 한 셀에 경로 찾기·읽기·출력·토큰 세기를 몰아 16줄(G2 over_15)
- 셀 4가 GPT-2는 `len(gpt2.encode())`, KLUE는 `len(ko_tokenizer.tokenize())`로 세어 두 수가 같은 방식이 아님(KLUE `encode()`는 특수 토큰 2개를 더함). 본문은 「특수 토큰」을 문단으로만 설명하고 노트북에서 보이지 않음
- 셀 6·8의 `print(…, len(gpt2.encode(…)), …)` 두 겹 호출(G2 5건), 첫 줄 주석 없음 2건과 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」 3곳, 반복 글을 `" ".join([base] * repeat)`(join·목록 곱하기 미교육)
- GPT-2 조각 `'ì'`, `'ĺ'`이 왜 나오는지(바이트 단위 분할) 설명 없음. 본문은 「'Ġ'나 '##'는 표시」만 적음. 반복 실험 해석은 「공백이 추가된 GPT-2 결과는 정확한 배수가 되지 않았다」에서 멈추고 공백 조각을 보이지 않음
- 「앞에서 배운 내용」이 「Ch 2에서 문자열을 리스트처럼 순회」 등 개선된 앞 챕터 요약과 맞지 않음. 준비물·기준 버전·호출 수 없음, 결과 읽기 셀 없음, 틀 주석
- 옛 도식 캡션이 그림에 없는 「보라색은 모델의 처리, 빨간색은 확인할 제한」을 설명(G6 long 포함). G5 7건(제목 셀·그림 없음, 결과 읽기가 출력 인용 안 함), G6 12건(영문·코드 이름+조사로 시작 9건, 70자 초과 3건), G7 3건(Mermaid 0, 삽화 0, 설계표 없음)

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「같은 뜻을 담은 한국어와 영어 문장은 토큰화 방식에 따라 몇 개의 토큰이 될까요?」와 데이터 유지 — 문장 쌍 두 개, 기사 A10, 「한국어 토큰 효율을 측정합니다.」 1·2·4·8번, GPT-2·KLUE 고정 revision): 제목(할 일 3, 호출 0번·1분 안팎, 첫 실행 내려받기 3.6MB, 기준 transformers 4.56.2·tokenizers 0.22.2·Python 3.12.13) → 오늘 볼 그림(01-1) → 1 준비(`os.path.exists()` 분기) → 2 토큰화기 두 개(`warnings.filterwarnings("ignore", message="IProgress not found")` 한 줄 설명, `import transformers`·`__version__`, `AutoTokenizer.from_pretrained(이름, revision=)`, `vocab_size`) → 3 GPT-2 `tokenize()` 18글자 → 39 → 4 `encode()`·슬라이싱 `[0:3]`·`decode()` → `[168, 246, 97]` → `오` → 5 KLUE `tokenize()` 9 → 6 KLUE `encode()`·`convert_ids_to_tokens()` → `[CLS]`·`[SEP]`, `added_count == 2` assert → 7 영어 문장 7·15 → 8 문장 쌍 표(for 풀어 담기) → 9 `with open`+`read()`+`json.loads()`, 네 칸, `schema_version`·`id` assert → 10 기사 글 36글자·81·17 → 11 값 바꿔 보기(for+range+글자 `+`, 37·75·151·303 / 8·16·32·64) → 이음새 조각 `['.', 'Ġ', 'íķ']`·`['.', '한국어']` → 정리
- 모든 결과 읽기는 새 출력에서 인용. 한 번만 본 이음새는 「첫 이음새 말고는 출력하지 않았습니다」로 한정
- 본문 10블록 전체를 다시 씀: 이 절의 질문, 비유(블록 쟁반 — Ch 4 나무 쟁반·상자 이어 씀), 용어 8개 표(LLM·토큰·토큰화와 토큰화기·어휘·토큰 ID·특수 토큰·판 번호·바이트), 세 가지 까닭(조각 크기·공백·특수 토큰), 반복 실험 해석과 결론 범위, 주의 메모 8개(실행하지 않은 것: ID 섞어 쓰기, 채팅 형식 토큰 → 04절, revision 생략, 오프라인, Windows·macOS), 복습 5문항(기초 2·적용 1·분석 2)
- 라이브러리 동작 확인(설치본·내려받은 설정 파일): `tokenization_utils_fast.py` `tokenize(…, add_special_tokens=False)`, `tokenization_utils_base.py` `encode(…, add_special_tokens=True)`, `vocab_size`는 추가 토큰 제외. KLUE `tokenizer.json` 정규화 BertNormalizer·나누기 BertPreTokenizer·모델 WordPiece(`##`, `[UNK]`)·후처리 TemplateProcessing `[CLS] A [SEP]`. GPT-2 `tokenizer.json` 나누기·후처리 ByteLevel(특수 토큰 없음). UTF-8 한글 음절 3바이트는 문장으로만 적음(노트북에서 바이트 수를 세지 않음)
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/01-concept.*`는 본문에서 뺌(원본 `before/figures/`, 옛 파일은 삭제하지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 01-1 TB: 초록 문장 → 초록 KLUE(32000) → 왼쪽 노랑 조각 9개·오른쪽 노랑 ID 11개 → 점선 회색 모델 입력(viewBox 527). 01-2 TB 두 갈래: 왼쪽 GPT-2(50257) → 조각 39개 → 앞 세 ID 168·246·97 → 오, 오른쪽 KLUE → 조각 9개(viewBox 511). 01-3 LR 두 줄: 처음 subgraph 두 칸 시안은 세로로 쌓이고 KLUE가 위로 가서, subgraph 없이 위 GPT-2·아래 KLUE 두 줄로 바꿈(viewBox 625). 01-4 xychart-beta: 위 주황 GPT-2·아래 초록 KLUE(viewBox 700). 한글 범주 이름은 따옴표가 있어야 렌더됨(`["1번", …]`)
- 01-4 색 판단(검토 대상): xychart-beta는 범례·classDef가 없어 `plotColorPalette`로 두 선 색만 정하고, 본문·캡션은 선 위치(위·아래)로 먼저 구분. 주황(#f59e0b)·초록(#22c55e)은 계열 구분용이라고 캡션에 적음
- 삽화 01-5(블록 쟁반): 1회 생성 job `0184d3b8-3aa7-41a7-bb99-c7bf06e84903` 채택, 2크레딧(생성 전 잔액 2902). 결과는 프롬프트의 홈 한 줄·막대 네 개와 달리 홈 두 줄·정육면체 16개씩(32)·막대 3개씩(6)이었으나 관계가 읽혀 채택하고, 비유 단락·그림 읽기·캡션을 저장 파일에 맞춰 씀. 저장 PNG(1100×614)를 기기에서 다시 받아 job 결과(2752×1536)를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0

## 검토에서 볼 곳

- 위 「실행 환경」: 새 전체 환경 재실행에서 출력이 같았는지, `warnings.filterwarnings` 한 줄을 기본 경로에 둔 판단(개선 전 노트북·README와 같은 경고)
- 4절 「한글 한 글자는 UTF-8 방식으로 3바이트」와 「대부분의 글자가 조각 두세 개」 설명 수준, 11절 이음새 한 곳으로 공백 조각을 짐작한 범위
- 비유 삽화(쟁반 홈 = 글, 블록 = 토큰, 상자 = 어휘)가 그림만 보고 읽히는지, 01-4 선 색 이름

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept(중 0, 하 2). 모두 반영했습니다.
- 01-1: 4절 결과 읽기 「한글 13글자 가운데 11글자가 조각 세 개, 두 글자가 조각 두 개가 되어 18글자 문장이 39토큰이 되었습니다.」(b4 「두세 개」는 그대로)
- 01-2: 그림 01-2 왼쪽 아래 화살표 라벨을 「앞 세 ID 되돌리기」로, alt·캡션 파일 읽는 법(「화살표 위 글자는 실행한 메서드이거나, 셀에서 한 일」)·b4 도식 읽기에 「앞 세 ID는 같은 문장을 `encode()`로 바꾼 ID 가운데 앞 세 개이고, `decode()`로 되돌렸습니다」. 다시 렌더(viewBox 511) PNG 확인
- C-5: review-pack 01을 다시 만듦(실행 시각만 다르던 문제)
- 재실행 없음. 코드 셀 12, `outputs_sha256` `060a9d48…` 그대로, 검사한 문장 345

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/01-토큰화와-한국어-효율.md`
- 정리 대상(삭제하지 않고 목록만): `figures/01-concept.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-01`(생성기 초안·화면 검사 사본·요구 목록)
- 챕터 안의 옛 생성기 `make_sources.py`(챕터 루트)와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하면 개선본 `_src`·노트북을 덮어씁니다. 고치지 않았고 실행하지 않았습니다
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음
- 고치지 않은 파일: 실습 폴더 `README.md`(TqdmWarning 문단 그대로 유효). 챕터 밖 Ch 4 06 b8 문장(두 토큰화기·text 칸)은 이 절과 맞아 그대로
