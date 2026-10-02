# 08-모델-선택-기준 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/08-model-selection.*`).
생성기: `qa/upgrade/author_08.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 08`(환경 변수 없이). 설명만 고칠 때는 `mdpatch.py` → `--no-exec`(생성기를 다시 실행하면 출력이 지워짐. 이 절은 시간 출력이 실행마다 달라, 재실행하면 본문·노트북·그림 08-3의 초 값을 다시 대조해야 함).
수정 전 수치는 `gates-before.json`의 08절 값이고, 작업 시작 때 `gates-before-08.json`으로 다시 확인해 같았습니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 0 | 0 |
| G3 | 1 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 24 | 0 |
| G7 | 3 | 0 |
| 합계 | 34 | 0 |
| 코드 셀 | 4 | 17 (준비 1 + 본문 16, 함수 정의 셀 5개) |
| 검사한 문장 | 130 | 412 (`gates-wip-08.json`) |
| 모델 실행 | `from_pretrained` 1번(Qwen), 생성 0번, 토큰화 1번 | 내 컴퓨터에서 `generate()` 16번(Qwen2.5-0.5B-Instruct·SmolLM2-135M-Instruct × 한국어 평가 자료 4 + 영어 평가 자료 4), 모두 `do_sample=False`·출력 몫 64. API 호출 0, 비용 0 |

## 실행 환경

