# 04-컨텍스트-윈도 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/04-concept.*`).
생성기: `qa/upgrade/author_04.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 04`(환경 변수 없이).
수정 전 수치는 01절 작업 때 남긴 챕터 기록 `gates-before.json`의 04절 값입니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 2 | 0 |
| G3 | 1 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 10 | 0 |
| G7 | 3 | 0 |
| 합계 | 22 | 0 |
| 코드 셀 | 4 | 15 (준비 1 + 본문 14, 함수 정의 셀 2개) |
| 검사한 문장 | 77 | 379 (`gates-wip-04.json`) |
| 모델 실행 | 없음(토큰화기만) | 내 컴퓨터의 Qwen2.5-0.5B-Instruct `generate()` 2번(입력 400조각, 출력 몫 64·8), API 호출 0, 비용 0 |

## 실행 환경

- 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`(`Qwen/Qwen2.5-0.5B-Instruct`@`7ae557604adf67be50417f59c2c2f167def9a775`). `run_section.sh`가 자동으로 씀.
- 새 커널 실행 PASS(`PASS 04-컨텍스트-윈도.ipynb: 15 cells`, `run_section.sh` 전체 약 13~15초). 코드를 마지막으로 고친 뒤 두 번 실행해 `outputs_sha256`(`974b9fe0…`)이 같았습니다. 그 전 실행(끝 글자 수 52, 두 겹 호출이 남은 판)과도 숫자·답 문장이 같았습니다.
- 메모리: 노트북 코드 셀을 기기 셸에서 스크립트(`/tmp/ch05-04/cells.py`)로 실행했을 때 `ru_maxrss` 3,327,744KiB(약 3.3GB). 어텐션 출력은 켜지 않았고, 모델에 넣은 가장 긴 입력은 400조각입니다(80번 반복 1480조각은 토큰화기만). 기기 메모리 3.8GB에서 실행됨. 루트 여유 약 578MB(변화 없음).
- `verify.py --chapter` `PASS 8 sections / 77 code cells (max 17 lines)`(17줄은 개선 전 다른 절). `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-04/vis`에 03절 작업자의 사본 복사, 공용 도구는 고치지 않음).

## 수정 전 주요 문제

- Ch 1~4·01~03절에서 가르치지 않은 문법: 목록 곱하기로 문서 만들기(`"…" * 20`, 01절은 `for`와 `+`), f-string 형식 지정 `{output_budget:3}`, `sum(counts.values())`, `assert A and B`와 `448 < full_counts[40]` 연쇄 비교, 한 셀 15줄 넘음·두 겹 호출(G2 2건), 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」 3곳, 첫 줄 주석 없는 검증 셀(G3)
- 제목 셀·준비물·핵심 그림·결과 읽기 없음(G5 6건). 설명 셀이 `parts`·`messages`·`encode()`로 문장 시작(G6 english_start 3건), 70자 넘는 문장 6개, 5문장 넘는 단락 1개
- 옛 도식 캡션이 그림에 없는 「보라색은 모델의 처리, 빨간색은 확인할 제한」을 설명(01~03절 옛 도식과 같은 문제). Mermaid 0, 삽화 0, 설계표 없음(G7 3건)
- 실행하지 않은 동작을 사실처럼 씀: b7 「출력 토큰을 예약하지 않으면 응답이 중간에 끊길 수 있습니다」(생성을 실행하지 않음), b4 「한도를 넘는 입력은 무조건 뒷부분을 잘라 해결하지 않습니다 … 뒷부분에 현재 질문이 있을 수 있고」(자르기를 실행하지 않음). 실습용 한도 512와 모델의 실제 한도의 관계, 설정 값 두 가지(`max_position_embeddings`·`model_max_length`)가 없음
- 「앞에서 배운 내용」이 개선 전 03절 기준(「입력 토큰 사이의 관계를 반영하는 어텐션 직관」) — 03 handoff 인계 사항. `tokenize=True`와 `encode()` 결과가 같은지 확인 없음. 복습 3문항에 난이도 표시 없음. 준비물 셀이 모델 다운로드를 말하나 노트북은 토큰화기만 씀

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「모델에 넣을 수 있는 토큰 예산은 입력과 출력 사이에서 어떻게 나눌까요?」의 뜻, 환불 문장·시스템 지시·질문·연습용 한도 512·출력 몫 32·64·128·반복 10·20·40·80 유지): 제목(할 일 3, 생성 2번·비용 0·2분 안팎, 모델 파일 약 1GB·메모리 약 3.3GB, transformers 4.56.2·torch 2.8.0·모델·revision) → 오늘 볼 그림(04-1) → 1 준비(`warnings`·`transformers.logging.set_verbosity_error()`·버전) → 2 모델·토큰화기 받기(03절 모양, eager 없음), `max_position_embeddings: 32768`·`model_max_length: 131072` → 3 세 부분 글(문서는 `for`+`+` 20번, 500글자)·토큰 수 12·360·15·합 387(딕셔너리 `items()`) → 4 메시지 목록·`apply_chat_template(tokenize=False, add_generation_prompt=True)` 앞 70·끝 50글자 → `encode()` 400·사용자 메시지 375·늘어난 13 → 앞 세 조각·끝 다섯 조각 → 5 값 바꿔 보기 시스템 메시지 빼기(예상 383 → 실제 404, 영어 기본 지시) → 6 예산 표 `32 | 480 | 80`·`64 | 448 | 48`·`128 | 384 | -16` → 7 `make_document()`·`make_input_text()` 정의, 반복 10·20·22·23·40·80 → 220·400·436·454·760·1480 → 8 40번 입력 760조각의 앞·뒤 448조각 남기기(`앞 448조각 | True | False | False`, `뒤 448조각 | False | True | True`) → 9 `encode(…, return_tensors="pt")`·`generate(max_new_tokens=64, do_sample=False)` 새 조각 18·끝 표시 True → 10 값 바꿔 보기 출력 몫 8(새 조각 8, `답: 환불은 결제일로부터`, False) → 정리
- 기본 경로에서 목록 곱하기·f-string 형식 지정·`sum`·`max`·`**` 풀기·목록 `+` 잇기·`import torch`·`tokenizer(글)` 객체 호출·`assert A and B`를 쓰지 않음. 함수 두 개는 타입힌트 없이 셀 하나에 하나, 정의·호출 분리. 두 겹 호출은 중간 변수로 풂
- 모델 생성을 넣은 판단: 개선 전 b7의 「응답이 끊길 수 있다」를 실제 조건(출력 몫 8)으로 재현. 05절(개선 전)이 `generate(do_sample=False)`를 쓰므로 그 앞에서 가장 작은 모양(`input_ids=`·`max_new_tokens`·`do_sample=False`)만 소개. 샘플링·temperature는 06절로 넘김
- 본문 10블록 전체를 다시 씀: 이 절의 질문 두 개(어떻게 나누나 / 넘치거나 모자라면 무엇이 사라지나), b3 01·03절 개선본 기준(03 handoff 인계: 03은 21 × 21 비중 표·뒤 조각을 보지 않음·생성은 하지 않음), 비유(칸막이 쟁반: 01-5 블록 쟁반을 이어 씀), 용어 7개 표, 세 부분과 표시 → 출력 몫 먼저 빼기(말 → 식 → 숫자) → 넘치는 입력 개념(Ch 8 02 Select·03 Compress 연결, `_src` b1에서 이름 확인), 실행 예제 해설(설정 값 두 가지, 템플릿, 기본 지시 404, 반복 수, 생성 둘), 실험 해석(입력 쪽·출력 쪽, 결론 두 가지, 범위: 모델 하나·연습용 문서·512, 32768 근처 긴 입력과 자른 입력의 생성은 실행 안 함), 주의 메모 7개, 복습 5문항(기초 2·적용 1·분석 2)
- 라이브러리 동작 확인(설치본 transformers 4.56.2): `generation/utils.py` 2078행 어텐션 마스크 안내는 `logger.warning_once`, 797~817행 `_prepare_attention_mask_for_generation`은 입력에 채움 조각(151643)이 없으면 모든 자리 1인 기본 마스크, 1252행 `if generation_config.do_sample:`일 때만 temperature·top-k·top-p 처리기를 붙임, `generation/configuration_utils.py` 757행 「The following generation flags are not valid」도 logger 경고(그래서 `set_verbosity_error()`로 꺼짐). 토큰화기 설정 파일 `chat_template`: 첫 메시지가 system이 아니면 `You are Qwen, created by Alibaba Cloud. You are a helpful assistant.`를 넣음. 설정 `config.json` `max_position_embeddings: 32768`, `tokenizer_config.json` `model_max_length: 131072`. 모델 카드(판 7ae5576 README, 2026-09-16 확인): 「Context Length: Full 32,768 tokens and generation 8192 tokens」, 시리즈 소개 「Long-context Support up to 128K tokens」
- 기기 셸 탐색(`/tmp/ch05-04/probe3.py`)으로 확인하고 본문에 반영한 것: 채팅 템플릿 입력 = 앞 표시 3 + 시스템 12 + 사이 표시 5 + 사용자 375 + 끝 표시 5(조각 ID 목록 일치), `apply_chat_template(tokenize=True)` 결과와 `encode(tokenize=False 글)` 결과가 같음(400, 목록 동일), 반복 1~29번 입력 = 40 + 18 × 반복 수
- 03절 `_src` b7 한 문장 고침(04절이 생성을 처음 하게 되어): 「모델이 글을 만들어 내는 실행은 06절」 → 「04절에서 처음 합니다. 조각을 고르는 방식은 06절에서 다룹니다」. 03 게이트 다시 0 확인, 03 리뷰 묶음 다시 만듦, `03-diagnosis.md` 끝에 기록
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/04-concept.*`는 본문에서 뺌(원본 `before/figures/`, 옛 파일은 삭제하지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 04-1 TB(초록 한도·출력 몫 → 노랑 입력 한도, 노랑 세 가지 조각 → 노랑 템플릿 입력, 두 갈래 → 노랑 남는 칸). 04-2 xychart 막대(노랑)+선(초록 448), 23번 막대가 선 바로 위라 도식 읽기에 「6조각만 높아 붙어 보임」을 적음. 04-3 TB 처음 렌더에서 `질문 False · 답 시작 표시 False`가 어색하게 접혀 `<br>`로 세 줄로 나눔(다시 렌더해 확인). 04-4 TB 보라 모델 아래 두 갈래
- 색: 정한 값(512·64·448 선) 초록, 출력 조각 수 노랑, 실행한 모델 보라, 잘려 나간 부분 회색, 빨강 없음. 메서드는 화살표 라벨
- 삽화 04-5(칸막이 쟁반): 1회차 job `d5de3e4a-9b3e-4fa4-a7ad-3e2297557b7f` 채택, 2크레딧(생성 전 잔액 2892). 쟁반 밖 블록이 요청 3개 → 결과 4개(뜻 없는 개수라 채택, 그림 읽기는 4개로 씀). 저장 PNG(1100×614)를 기기에서 다시 받아 채택 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0

## 검토에서 볼 곳

- 생성(`generate()`)을 04절에 넣은 판단과 03 b7 고침. 새 API(`apply_chat_template`·`max_position_embeddings`·`model_max_length`·`generate`·`max_new_tokens`·`do_sample`·`transformers.logging.set_verbosity_error()`)의 설명 수준. 안내 경고 두 줄을 끄고 9절 결과 읽기·b7에서 소스 근거로 설명한 방식이 초보자에게 괜찮은지
- 「출력 몫」은 교재에서 정한 이름(용어 표에 적음). 「역할 표시 13」에 줄바꿈 조각이 섞여 있다는 설명 수준(4절 결과 읽기). `model_max_length: 131072`를 모델 카드 시리즈 소개의 128K와 같은 수로만 적고 까닭은 추정하지 않음
- 결론 범위: 자르기는 토큰 ID 목록 슬라이싱(교재 코드)으로 본 것이고 라이브러리의 잘라내기 옵션은 실행하지 않음. 답이 끊긴 관찰은 한 입력·한 번 실행. meta는 개선 전 「강의 1h · 실습 0.5h」 유지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept(중 0, 하 3). 모두 반영했습니다.
- 04-1: b2 「한도를 넘는 입력은 누군가 잘라야 들어갑니다. 어느 쪽을 자르느냐에 따라 질문이나 지시가 빠질 수 있고, 답에 쓸 칸이 모자라면 …」, b7에 「한도를 넘는 입력을 자르지 않고 모델에 넣는 경우는 이번에 실행하지 않았습니다」 항목
- 04-2(결정: 05절이 32768을 쓰는 까닭 한 문장): [7] 새 단락과 b5 「두 곳이 같은 값을 적었으므로, 05절부터는 32768을 이 모델의 전체 한도로 씁니다. 131072에 가까운 입력은 이번에 실행하지 않았습니다.」
- 04-3: 그림 04-1 라벨 「템플릿 표시 13」, alt·노트북 [1]·도식 읽기, 4절 예상 「채팅 템플릿의 표시가」. 다시 렌더 PNG 확인
- C-2: 그림 04-2 「주황 막대」, 설계표. C-4(결정): 용어 표 출력 몫 뜻 칸 끝 「Ch 6에서는 같은 뜻의 값을 출력 상한, Ch 8 01절에서는 출력 예약분이라고 부름」(Ch 6 01 `_src` 38행 「출력 상한」, Ch 8 01 `_src` 39행 「출력 예약분 (output reservation)」 확인). Q4: b7 `set_verbosity_error()` 항목에 「이 노트북의 뒤 셀 전체에서」
- 재실행 없음. 코드 셀 15, `outputs_sha256` `974b9fe0…` 그대로, 검사한 문장 386

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/04-컨텍스트-윈도.md`
- 정리 대상(삭제하지 않고 목록만): `figures/04-concept.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-04`(탐색 스크립트·visual 사본·cells.py)
- 챕터 안 옛 생성기 `make_sources.py`와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않았습니다(개선본을 덮어씀)
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음
- 05절(개선 전) `_src` b3 「앞 절에서 연습용 컨텍스트 예산 512토큰을 계산」·`max_position_embeddings` 32,768은 개선된 04와 맞음. 05 작업자가 04의 `generate()` 모양과 이어 씀
