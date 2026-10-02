# Ch 5 verification

Date: 2026-09-09. Python 3.12.13; pinned dependencies in `labs/part1/ch05-llm-principles/uv.lock`.

- Eight independent notebooks, 33 code cells, maximum 21 lines per cell: fresh-kernel execution passed.
- HTML code, retained actual outputs, and embedded notebook downloads: eight lessons passed the common verifier.
- Student installation from only `pyproject.toml` and `uv.lock`, with no dependency overrides: ipykernel 7.3.0, Transformers 4.56.2, Torch 2.8.0, and Sentence Transformers 5.1.1 imported successfully.
- Independent technical review: APPROVE; Pyright reported zero errors, lockfile check passed, and targeted Ruff checks passed.
- All eight lessons have the ten required blocks and three or four review questions. Lecture hours sum to 10 and practice hours to 6.
- Experiments use pinned local pretrained models, without paid model API calls. Their small-sample observations are not general quality rankings.
- Lesson 04 counts chat-template tokens. Lesson 05 separates the 512-token teaching budget from the pinned Qwen model's 32,768-position limit, and does not claim unobserved length-based deterioration. Lessons 06–08 preserve the sampling, hallucination, and timing limitations stated in the actual-output review.

The final browser and archive checks are recorded in [Part 1 verification](../../qa/verification.md), [delivery results](../../qa/delivery-results.json), and [technical review](../../qa/topic-review.md). The final Korean and meaning reviews are in this directory's `language/`, `textbook/part1/qa/language/ch05/`, and [final meaning review](../../qa/final-meaning-review.md).

Only macOS execution was measured. Model files require a separate first download. The external spelling service was not called because its skill prohibits commercial bulk processing; local spelling and prose review were performed. Excalidraw MCP preview was unavailable, so matching SVG/Excalidraw structure and browser measurements were used.

## 품질 개선 01 토큰화와 한국어 효율 (2026-09-16)

- 새 커널 실행 PASS: `01-토큰화와-한국어-효율.ipynb` 코드 셀 12개, Linux aarch64, Python 3.12.13, transformers 4.56.2, tokenizers 0.22.2, huggingface-hub 0.36.2. 모델 호출 0번.
- 실행 환경: 기기 디스크 부족으로 torch 계열을 뺀 고정 버전 68개만 설치한 `/tmp/venv-ch05-llm-principles`, `UV_NO_SYNC=1`, `TRANSFORMERS_NO_ADVISORY_WARNINGS=1`(torch 없음 조언 경고만 끔). 01 노트북은 torch를 쓰지 않음.
- 커널 작업 폴더 두 경우(프로젝트 맨 위, `notebooks`) 출력 동일. `labs/part1/ch04-data-tools/data/article-text.json` SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1` 유지.
- `verify.py --chapter` PASS 8 sections / 44 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-01.json`). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/01-diagnosis.md`, `qa/upgrade/01-figures.md`.

## 품질 개선 02 임베딩과 의미 유사도 (2026-09-16)

- 새 커널 실행 PASS: `02-임베딩과-의미-유사도.ipynb` 코드 셀 13개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2, sentence-transformers 5.1.1, numpy 2.3.3. 임베딩 모델 `encode()` 5번(내 컴퓨터), API 호출 0번. 네 번 실행해 출력 글자 동일.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동). 같은 환경에서 01절을 다시 실행해 코드 셀 출력 `outputs_sha256` `060a9d48…`이 처음 실행과 같음을 확인.
- `verify.py --chapter` PASS 8 sections / 52 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-02.json`). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/02-diagnosis.md`, `qa/upgrade/02-figures.md`.

## 품질 개선 03 어텐션 직관 (2026-09-16)

- 새 커널 실행 PASS: `03-어텐션-직관.ipynb` 코드 셀 17개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`, `attn_implementation="eager"`) 계산 2번, API 호출 0번. 두 번 실행해 `outputs_sha256` `2aa3ccaf…` 동일.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동).
- `verify.py --chapter` PASS 8 sections / 66 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-03.json`, 수정 전 25건). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/03-diagnosis.md`, `qa/upgrade/03-figures.md`.

## 품질 개선 04 컨텍스트 윈도 (2026-09-16)