- 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`. `run_section.sh`가 자동으로 씀. `/tmp`에 torch 설치 없음.
- **새로 받은 모델**: `HuggingFaceTB/SmolLM2-135M-Instruct`@`12fd25f77366fa6b3b4b768ec3050bf629380bac`(Apache-2.0, 134,515,008 파라미터, `model.safetensors` 269,060,552바이트), `HF_HOME=$ROOT/.cache/vm/hf`로 받음, 캐시 276MiB(사용자 디스크). 규칙(1.5GB 이하·메모리 3GB 이하 모델)을 지킴. EXAONE 3.5 2.4B(24억 파라미터, float32 약 9GB)는 내려받지 않고 모델 카드·라이선스 문서만 읽음. 기기 루트 여유 567MB → 566MB.
- 새 커널 실행 PASS(`PASS 08-모델-선택-기준.ipynb: 17 cells`, `run_section.sh` 전체 약 49초). 답 글·정답 수는 기기 셸 스크립트(`/tmp/ch05-08/probe3.py`, 노트북과 같은 코드)와 글자까지 같음. 시간 값은 실행마다 다름(스크립트: 불러오기 1.5·0.8초, 한국어 11.6·6.9초, 영어 17.8·4.3초 / 노트북: 1.9·0.7, 11.5·7.0, 17.8·4.1). 그래서 `outputs_sha256` 반복 일치 확인은 하지 않았고, 노트북 출력으로 본문을 맞춤.
- 메모리(`/usr/bin/time -v probe3.py`, 두 모델을 함께 올리고 생성 16번): 최대 RSS 3,477,772KB(`ru_maxrss` 3396MB, 약 3.4GB). Qwen 적재 순간 3248MB, SmolLM2를 뒤에 올려도 적재 최대치는 그대로, 생성 중 3396MB. SmolLM2를 먼저 올리면 Qwen 적재 순간에 더해져 3.8GB에 가까워질 수 있어 Qwen을 먼저 불러오도록 후보 순서를 둠. `model = None`으로 Qwen을 내려놓는 방식(probe1)은 RSS가 1.87GB까지만 내려가 다시 올리기 위험 → 두 모델을 함께 올리는 방식을 택함.
- `verify.py --chapter` `PASS 8 sections / 115 code cells (max 17 lines)`. `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-08/vis`에 07절 작업자 사본 복사, 공용 도구는 고치지 않음).

## 소스·문서·파일로 확인한 것 (2026-09-16)

- Hugging Face API·모델 카드(판 고정): Qwen2.5-0.5B-Instruct `7ae5576…` license apache-2.0·pipeline text-generation·safetensors 494,032,768·README 「Multilingual support for over 29 languages, including … Korean」「Context Length: Full 32,768」(메타데이터 language는 `en`만 — b7 메모), SmolLM2-135M-Instruct `12fd25f…` apache-2.0·text-generation·language en·README Limitations 「primarily understand and generate content in English」·config `max_position_embeddings` 8192·`torch_dtype` bfloat16, EXAONE-3.5-2.4B-Instruct `ccce25b…` license other/`exaone`·README 「EXAONE AI Model License Agreement 1.1 - NC」·LICENSE 「solely for research purposes」「expressly prohibited from using the Model … for any commercial purposes」·safetensors 2,405,327,360, MiniLM `e8f8c21…` apache-2.0·sentence-similarity, klue/bert-base `77c8b3d…` cc-by-sa-4.0·fill-mask
- 기기 셸(`probe1.py`): 기본 지시 Qwen `You are Qwen, created by Alibaba Cloud. You are a helpful assistant.`, SmolLM2 `You are a helpful AI assistant named SmolLM, trained by Hugging Face`. 같은 문장의 조각 이름 Qwen 첫 조각 `ëħ¸`(「노」 하나), SmolLM2 `ë`·`ħ`·`¸`(세 조각). 불러온 dtype 두 모델 모두 `torch.float32`(노트북 출력에도 있음)
- 기기 셸(`probe2.py`·`probe4.py`, 노트북에 넣지 않음): 출력 몫 32에서 SmolLM2 한국어 0/4(모두 끊김), 64에서 1/4 → 출력 몫 64(07절 값)로 정함. 영어 셋째 문서를 「3 million won」으로 적으면 Qwen이 `15 billion won`으로 답함(b6에 「노트북에 넣지 않음」으로 적음) → 정답 숫자가 같은 「300 dollars」로 둠(노트북 7절 설명)
- 뒤 챕터 파일(개선 전): Ch 6 01 `_src` b3 「Ch 5의 모델 선택표는 작업과 제약에 맞는 후보를 사람이 미리 고르는 기준이었습니다. 이 절은 그 기준으로 미리 고정한 `openai:gpt-5.4-mini`를 API로 호출합니다」, Ch 6 06 `_src`(세 제공자 같은 사용자 메시지·출력 상한, `usage_metadata`·`perf_counter()`, 요금 기준일, 「제공자 전체의 성능 순위를 만들지 않습니다」), Ch 11 01 `_src`(질의셋 = 평가에 반복해서 사용하는 질문 모음, 답변 근거는 Ch 15), Ch 15 02 `_src`(Correctness·Groundedness)

## 수정 전 주요 문제

- 미교육 문법·모양: `f"{model.num_parameters():,}"`(f-string 형식 지정), 글 곱하기 `"한국어 문장을 토큰화합니다. " * 100`, `(time.perf_counter() - start) * 1000`(식 안 숫자), `assert A and B`·`494_032_768`, 영어 출력 라벨 `parameters:`·`eligible:`·`cached load seconds:`, 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」, 첫 줄 주석 없는 검증 셀(G3 1)
- 제목 셀·준비물·핵심 그림·결과 읽기 없음(G5 6). 70자 넘는 문장·5문장 넘는 단락(G6 24). 옛 Excalidraw 도식 1장(왼쪽→오른쪽 네 상자), Mermaid 0·삽화 0·설계표 없음(G7 3)
- 내용: 필터를 통과한 후보가 Qwen 하나라 「비교」가 없고, 「실제 대표 질문과 정답 기준으로 품질과 속도를 추가 측정해야 합니다」를 출력 문장으로만 적고 측정하지 않음. 토큰화 시간 3.631ms·로딩 0.384초는 생성과 관계없는 값이라 본문 대부분이 「이 값이 무엇이 아닌지」 설명에 쓰임. 01~07절 결과(토큰 수·컨텍스트 한도·판정 규칙)와 연결 없음. 라이선스 조건이 작업 조건과 겹쳐 KLUE만 빼서, 라이선스만으로 빠지는 후보가 없음

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「정확도, 속도, 메모리, 라이선스 조건이 다를 때 어떻게 모델 후보를 비교할까요?」를 본문 「이 절의 질문」에 이어 씀. 개선 전 후보 세 개·작업 종류·라이선스 필수 조건·파라미터 수·불러오기 시간 유지): 제목(할 일 3, 생성 16번·비용 0·1분 안팎, SmolLM2 약 270MB 새로 받음, 메모리 약 3.4GB, 두 모델 판 번호, 모델 카드 확인일) → 오늘 볼 그림(08-1) → 1 준비(`time` 포함) → 2 후보 표(모델 카드 값 5개) → 3 필수 조건 거르기(작업 종류·라이선스, EXAONE은 라이선스로만 빠짐) → 4 평가 자료와 선택 기준을 먼저 정하기(04·05·07절 문서 네 개, 출력 몫 64, 한국어 정답 3개 이상·메모리 어림 2.0GB 이하) + 07절과 같은 `find_numbers`·`make_input`, 05·07절과 같은 `ask_model`, 새 `run_evaluation(items)` 정의 → 5 판 번호·`load_candidate(model_name)` 정의·두 후보 불러오기(파라미터 수·컨텍스트 한도·한국어 조각 수)·메모리 어림 → 6 한국어 평가 → 7 값 바꿔 보기 영어 평가 자료 → 8 선택 기준으로 고르기 → 9 값 바꿔 보기 메모리 기준 1.0GB → 정리
- 기본 경로에서 조건 표현식·`**`·`with`·`tokenizer(글)`·f-string 형식 지정·목록/글 곱하기·`zip`·`max`·`sum`·`enumerate`·내포식·`Path`·`raise`·`try/finally`·상속·`threading`·`@`·`BaseModel`·`*args`·`global`을 쓰지 않음. 새로 쓴 모양: 튜플 두 개·세 개 반환(`return correct_count, round(elapsed, 1)`, Ch 2 03 풀어 담기), 딕셔너리 값에 목록 `[토큰화기, 모델]`, 바깥 이름 `tokenizer`·`model`에 후보를 담고 함수 부르기(「함수 안 이름은 부르는 순간의 값을 읽음」 한 문장), 비교 결과를 `and`로 묶어 대입, 메서드 `num_parameters()`, 속성 `dtype`, 이름 붙인 상수 `bytes_per_number = 4`·`bytes_per_gb = 1024 * 1024 * 1024`. 함수 다섯 개는 타입힌트 없이 셀 하나에 하나, 정의·호출 분리
- 본문 10블록 전체를 다시 씀: 학습 목표 3, 이 절의 질문 2개, b3 01·02·04·05·07절 개선본과 Ch 2 03·12 기준, 비유(빵 썰 도구 고르기) + 삽화, 용어 7개(모델 카드·작업 종류·라이선스·필수 조건·파라미터·평가 자료·선택 기준), 거르기와 재기 분리·기준을 먼저 정함, 측정값마다 재는 것(메모리 어림 식 → 숫자, 불러오기 시간, 답 시간, 정답 수, 조각 수), 실행 예제 해설 세 소제목, 해석(언어·판정 규칙 한계·답 시간과 답 길이·선택 기준·경계값·후보 없음·기준을 결과에 맞추지 않음·일반화 금지와 「3 million won」 기기 셸 기록), 주의 메모 10개, 복습 5문항(기초 2·적용 1·분석 2), 참고 자료 5개(모델 카드·라이선스 문서, 판·확인일). 「다음 학습」은 링크 없이 Ch 6(01·06)·Ch 11·Ch 15로 두고 문장만 짧게 나눔(09 실습 절 링크는 다음 단계)
- 개선 전의 「토큰화 시간 3.631ms」 측정은 뺌(생성과 관계없는 전처리 시간이라 본문을 부정 설명에 쓰게 했음). 답 시간에 토큰화·생성·첫 생성 준비가 함께 들어 있다고 b4에 적음
- 실습 폴더 `README.md`에 SmolLM2 캐시 276MiB와 두 모델을 한 커널에 올린다는 문장 한 개를 더함
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/08-model-selection.*`는 본문에서 뺌(원본 `before/figures/`, 삭제하지 않음)
- 기준 값을 정한 시점(검토 1차 08-1에서 더함): 출력 몫 64는 `probe2.py`(출력 몫 32에서 SmolLM2 한국어 0/4)를 본 뒤 정했고, 한국어 정답 3개·메모리 2.0GB는 탐색 스크립트에 없고 `probe3.py`로 두 모델의 정답 수를 본 뒤 만든 생성기에 처음 적었습니다. 본문 b7·노트북 4절에 「흐름을 보여 주려고 정한 예」로 밝힘

