# 05-컨텍스트-로트 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/05-concept.*`).
생성기: `qa/upgrade/author_05.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 05`(환경 변수 없이).
수정 전 수치는 01절 작업 때 남긴 챕터 기록 `gates-before.json`의 05절 값입니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 1 | 0 |
| G3 | 2 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 10 | 0 |
| G7 | 3 | 0 |
| 합계 | 23 | 0 |
| 코드 셀 | 5 | 13 (준비 1 + 본문 12, 함수 정의 셀 4개) |
| 검사한 문장 | 79 | 338 (`gates-wip-05.json`) |
| 모델 실행 | `generate()` 18번(9조건 × 2) | 내 컴퓨터의 Qwen2.5-0.5B-Instruct `generate()` 27번(시스템 메시지 없음 9 + 같은 입력 다시 9 + 04절 시스템 지시 9), API 호출 0, 비용 0 |

## 실행 환경

- 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`(`Qwen/Qwen2.5-0.5B-Instruct`@`7ae557604adf67be50417f59c2c2f167def9a775`). `run_section.sh`가 자동으로 씀. `/tmp`에 torch 설치 없음.
- 새 커널 실행 PASS(`PASS 05-컨텍스트-로트.ipynb: 13 cells`, `run_section.sh` 전체 약 77~81초). **반복 확인**: 코드를 마지막으로 고친 뒤 새 커널로 두 번 실행해 `outputs_sha256` `642f2147…`이 같았고, 출력 글 46줄도 `diff`로 같았습니다. 그 전 실행 1회와 기기 셸 스크립트(`/tmp/ch05-05/cells.py`) 실행의 표·답 문장도 같았습니다. 노트북 안에서도 7절이 같은 입력 9개를 다시 실행해 `같은 답 수: 9 / 9`.
- 메모리(기기 셸 스크립트): 모델을 float32로 올리는 순간 `ru_maxrss` 약 3.24GB, 올린 뒤 기준 VmRSS 약 2.30GB, 생성 중 최대 VmRSS 는 95조각 약 2.86GB·1197조각 약 3.19GB·2337조각 약 3.16GB(20ms 표본). **약 3,500조각(무관한 문장 180개) 입력은 프로세스가 강제 종료(종료 코드 137, 메모리 부족)** → 가장 긴 입력을 개선 전과 같은 1201조각으로 둠. 생성 시간은 1201조각 한 번 약 3.5~5초.
- `verify.py --chapter` `PASS 8 sections / 85 code cells (max 17 lines)`(17줄은 개선 전 다른 절). `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-05/vis`에 04절 작업자의 사본 복사, 공용 도구는 고치지 않음). 루트 여유 약 569MB.

## 수정 전 주요 문제

- Ch 1~4·01~04절에서 가르치지 않은 문법: 목록 곱하기 `[filler] * repeats`, `items.insert()`, `"\n".join()`, 몫 연산 `//`, 딕셔너리 즉석 인덱싱 `{...}[position]`, f-string 형식 지정 `{repeats:2}`, `for _ in`, `max()`, `32_768`, `*` 키워드 전용 인자와 타입힌트 `-> str`, `**inputs`, `with torch.inference_mode()`, `tokenizer(글)` 객체 호출, `skip_special_tokens`·`pad_token_id`·`model.eval()`·`num_parameters()`·`f"{n:,}"`. 한 셀 15줄 넘음(G2), 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」 3곳, 첫 줄 주석 없는 셀 2개(G3)
- 제목 셀·준비물·핵심 그림·결과 읽기 없음(G5 7건). 설명 셀이 `generate()`·`model.config…`·`hits=0/2`로 문장 시작(G6 english_start 4건), 70자 넘는 문장 5개, 5문장 넘는 단락 1개
- 옛 도식 캡션이 그림에 없는 「파란색·빨간색」을 설명(01~04절 옛 도식과 같은 문제). Mermaid 0, 삽화 0, 설계표 없음(G7 3건)
- 입력 모양이 결과를 바꾼다는 사실을 몰랐음: 개선 전 입력은 사용자 메시지 하나라 04절에서 확인한 영어 기본 지시가 들어간 상태였음. 이 절에서 04절 시스템 지시를 넣자 9조건 모두 정답(기기 셸 탐색 `/tmp/ch05-05/probe1.py`). 개선 전 결론 「중간 위치는 세 길이 모두 0/2」를 입력 모양 하나의 결과로만 쓸 수 있음
- 복습 3문항에 난이도 표시 없음, 「앞에서 배운 내용」이 개선 전 04절 기준(512 예산만)

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「근거 문장의 위치와 주변 문장 수가 답에 어떤 차이를 만들까요?」 유지, 개선 전 데이터 — 근거 「해바라기 작전의 확인 코드는 314159입니다.」·무관한 문장 「주문 조회 화면에는 결제 상태와 배송 상태가 표시됩니다.」·질문 「해바라기 작전의 확인 코드만 답하세요.」·무관한 문장 2·20·60개 × 앞·가운데·끝·같은 입력 두 번·사용자 메시지 하나 입력 — 유지): 제목(할 일 3, 생성 27번·비용 0·2분 안팎, 모델 파일 약 1GB·메모리 약 3.2GB, transformers 4.56.2·torch 2.8.0·모델·revision) → 오늘 볼 그림(05-1) → 1 준비(04절과 같은 `warnings`·`set_verbosity_error()`·버전) → 2 모델(03·04 모양)·`output_budget = 32`·입력 한도 32736(04절 식) → 3 재료 토큰 수 19·19·13 → 4 `make_document(filler_count, fact_place)` 정의(`for`+`if`+`+`)·작은 문서 `make_document(2, 1)` → 5 `make_input_without_system()` 정의·조건 9개와 입력 토큰 수 99·441·1201·한도 이하 True → 6 `ask_model()` 정의(04절 9절 모양)·9조건 실행(가운데 3개·끝 2개 조건 False) → 7 같은 입력 다시 `같은 답 수: 9 / 9` → 8 값 바꿔 보기 `make_input_with_system()`(04절 시스템 지시)·지시 확인 표·9조건 모두 True → 정리
- 기본 경로에서 목록 곱하기·`insert`·`join`·`//`·f-string 형식 지정·`for _`·`max`·`sum`·`zip`·`**` 풀기·`import torch`·`with`·`tokenizer(글)`·`Path`·`raise`·내포식·`try/finally`·상속·`threading`·`@`·`BaseModel`·`*args`를 쓰지 않음. 가운데 자리는 `int(filler_count / 2)`(Ch 2 01 `int()`), 조건은 세 칸 목록을 `for a, b, c in conditions:`로 풀어 담기(Ch 2 03). 함수 네 개는 타입힌트 없이 셀 하나에 하나, 정의·호출 분리. `print(len(encode()))` 두 겹 호출은 중간 변수로 풂
- 값 바꿔 보기로 04절 시스템 지시를 넣은 판단: 04절에서 이어 온 입력 모양이고, 기기 셸 탐색에서 결과가 크게 달라져 「작은 모델 하나의 위치 결과를 일반화하지 않는다」를 노트북 출력으로 보일 수 있음. 반복 실행은 가장 결과가 갈린 시스템 메시지 없는 입력에 둠
- 본문 10블록 전체를 다시 씀: 이 절의 질문 두 개(한도 안에서도 자리·주변 문장 수로 답이 달라지나 / 다른 모델·입력에도 말할 수 있나), b3 01·03·04절 개선본 기준(04의 채팅 템플릿·출력 몫·입력 한도·기본 지시·가장 긴 입력 400, 03의 「비중으로 근거를 말할 수 없다」), 비유(세 쟁반: 01-5·04-5 쟁반을 이어 쓰되 블록 = 문장), 용어 6개 표, 두 값만 바꾸기 → 글자 판정 → 한도 안의 차이와 04절 잘림 구분, 실행 예제 해설(크기, 자리, 결과, 다시 실행), 실험 해석(길이 1·2·2개로 줄지 않음, 자리, 값 바꿔 보기, 결론 두 가지, 범위, Liu 외 2023·Chroma 2025 보고와 대조), 주의 메모 8개, 복습 5문항(기초 2·적용 1·분석 2)
- 참고 자료 확인(2026-09-16 웹): Lost in the Middle 초록 「performance is often highest when relevant information occurs at the beginning or end … significantly degrades … in the middle of long contexts」, Chroma Context Rot(2025-07-14) 모델 18개·「performance grows increasingly unreliable as input length grows」·한 NIAH 과제에서 근거 위치 11곳 간 뚜렷한 차이 없음. 본문은 이 범위만 인용
- 기기 셸에서만 확인하고 본문 주의 메모에 「노트북에 넣지 않음」으로 적은 것: 질문 앞 줄바꿈을 하나 더 넣으면(빈 줄 두 줄) 시스템 메시지 없는 `2 | 2` 조건이 `314159<|im_end|>`로 바뀜(`/tmp/ch05-05/probe1.py`, 출력 몫 20), 약 3,500조각 입력의 강제 종료
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/05-concept.*`는 본문에서 뺌(원본 `before/figures/`, 옛 파일은 삭제하지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 05-1 TB(초록 재료 세 개·문서 → 노랑 입력 → 보라 모델 → 노랑 판정), 05-2 LR 세 줄(초록 근거·회색 무관한 문장 묶음, 줄마다 왼쪽 → 오른쪽), 05-3 TB(노랑 입력 → 보라 모델 → 노랑 첫 실행·다시 실행 두 갈래), 05-4 TB(초록 같은 조건 → 노랑 두 결과). viewBox 폭 430·629·439·473으로 모두 860 미만
- 05-4는 처음 xychart-beta(막대 3·0·2 + 선 3·3·3)로 렌더했으나 세로축이 0.2 간격 소수 눈금이라(조건 수는 정수) flowchart로 바꿔 다시 렌더
- 색: 만든 문장·문서·같게 둔 조건 초록, 입력 조각 수·판정·결과 노랑, 실행한 모델 보라, 무관한 문장 묶음 회색, 빨강 없음(False도 출력으로 확인한 결과). 메서드·함수는 화살표 라벨
- 삽화 05-5(세 쟁반): 1회차 job `97e322bd-1c60-4633-abab-0fccd5855d82` 채택, 2크레딧(생성 전 잔액 2890). 요청 칸 11개 → 결과 9개(가운데 자리가 정확히 다섯째 칸이라 관계가 그대로 읽혀 채택, 그림 읽기는 9칸으로 씀). 저장 PNG(1100×614)를 기기에서 다시 받아 채택 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0

## 검토에서 볼 곳

- 주 실행을 개선 전과 같은 「사용자 메시지 하나」 입력으로 두고, 04절 시스템 지시를 값 바꿔 보기로 둔 순서. 결론을 「자리에 따른 차이가 입력 모양에 따라 나타나거나 사라짐」으로 둔 범위(6절 결과 읽기, b6, b8, 복습 4·5)
- 정답 판정 규칙(글자 포함)과 그 한계 메모(「314159가 아닙니다」도 True, 실행하지 않은 예), 반복 실행을 「우연이 아님」까지만 쓰고 실패율로 쓰지 않은 설명
- Chroma·Liu 외 인용 수준(b6 마지막 단락), 주의 메모의 「줄바꿈 하나 더」·「3,500조각 강제 종료」가 노트북 밖 기기 셸 관찰이라는 표시. meta는 개선 전 「강의 1h · 실습 1h」 유지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept-with-fixes(중 1, 하 3). 모두 반영했습니다.
- 05-1(중, 결정: 입력 길이 기준 정의): b2를 두 단락으로(「입력이 길어질수록 … 나빠질 수 있습니다. 이런 현상을 컨텍스트 로트」, 「정보가 입력의 가운데 있을 때 결과가 나빠진다는 보고도 따로 있습니다」, 「이 절은 입력 길이와 정보의 자리를 함께 바꿔 봅니다」), 용어 표(뜻 입력 길이 기준·긴 회의록일수록, 보이는 모습 「이번 99~1201조각에서는 정답 수가 줄지 않음」), b4 「가운데에서 잃어버림(lost in the middle)」 한 문장(새 용어 수 6 유지), b6 범위 단락 첫 문장 「이 노트북이 본 것은 길이에 따른 저하, 곧 컨텍스트 로트가 아니라 근거의 자리에 따른 차이입니다」. Chroma 보고서·Ch 8 05 `_src` 24행 정의와 같음
- 05-2(결정: 반복 벌점 1.1 한 줄): b7 새 항목. 마감 세션 기기 셸에서 조건 9개를 `repetition_penalty=1.0`으로 다시 만들어 확인: `2 | 2`만 `314159<|im_end|>`(True)로 바뀌고 가운데 세 조건은 그대로 False, 나머지는 True. 가운데 `20 | 10` 답 글자는 「…표시되지 않습니다」에서 「…표시됩니다」로 바뀌어, 검토 A 기록 「같은 틀린 답」과 달라 본문은 「그대로 틀렸습니다」로만 씀. 06 b7 셋째 항목 끝에 「05절 주의 메모에 있습니다」를 더해 서로 가리킴
- 05-3: 삽화 그림 읽기 둘째 단락(문서·문장, 쟁반 밖 블록 없음 = 잘린 문장 없음, 칸이 찬 정도는 한도 비율이 아님, 출력 몫 칸막이는 그리지 않음)
- 05-4: 참고 자료 원제목 「Lost in the Middle: How Language Models Use Long Contexts」(TACL, arXiv 페이지 확인)·「Context Rot: How Increasing Input Tokens Impacts LLM Performance」(Chroma 페이지 제목 확인), 제목은 `<div>` 줄
- Q5: 6절 설명 「시스템 메시지 없는 입력 모양은 결과를 보기 전에 정해 둔 모양입니다.」
- 재실행 없음. 코드 셀 13, `outputs_sha256` `642f2147…` 그대로, 검사한 문장 347

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/05-컨텍스트-로트.md`
- 정리 대상(삭제하지 않고 목록만): `figures/05-concept.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-05`(탐색 스크립트·cells.py·visual 사본·출력 비교 글)
- 챕터 안 옛 생성기 `make_sources.py`와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않았습니다(개선본을 덮어씀)
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음
- 06절(개선 전) `_src` b3 「04절과 05절에서는 모델이 받을 수 있는 입력 길이와 긴 문맥에서의 관찰 범위를 구분했습니다」는 06 작업자가 개선된 05 기준으로 고칠 곳(handoff에 적음)