- 새 커널 실행 PASS: `04-컨텍스트-윈도.ipynb` 코드 셀 15개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`) `generate()` 2번(입력 400조각, `max_new_tokens` 64·8, `do_sample=False`), API 호출 0번. 두 번 실행해 `outputs_sha256` `974b9fe0…` 동일. 노트북과 같은 계산의 `ru_maxrss` 약 3.3GB.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동).
- `verify.py --chapter` PASS 8 sections / 77 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-04.json`, 수정 전 22건). `visual.cjs` 1280·390px PASS(이 절 HTML). 03절 `_src` b7 한 문장을 고친 뒤 03 게이트도 다시 0.
- 진단·그림 기록: `qa/upgrade/04-diagnosis.md`, `qa/upgrade/04-figures.md`.

## 품질 개선 06 temperature와 샘플링 (2026-09-16)

- 새 커널 실행 PASS: `06-temperature와-샘플링.ipynb` 코드 셀 14개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`) `generate()` 16번(입력 56조각, `max_new_tokens` 32, 뽑기를 끈 답 1 + `do_sample=True`·temperature 0.3·1.0·top_p 0.9·시드 11~55 10 + 같은 시드 다시 5), temperature 0.0 호출은 생성 전 `ValueError`, API 호출 0번. 두 번 실행해 `outputs_sha256` `df95f660…` 동일. 노트북과 같은 계산의 `ru_maxrss` 약 3.2GB.
- 노트북 밖 확인: Linux x86_64에서 같은 버전으로 답 11개 같음, torch 2.5.1+cpu로 바꾸면 시드 답 10개 모두 다름(`qa/upgrade/06-diagnosis.md` 「실행 환경」).
- `verify.py --chapter` PASS 8 sections / 93 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-06.json`, 수정 전 53건). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/06-diagnosis.md`, `qa/upgrade/06-figures.md`.

## 품질 개선 07 환각의 구조적 원인 (2026-09-16)

- 새 커널 실행 PASS: `07-환각의-구조적-원인.ipynb` 코드 셀 14개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`) `generate()` 12번(`max_new_tokens` 64, 모두 `do_sample=False`: 근거 없는 질문 2, 「가상」 뺀 질문 2, 답 첫머리 2, 근거 문서 2, 보류 지시 문서 없음 2·있음 2), API 호출 0번. 두 번 실행해 `outputs_sha256` `f6b8bcc8…` 동일. 같은 계산의 `ru_maxrss` 약 3.2GB.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동).
- `verify.py --chapter` PASS 8 sections / 102 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-07.json`, 수정 전 33건). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/07-diagnosis.md`, `qa/upgrade/07-figures.md`.

## 품질 개선 08 모델 선택 기준 (2026-09-16)

- 새 커널 실행 PASS: `08-모델-선택-기준.ipynb` 코드 셀 17개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`)와 `HuggingFaceTB/SmolLM2-135M-Instruct`(revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, 이 절에서 새로 받음) `generate()` 16번(`max_new_tokens` 64, 모두 `do_sample=False`: 두 모델 × 한국어 평가 자료 4·영어 평가 자료 4), API 호출 0번. 답 글은 같은 코드의 기기 셸 스크립트와 같고, 시간 값은 실행마다 달라 `outputs_sha256` 반복 일치는 확인하지 않음. 같은 계산의 최대 RSS 약 3.4GB.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동).
- `verify.py --chapter` PASS 8 sections / 115 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-08.json`, 수정 전 34건). `visual.cjs` 1280·390px PASS(이 절 HTML).
- 진단·그림 기록: `qa/upgrade/08-diagnosis.md`, `qa/upgrade/08-figures.md`.

## 품질 개선 09 LLM 동작 원리 실습 (2026-09-16, 챕터 끝 실습 절 새로 만듦)