## 그림 확인

- PNG 네 장을 직접 열어 확인. 08-1 TB 일곱 상자(초록 후보 → 파랑 필수 조건 → 초록 남은 후보 → 보라 모델 두 개 → 노랑 측정 기록 → 파랑 선택 기준 → 노랑 Qwen), 08-2 TB 두 번 갈라짐(파랑 조건 → 회색 빠진 후보·초록 남은 후보, 화살표 예·아니오), 08-3 LR 2×2(초록 평가 자료 → 노랑 네 결과), 08-4 TB 두 갈래(노랑 기록 → 파랑 기준 둘 → 노랑 판정 → 회색 다음 할 일). viewBox 폭 255·566·686·491로 모두 860 미만. 08-4는 처음 LR로 폭 967이라 TB로 바꿔 다시 렌더
- 색: 후보·평가 자료 초록, 노트북에서 정한 조건 파랑(07절 판정 규칙 선례), 실행한 모델 보라, 출력 기록·판정 노랑, 빠진 후보·실행하지 않은 다음 할 일 회색, 빨강 없음
- 삽화 08-5(빵 칼): 1회차 job `db84bae9-aafb-4b91-a276-a0b9672da9c8` 채택, 2크레딧(생성 전 잔액 2884). 바구니·잠긴 상자가 도마와 한 줄로 붙어 있지만 빵이 없어 「쓰지 않은 도구」로 읽혀 채택. 저장 PNG(1100×614)를 기기에서 다시 받아 채택 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0

## 검토에서 볼 곳