- 새 커널 실행 PASS 두 번: `09-LLM-동작-원리-실습.ipynb` 코드 셀 15개, Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2, sentence-transformers 5.1.1. 내 컴퓨터의 `Qwen/Qwen2.5-0.5B-Instruct`(revision `7ae557604adf67be50417f59c2c2f167def9a775`) `generate()` 4번(`max_new_tokens` 64, 모두 `do_sample=False`)과 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`(revision `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`) `encode()` 5번, API 호출 0번. 두 실행의 `outputs_sha256` `981329b4…` 같음. 같은 계산의 최대 RSS 약 3.2GB.
- 실행 환경: 전체 가상환경 `.cache/vm/venv-ch05-llm-principles`와 모델 캐시 `.cache/vm/hf`(`run_section.sh` 자동, 새로 받은 모델 없음).
- `verify.py --chapter` PASS 9 sections / 130 code cells. 품질 게이트 G1~G7 0(`qa/upgrade/gates-wip-09.json`), 08절도 문장 수정 뒤 0. `visual.cjs` 08·09·index 1280·390px PASS.
- 진단·그림 기록: `qa/upgrade/09-diagnosis.md`, `qa/upgrade/09-figures.md`.

## 검토 1차 반영과 챕터 마감 (2026-09-16)

- 검토 A(01~05) 중 4·하 19, 검토 B(06~09) 중 4·하 15를 모두 반영(각 보고서 끝 「반영 결과」).
- 새 커널 실행: 02 `02-임베딩과-의미-유사도.ipynb` 코드 셀 13(두 번 PASS, 출력 글자 같음, `outputs_sha256` `e1676185…`/`f43ffa90…` — stdout 조각 수 차이), 03 `03-어텐션-직관.ipynb` 코드 셀 19(두 번 PASS, `outputs_sha256` `fb798b7e…` 같음). 반영 전 셀의 출력 글자는 두 절 모두 같음. Linux aarch64, Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2, sentence-transformers 5.1.1. 03 심화 셀은 기존 모델 계산 결과를 다시 써서 모델 계산 2번 그대로.
- 01·04~09는 `mdpatch.py` 방식 치환 + `run_section.sh … --no-exec`(노트북 출력·해시 그대로).
- 기기 셸 확인(노트북 밖, 본문에 표시): MiniLM 특수 토큰까지 평균(차이 0.0)·128 한도 포함(`[1, 128]`), 05 조건 9개 `repetition_penalty=1.0`(`2 | 2`만 True로 바뀜), 06 시드 재현 스크립트 `qa/upgrade/evidence/06_seed_platform.py` 11/11.
- 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `qa/upgrade/gates-after.json`, 수정 전 262건). `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`. `visual.cjs` 9절+목차 × 1280·390px 20건 PASS. review-pack 9개 갱신.
- `labs/part1/ch04-data-tools/data/article-text.json` SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1` 전후 같음.
- 옛 생성기 두 파일은 실행 막음 줄을 넣고 `qa/upgrade/before/generators/`로 옮김. 챕터 요약 `qa/upgrade/chapter-summary.md`.

## §2-7 리팩터 (2026-09-21)

- 대상: 02·03·06·07·08·09(01·04·05는 코드 변경 없음). 도구 파일 `labs/part1/ch05-llm-principles/notebooks/llm_tools.py`(함수 6개), 리팩터 직전 스냅숏 `qa/upgrade/before-2-7/`.
- 새 커널 실행: 바뀐 절마다 `run_section.sh` 두 번(A·B), 셀별 출력 글자 대조 → 08 시간 값 6개 외 모두 같음. 리팩터 전 노트북과 대조 → 모델 답·유사도·비중·판정 모두 같고, 03 NumPy 배열 모양 4줄과 08 시간 값만 다름. 묶음을 풀어 노트북 폴더에서 09를 한 번 더 실행해 같음.
- 게이트 `upgrade_gates.py --label after-2-7` 9/9 PASS(G1~G7 0). `verify.py --chapter` PASS(9절·코드 셀 119). 빌드 HTML `{{` 0건. `visual.cjs` 02·03·06·07·08·09 × 1280·390px 12건 PASS.
- 다시 렌더한 그림: 02-3(라벨 `@ 점곱`)·03-1(라벨 `@ 점곱`·`@ 가중합`, 배열 모양)·08-3(답 시간). PNG 직접 확인.
- 코드 셀 132 → 119, 코드 줄(주석·빈 줄 제외) 1033 → 911. 서비스 모델 요청 0번.
- 묶음: `part1-practice.zip` 다시 만듦(40절·66파일, `llm_tools.py` 포함). `check_delivery.py`는 81행(Ch1 06 실습 절 시수 meta)에서 멈춤 — 전체 마감 몫.