- 새 후보 두 개의 사실 문장(노트북 2·3절, b5 첫 소제목, b7 둘째·셋째 항목, 복습 1, 참고 자료): EXAONE 라이선스 요약 「연구 목적만 허락, 상업 이용 금지」와 Qwen 카드 요약 칸 언어 `en` 메모가 원문과 맞는지
- 측정 해석의 범위(노트북 5~7절 결과 읽기, b4 「측정값마다 재는 것」, b6 둘째~다섯째 단락, 복습 4): 메모리 어림을 실제 메모리로, 답 시간을 모델 속도로 쓰지 않았는지. 영어 셋째 문서의 「300 dollars」 설명이 충분한지
- 선택 기준을 측정 전에 정한 흐름(노트북 4·8·9절, b4 셋째 소제목 셋째 단락, 08-1 도식 읽기 둘째 단락, 복습 5)과 두 모델을 한 커널에 올리는 메모리 안내(준비물, 5절, b7, README)

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(중 1, 하 3). 모두 반영했습니다.
- 08-1(중, 결정: 정한 시점·과정을 b7에): b7 새 항목 「교재를 만들 때는 기기 셸에서 두 모델을 먼저 실행해 보고 출력 몫을 64로 정했습니다. 32에서는 SmolLM2의 한국어 답이 모두 끊겼습니다. 기준 값 3개와 2.0GB는 흐름을 보여 주려고 정한 예입니다. 이 값을 노트북에 적은 것도 탐색 실행에서 두 모델의 정답 수를 본 뒤였습니다. 실제 선택에서는 …」, 4절 설명 「이 교재의 기준 값은 흐름을 보여 주려고 정한 예입니다.」
- 기준 값 시점 기록: 탐색 스크립트 `/tmp/ch05-08/probe2.py`(20:29, 출력 몫 인자)·`probe3.py`(20:32, 출력 몫 64, 두 모델 × 한국어·영어 정답 수 출력)에는 기준 값 3개·2.0GB가 없고, 기준 값은 그 뒤 만든 생성기 `author_08.py`에 처음 나옵니다. 곧 노트북에 기준 값을 적은 시점은 Qwen 3/4·SmolLM2 1/4를 본 뒤입니다(값을 머릿속에서 먼저 정했는지는 기록이 없어 본문은 「적은 것도 … 본 뒤」로 씀)
- 08-2: b6 첫 단락 「셋째 문서는 정답 숫자를 같게 두려고 「300 dollars」로 옮겨, 금액 단위도 달라졌습니다.」, 끝 단락을 둘로 나누고 「그래서 Qwen의 영어 정답 4개도 옮긴 문장에 따라 달라질 수 있습니다.」, [33] 「이 문서만 언어와 함께 금액 단위도 바뀌었습니다.」, 그림 08-3 라벨 「정답 숫자 같게 옮김」·alt·캡션·도식 읽기
- 08-3: [37]·b6·복습 4 「영어 답 네 개 가운데 두 개를 64조각 끝까지」
- 08-4: [8] 「EXAONE 모델 카드의 라이선스 칸은 `other`이고, 라이선스 이름이 `exaone`입니다.」, 그림 08-4 맨 위 「측정 기록 · 메모리는 어림」과 「Qwen은 어림 1.84GB라 초과」(첫 렌더에서 「어림 1.84GB」가 줄바꿈되어 라벨을 바꿈)·alt·캡션, [21] 「모델 파일 기준으로 … 약 24억 개」
- 재실행하지 않았으므로 초 값(1.9·0.7, 11.5·7.0, 17.8·4.1)은 그대로입니다. 코드 셀 17, `outputs_sha256` `6d188945…` 그대로, 검사한 문장 421

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/08-모델-선택-기준.md`
- 정리 대상(삭제하지 않고 목록만): `figures/08-model-selection.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-08`(probe1~4, reps1~5.json, visual 사본·화면 캡처), `qa/upgrade/gates-before-08.json`(작업 시작 확인용)
- 다음 단계(09 실습 절): 08 b8 「다음 학습」과 노트북 정리 끝 문장을 실습 절로 고침. 모델 캐시 `.cache/vm/hf`에 SmolLM2가 더해짐(전체 마감 때 정리 대상)
- 챕터 안 옛 생성기 `make_sources.py`와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않았습니다(개선본을 덮어씀)
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음


## §2-7 리팩터 (2026-09-21)

`find_numbers`·`make_input`·`ask_model` 다시 정의를 빼고 가져옴. `run_evaluation()`은 바깥 tokenizer·model을 읽어 넘김. 답·정답 수는 같고 시간 값만 바뀜(두 번 실행: 2.1/0.8·12.9/8.5·19.6/4.8 → 1.6/0.9·12.4/7.7·19.3/4.7초, 리팩터 전 1.9/0.7·11.5/7.0·17.8/4.1초) → 마지막 실행 값으로 결과 읽기·본문·복습 4·08-3. 코드 셀 17 → 14, 코드 줄 152 → 130.
