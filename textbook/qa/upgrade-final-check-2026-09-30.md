# 교재 품질 개선 전체 점검 (2026-09-30)

읽기 전용 · 노트북 재실행 0 · 모델 요청 0

점검 범위: 품질 개선 대상 32챕터(Ch 1~31, Ch 34 — Ch 22는 시범 챕터), 제외 2챕터(Ch 32·33, 사용자 결정). 기준 시각은 기기 셸 시계(UTC)이며, 이 보고서 한 파일 말고는 어떤 파일도 고치지 않았습니다(임시 파일은 기기 `/tmp/finalcheck/`에만 만듦).

## 요약

| 항목 | 결과 | 문제 수 |
|---|---|---|
| 1. 챕터와 상태 | 교재 폴더 34챕터. 대상 32챕터 236절 모두 진행표 「완료」(30개 「강사 확인 대기」, Ch 22 「완료(강사 확인)」), Ch 32·33은 「대기」·「제외(사용자 결정)」 | 2 — Ch 22 `chapter-summary.md` 없음 · Ch 1 요약에 「강사 확인」·「남은 것」 절 없음 |
| 2. 게이트 G1~G7 | `check_section()` 직접 호출로 236/236절 PASS, G1~G7 합 0, 코드 셀 5,282 · 검사 문장 88,781 | 0 (기록과 문장 수만 다른 절 2 — 설명 가능) |
| 3. 노트북 검증 흔적 | 236개 노트북 모두 `metadata.verification` 있음, `status` passed, `code_sha256`·`outputs_sha256`·`code_cells` 236/236 일치. `verify.py`의 읽기 전용 `verify_lesson()` 236/236 PASS | 0 (Traceback 0, `Error`로 시작하는 줄 2곳은 의도된 오류 장면) |
| 4. 그림 | Mermaid 924장(236절 모두 3~5장), 삽화 235장(235절 1장씩). 미전개 `{{mermaid:`·`{{img:` 0 | 2 — Ch 4 02절 삽화 대기(prompt 파일만) · Ch 1 05 HTML에 `[[미정: …]]` 주석 1곳 |
| 5. 학생 묶음 | Part 1~7 zip 속 노트북 257개 모두 디스크와 같음(다름 0·빠짐 0), 공개 목록 명시 항목 누락 0, 금지 파일(`__pycache__`·`.venv`·`.env`·`.pyc`) 10개 zip 모두 0 | 4 — `llm-practice.zip`(2026-09-14 판)·`ch01-practice.zip`·`ch02-practice.zip`(2026-09-11 판) 낡음 · Part 7 `bundle-execution.json`이 옛 판 |
| 6. 금지 표현 | 사용자가 금지한 표현(과정 규칙): 원고·빌드 HTML·노트북 마크다운·코드·출력 모두 0 | 0 (규격·검사 스크립트·작업 기록 77파일 84곳은 규칙과 검사 기록) |
| 7. 옛 생성기 | 대상 챕터에 `raise SystemExit`로 막히지 않은 옛 생성기 12개(`_gen_figures.py` 11 · Ch 3 실습 폴더 `_make_notebooks.py` 1). `.moai` 보조 스크립트 지정 5개는 막힘 | 12 (+ `.moai`에서 교재·실습 파일을 쓰는 막히지 않은 스크립트 11) |
| 8. 기기 상태 | 이 셸에서 보이는 파이썬·주피터·postgres·연습 서버 프로세스 0, `127.0.0.1` 대기 포트 0. 루트 여유 1.5G(86%), 세션 디스크 830M(92%), 연결 폴더 73G(85%). `/tmp` 2.09 GiB, `.cache/` 28.06 GiB | 참고 (프로세스는 격리 이름공간이라 셸 밖은 보이지 않음) |
| 9. 남은 일 | 강사 확인 항목 331개(챕터 요약 기준) + 과정 전체 결정 19건, 다음 세션 마감 일 11단계, 계정에 남은 Batch 파일 4건. 삭제 승인 대상 실측 합계 약 32.97 GiB(연결 폴더 30.81 GiB + 작업 기기 2.16 GiB) | — |

## 1. 챕터와 상태

- 교재 폴더 `textbook/part1`~`part7`의 챕터는 34개입니다(Part 1: 5 · Part 2: 3 · Part 3: 4 · Part 4: 4 · Part 5: 4 · Part 6: 9 · Part 7: 5). 대상 32챕터의 절은 236개(실습 절 포함), 제외된 Ch 32·33은 각 5절입니다.
- `qa/upgrade/chapter-summary.md`: 대상 32챕터 가운데 **31개**가 가지고 있습니다. **Ch 22(시범)에는 없습니다**(`qa/upgrade/`에 진단 8·설계표 9·`handoff.md`·`gates-after.json`만 있음).
- Ch 1 요약(67줄)은 §1~§5(가르친 것·예제·실습 절·인계·전제 금지)만 있고 「강사 확인 대상」·「남은 것」 절이 없습니다. Ch 1의 강사 확인 1건(A/B 배치 기준)은 `upgrade-final-checklist.md` §3에만 있습니다.
- 진행표(`textbook/qa/upgrade-progress.md` Ch 행 34줄) 상태 칸:
  - 「완료(강사 확인 대기)」 30개 — Ch 4는 「완료(강사 확인 대기, 삽화 1장 대기)」로 적혀 있습니다.
  - Ch 22 「완료(강사 확인)」(과제 지시의 「강사 확인 끝」과 같은 뜻으로 읽음).
  - Ch 32·33: 상태 「대기」, 실습 절 칸 「제외(사용자 결정)」, 메모 「Docker 실행 환경 없음」.
- 참고: 진행표 「절 수」 칸의 기준이 섞여 있습니다. Ch 9~22는 실습 절을 포함한 수, Ch 1~8·25·26·29·30·34는 제외한 수, Ch 23·24·27·28·31은 「N + 실습 1」로 적었습니다.

## 2. 게이트

`textbook/_notebook/checks/upgrade_gates.py`를 모듈로 불러 `check_section(chapter, lab, slug)`만 호출했습니다(`main()`을 부르지 않아 `gates-*.json`을 쓰지 않음). 절 목록은 `chapter.json`의 `sections`, `chapter.json`이 없는 Ch 8·9·10은 `_src/[0-9][0-9]-*.html`에서 얻었습니다.

| 챕터 | 절 | PASS | 코드 셀 | 검사 문장 | G1~G7 합 | 기록 대조 |
|---|---|---|---|---|---|---|
| Ch 01 | 6 | 6 | 84 | 1,707 | 0 | `gates-after.json`과 같음 |
| Ch 02 | 13 | 13 | 190 | 4,586 | 0 | 같음 |
| Ch 03 | 6 | 6 | 108 | 2,256 | 0 | `gates-after-2-7.json`과 같음(①) |
| Ch 04 | 6 | 6 | 96 | 2,197 | 0 | 같음 |
| Ch 05 | 9 | 9 | 119 | 3,419 | 0 | ① |
| Ch 06 | 7 | 7 | 130 | 2,767 | 0 | 같음 |
| Ch 07 | 9 | 9 | 179 | 3,770 | 0 | ① |
| Ch 08 | 7 | 7 | 161 | 3,090 | 0 | ① |
| Ch 09 | 7 | 7 | 145 | 3,327 | 0 | ① |
| Ch 10 | 9 | 9 | 185 | 3,749 | 0 | ① |
| Ch 11 | 7 | 7 | 167 | 2,934 | 0 | ① |
| Ch 12 | 13 | 13 | 330 | 4,430 | 0 | ① |
| Ch 13 | 8 | 8 | 195 | 2,559 | 0 | ① |
| Ch 14 | 10 | 10 | 236 | 3,524 | 0 | ① |
| Ch 15 | 9 | 9 | 233 | 3,383 | 0 | 같음 |
| Ch 16 | 7 | 7 | 184 | 2,632 | 0 | 같음 |
| Ch 17 | 6 | 6 | 147 | 2,297 | 0 | 같음 |
| Ch 18 | 7 | 7 | 192 | 2,931 | 0 | 같음 |
| Ch 19 | 7 | 7 | 171 | 2,581 | 0 | 같음 |
| Ch 20 | 5 | 5 | 135 | 1,979 | 0 | 같음 |
| Ch 21 | 7 | 7 | 180 | 2,633 | 0 | 06절 문장 411 → 412(②) |
| Ch 22 | 9 | 9 | 135 | 1,412 | 0 | 02절 문장 162 → 169(③) |
| Ch 23 | 7 | 7 | 178 | 2,493 | 0 | 같음 |
| Ch 24 | 4 | 4 | 112 | 1,593 | 0 | 같음 |
| Ch 25 | 4 | 4 | 97 | 1,414 | 0 | 같음 |
| Ch 26 | 5 | 5 | 135 | 2,044 | 0 | 같음 |
| Ch 27 | 9 | 9 | 253 | 3,726 | 0 | 같음 |
| Ch 28 | 6 | 6 | 152 | 2,428 | 0 | 같음 |
| Ch 29 | 5 | 5 | 127 | 2,003 | 0 | 같음 |
| Ch 30 | 10 | 10 | 229 | 3,926 | 0 | 같음 |
| Ch 31 | 6 | 6 | 150 | 2,560 | 0 | 같음 |
| Ch 34 | 6 | 6 | 147 | 2,431 | 0 | 같음 |
| **합** | **236** | **236** | **5,282** | **88,781** | **0** | |

- 0이 아닌 곳: 없음(G1~G7 모든 절 0건).
- 「같음」은 절마다 `counts`·`sentences`·`code_cells`가 `gates-after.json`과 모두 같다는 뜻입니다(20챕터).
- ① §2-7 리팩터(2026-09-21)로 코드 셀·문장 수가 바뀐 10챕터(Ch 3·5·7~14)는 `gates-after.json`과 다르고 `gates-after-2-7.json`과는 절마다 모두 같습니다.
- ② Ch 21 06절: 원고 `_src/06-같은-평가셋으로-RAG-비교.html` 수정 시각 2026-09-29 04:57Z(Ch 29 마감이 b10 문장을 고침, Ch 29 요약 172행). 이후 게이트 기록이 없어 `gates-after.json`·`gates-wip-06.json`의 411보다 1 많습니다. 게이트 합은 0 그대로입니다.
- ③ Ch 22 02절: Ch 16 마감(2026-09-23)이 설명 문장을 고친 뒤 기록 `gates-wip-02.json`(169)과 같고 `gates-after.json`(162)보다 7 많습니다.

## 3. 노트북 검증 흔적

- 대상 32챕터 실습 폴더 `notebooks/*.ipynb`는 236개이고 모두 절 노트북입니다(절 밖 노트북 0).
- `metadata.verification`: 236/236 있음. 모두 `status` `passed`, `fresh_kernel` true, `allow_errors` false. 실행 시각 범위 2026-09-15T10:31Z ~ 2026-09-30T02:36Z.
- `execute.py`의 `code_hash`·`output_hash`와 같은 식으로 다시 셈: `code_sha256` 236/236 · `outputs_sha256` 236/236 · `code_cells` 236/236 일치. **메타데이터와 다른 노트북 0.**
- `verify.py`의 `discover_lessons()`·`verify_lesson()`(파일을 쓰지 않는 함수)만 불러 236절을 확인: HTML ↔ 노트북 코드·출력·내려받기 사본 일치, 236/236 PASS(가장 긴 셀 21줄). `verify.py --chapter`(계약 JSON을 다시 씀)는 돌리지 않았습니다. Ch 14~34 챕터 요약 머리의 `verify.py --chapter` 코드 셀 수는 지금 값과 모두 같습니다.
- 저장 출력의 오류 흔적: `output_type` `error` 0, `Traceback` 0. `Error`로 시작하는 줄은 2개 노트북에 1곳씩이며 둘 다 코드가 받아서 출력한 의도된 오류 장면입니다.
  - Ch 6 `02-메시지와-제공자-전환.ipynb` 셀 29: `Error code: 404 - … gpt-5.4-mimi does not exist …`. 7절 제목 「없는 모델 이름으로 요청 보내기」, 셀 첫 줄 「없는 모델 이름으로 요청을 보내고, 모델을 찾지 못한 오류만 받습니다」, 결과 읽기가 `OpenAIModelNotFoundError`를 설명합니다.
  - Ch 20 `02-도구-오류와-ToolMessage.ipynb` 셀 53(After): `Error invoking tool 'lookup_policy' with kwargs {'주제': '대출'} …`. 셀 첫 줄 「이 셀만 올라온 오류를 받아 출력합니다」, 결과 읽기가 `ToolInvocationError`를 설명합니다.

## 4. 그림

- 절별 Mermaid(`_src`의 `{{mermaid:…}}`): 924장. 236절 모두 3~5장이고 SVG가 없는 이름 0.
- 삽화(`{{img:…}}`): 235장. 235절이 1장씩이고, PNG가 없는 이름 0.
- **Ch 4 02절 삽화 0장**: `figures/02-5-쪽지와-카드-상자.prompt.md`·`.caption.md`만 있고 `_src`에 `<!-- 삽화 대기 … -->` 주석 1곳. `qa/upgrade/illustration-pending.md`에 「재생성 한도 소진」으로 남아 있습니다(게이트 G7은 prompt 파일을 삽화로 세어 통과).
- 빌드한 HTML 276개(대상 챕터 절 236 + 챕터 목차 32 + Part 목차 7 + 전체 목차 1)에서 `{{`·`[[`를 찾았습니다.
  - 자리 표시가 남은 파일 **1개**: `textbook/part1/ch01-development-environment/05-Git과-Docker-준비.html`의 HTML 주석 `<!-- [[미정: Ch 1 A/B 트랙 공식 배치 기준]] 확정되면 이 문장을 바꿉니다 -->`(화면에는 보이지 않음, 강사 확인 대기 Ch 1 항목과 같은 건).
  - 미전개 `{{mermaid:`·`{{img:` 0.
  - 나머지 9개 파일의 `{{`·`[[`는 코드·출력 내용입니다(Ch 1 05 `docker version --format "{{.Server.Version}}"`, Ch 7 04 LangChain 오류 글의 `{{history}}`, Ch 5 03·Ch 7 06·Ch 12 12·13·Ch 17 05·Ch 18 05·Ch 20 04의 중첩 리스트).

## 5. 학생 묶음

`textbook/downloads/*.zip` 10개(만든 시각은 파일 수정 시각, UTC). 「노트북」 칸은 zip 속 노트북을 디스크의 같은 경로 파일과 바이트로 견준 수(같음/다름/빠짐 — 빠짐은 디스크에 있는데 zip에 없는 그 묶음 범위의 노트북)입니다.

| zip | sha256 | 크기(바이트) | 만든 시각 | 항목 | 노트북 같음/다름/빠짐 | 금지 파일 |
|---|---|---|---|---|---|---|
| `ch01-practice.zip` | `3763c9b7fbfe31f95d932121a4f20147673da8901e75a958165b790a9d63aea7` | 37,817 | 2026-09-11 06:37 | 11 | 0 / 5 / 1 | 0 |
| `ch02-practice.zip` | `23dd6e3f8ba213b57181a17b68800111df98729bc08ee1168d353334d47849a6` | 68,018 | 2026-09-11 06:37 | 17 | 0 / 12 / 1 | 0 |
| `llm-practice.zip` | `f2d2008a77fafdcc41bf46e4efddde9f65a48452f6173513661ef4a390430aad` | 11,102,660 | 2026-09-14 04:18 | 455 | 10 / 204 / 32 | 0 |
| `part1-practice.zip` | `b82d8fc12f7c7df198462e41e704c30888e20ebb27677be53d65251acaa4002d` | 3,880,804 | 2026-09-21 10:21 | 69 | 40 / 0 / 0 | 0 |
| `part2-practice.zip` | `7f894a76e30b4458857775b1c86a9b8eac001a759b35faf16078947ff250d76b` | 2,287,584 | 2026-09-21 05:22 | 40 | 23 / 0 / 0 | 0 |
| `part3-practice.zip` | `c6dea7c1722e7f7b7cffb4dd2799aa6e083dc93927de1858c27782d077aac5a5` | 11,936,062 | 2026-09-21 08:43 | 96 | 36 / 0 / 0 | 0 |
| `part4-practice.zip` | `29cc6d1fa9be0c6a141d5fb6d8d56fefa76021c93415ba321b49ec17bd9da8d9` | 11,311,384 | 2026-09-23 13:47 | 101 | 34 / 0 / 0 | 0 |
| `part5-practice.zip` | `faf00151f902de75a951dc603f1a8f8bff56c0cf97602b8bc9732fe50d75ce15` | 3,914,878 | 2026-09-24 09:37 | 68 | 31 / 0 / 0 | 0 |
| `part6-practice.zip` | `6d746be1ac649c102ee93475d897ae87e52b9876d2b131389a766a58afabb487` | 7,483,781 | 2026-09-29 05:01 | 113 | 61 / 0 / 0 | 0 |
| `part7-practice.zip` | `af44a3287324a728e21693760068ccb899b2cf4741ea56f00d9ccc673facbb1e` | 2,368,369 | 2026-09-30 03:57 | 117 | 32 / 0 / 0 | 0 |

- **Part 1~7 zip**: 노트북 257개 모두 디스크와 같고 빠진 노트북 0. 노트북 밖 파일도 디스크에 있는 것은 모두 같습니다(디스크에 없는 것은 묶음이 만드는 `시작하기.md`·`env.example`·`manifest.json`뿐). 선행 노트북 포함: Part 5 zip에 Ch 4 노트북 6, Part 6 zip에 Ch 18 1·Ch 19 4, Part 7 zip에 제외 챕터 Ch 32·33 노트북 10.
- 각 Part `public-files.json`의 명시 항목(2·2·17·59·10·94·113개)과 Part 6·7 `prerequisite-files.json`(13·1개)은 해당 zip에 모두 있습니다. 도구 파일 27개(`notebooks/*.py`)도 모두 해당 Part zip에 있습니다.
- **`llm-practice.zip`(2026-09-14 04:18)**: 품질 개선 시범(2026-09-15)보다 앞선 판입니다. 노트북 214개 가운데 204개가 지금과 다르고 같은 10개는 제외 챕터 Ch 32·33 노트북입니다. 대상 32챕터의 실습 절 노트북 32개가 없고, 도구 파일 27개도 하나도 없습니다. 전체 455항목 중 같음 187 · 다름 264 · 디스크에 없는 경로 4(그중 `labs/part4/ch16-guardrails/guardrails.py`는 Ch 16 01절이 옮긴 옛 자리).
- **`ch01-practice.zip`·`ch02-practice.zip`(2026-09-11 06:37)**: 노트북 5개·12개 모두 지금과 다르고, 실습 절 노트북(Ch 1 06·Ch 2 13)이 없습니다.
- 금지 파일(`__pycache__`·`.venv/`·`.env`·`.pyc`): 10개 zip 모두 0.
- **묶음 실행 기록**(어느 zip 기준인지):

| 기록 | 수정 시각 | 기준 zip | 지금 파일과 |
|---|---|---|---|
| `textbook/part4/qa/bundle-execution.json` | 2026-09-23 13:47 | `part4-practice.zip` `29cc6d1f…` | zip 해시·대상 노트북 2개 `code_sha256` 모두 같음 |
| `textbook/part5/qa/bundle-execution.json` | 2026-09-24 09:38 | `part5-practice.zip` `faf00151…` | zip·노트북 3개 모두 같음 |
| `textbook/part6/qa/bundle-execution.json` | 2026-09-29 05:02 | `part6-practice.zip` `6d746be1…` | zip·노트북 2개(Ch 24 01·Ch 28 01) 모두 같음 |
| `textbook/part7/qa/bundle-execution.json` | 2026-09-11 02:31 | zip 해시 칸 없음 | **Ch 30 01 `7bd57d1f…` → 지금 `861cacdb…`, Ch 31 03 `b0594f2d…` → 지금 `f97cba07…`로 다름**, Ch 33 02만 같음, Ch 32·34 실행 줄 없음 |
| `textbook/part3/qa/continuity-evidence/bundle-execution-results.json` | 2026-09-09 16:48 | `5b2a5947…` | 지금 `part3-practice.zip`과 다름 |
| `textbook/qa/continuity-evidence/bundle-execution-results.json` | 2026-09-09 17:52 | `a750de3e…` | 지금 zip 10개 어느 것과도 다름 |
| `textbook/part5/qa/bundle-execution-summary.json` | 2026-09-10 06:47 | `19acb30a…` | 옛 파일(Ch 20 요약: `check_bundle_execution.py`가 쓰지 않음) |

## 6. 금지 표현

사용자가 금지한 표현(과정 규칙)을 글자 그대로 찾았습니다. 범위는 `textbook/`·`labs/`의 텍스트 파일 13,393개(`.venv`·`node_modules`·`__pycache__` 제외, JSON은 `\u` 이스케이프 꼴도 셈)이고, 노트북은 셀 종류별로 나눠 셌습니다.

| 분류 | 파일 | 자리 |
|---|---|---|
| 원고(`_src`) | 0 | 0 |
| 빌드 HTML | 0 | 0 |
| 노트북 마크다운 | 0 | 0 |
| 노트북 코드 | 0 | 0 |
| **노트북 출력(따로 셈)** | 0 | 0 |
| 규격·절차서·과정 요약 | 3 | 3 |
| 챕터 작업 기록(`qa/upgrade/` 진단 42·handoff 14·검토 10·요약 7) | 73 | 80 |
| 검사 스크립트(`textbook/_notebook/checks/upgrade_gates.py`의 금지어 목록) | 1 | 1 |

- 규격·절차서·과정 요약 3개: `textbook/QUALITY-UPGRADE.md`, `textbook/_notebook/upgrade/PLAYBOOK.md`, `textbook/qa/upgrade-course-summary.md`.
- 챕터 작업 기록 73개(자리 수): Ch 12 3(3) · Ch 13 2(2) · Ch 14 7(12) · Ch 15 12(12) · Ch 16 3(4) · Ch 17 2(2) · Ch 18 5(5) · Ch 19 2(2) · Ch 20 7(8) · Ch 21 6(6) · Ch 23 1(1) · Ch 24 3(3) · Ch 25 5(5) · Ch 27 7(7) · Ch 28 5(5) · Ch 29 3(3). 파일 목록 전체는 점검 방법의 `/tmp/finalcheck/banned-result.json`에 있습니다.
- 학생이 읽는 자료(원고·HTML·노트북)에는 0입니다. 남은 84곳은 금지 규칙을 적은 문서, 「0건」을 확인한 작업 기록, 게이트의 금지어 목록입니다. 코드 문자열로 나눠 적은 자리는 글자 그대로 검색에 걸리지 않아 세지 않았습니다.

## 7. 옛 생성기

챕터·실습 폴더(`qa/upgrade/before/` 제외)에서 옛 생성기 이름(`_gen_figures.py`·`author_ch*.py`·`_generate*.py`·`_make_notebooks.py`·`_make_*.py`·`_author*.py` 등)과, `.ipynb`·`_src`를 쓰는 파이썬 파일을 찾아 맨 위 60줄 안의 최상위 `raise SystemExit`를 확인했습니다.

**막히지 않은 옛 생성기 — 대상 챕터 12개**

| 파일 | 쓰는 것 |
|---|---|
| `labs/part1/ch03-git-github/_make_notebooks.py`(491줄) | **`notebooks/{slug}.ipynb` 다섯을 출력 없는 옛 판으로 덮어씀**(489~490행) |
| `textbook/part1/ch01-development-environment/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part1/ch02-python/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part1/ch03-git-github/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part1/ch04-data-tools/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part1/ch05-llm-principles/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part2/ch06-langchain-start/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part2/ch07-prompt-engineering/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part2/ch08-context-engineering/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part3/ch09-rag-first-run/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part3/ch11-evaluation/figures/_gen_figures.py` | 옛 SVG·excalidraw |
| `textbook/part6/ch22-middleware/figures/_gen_figures.py` | 옛 흐름 SVG(`textbook/part5/_figure.py`의 `render`) |

- `_gen_figures.py` 11개가 쓰는 파일 이름(예: `01-learning-cycle.svg`, `01-미들웨어와-6개-훅-흐름.svg`)은 지금 원고가 부르지 않는 옛 그림이라, 실행해도 현재 Mermaid·삽화 파일과 이름이 겹치지 않습니다. 규격 §8 1번(막음 줄 + `before/generators/`로 옮김)은 지켜지지 않은 상태입니다.
- 제외 챕터: Ch 32·33 `figures/_gen_figures.py` 둘도 막힘 줄이 없습니다. Ch 33 `labs/part7/ch33-cicd/_make_chapter.py`는 `main()` 안에서 `raise SystemExit`로 멈춥니다.
- 막혔지만 제자리에 있는 것(체크리스트 §1-7·§2-2 4번의 「옮김」 대기): Ch 10 `figures/_gen_figures.py`(14행) · Ch 11 `labs/…/_make_notebooks.py`(8행) · Ch 12 `figures/_gen_figures.py`(8행)·`qa/advanced_author.py`(11행) · Ch 13 `figures/_gen_figures.py`(10행)·`qa/author_ch13.py`(11행).
- 옛 생성기가 아닌 것으로 분류(막힘 대상 아님): Ch 22 `qa/upgrade/author_upgrade.py`(시범 개선 생성기 — 다른 챕터의 `qa/upgrade/author_NN.py`와 같은 역할), Ch 34 `qa/upgrade/probe/make_data02.py`(자료 파일을 없을 때만 쓰는 확인 스크립트), Ch 9 `labs/…/examples/ex04_generate.py`(학생 예제), `textbook/part5/qa/language/ch17-original/…/_gen_figures.py`(옛 감사 기록 속 사본).
- **`.moai` 보조 스크립트**: 체크리스트가 적은 5개(`.moai/evolution/remaining-parts-learning-sequence-2026-09-14/part6b_enrich.py`·`part6b_review_fixes.py`·`part7_apply_depth.py`·`part7_review_fixes.py`·`part7_final_repairs.py`)는 4~5행 최상위 `raise SystemExit`로 막혀 있습니다.
- `.moai`의 파이썬 109개 중 교재·실습 경로를 적고 파일을 쓰는 것은 46개, 그중 막힌 것은 위 5개뿐입니다. 사본 폴더(`before`·`*-before`) 밖의 막히지 않은 11개:
  - `_src`·노트북을 직접 고쳐 쓰는 9개(같은 폴더 `remaining-parts-learning-sequence-2026-09-14/`): `enrich_part4.py`(Ch 13~16) · `part2_review_repairs.py` · `part4_final_repairs.py`(Ch 15·16) · `part5_enrich.py` · `part5_review_repairs.py`(Ch 18·20) · `part6a_enrich.py`(Ch 21) · `refine_part2.py`(Ch 6·7) · `revise_part2.py` · `revise_part2_ch07.py`.
  - 교재를 읽고 기록만 쓰는 2개: `part1-learning-sequence-2026-09-11/language_corpus.py`(루트 `_workspace/2026-09-11-NNN/`에 씀)·`verify_revision.py`(자기 폴더 `revision-results.json`에 씀).

## 8. 기기 상태

- **프로세스**: 이 셸은 격리된 PID 이름공간(`bwrap`)에서 돌아 `ps`에 보이는 것은 셸 자신뿐입니다. 보이는 범위에서 파이썬·주피터·postgres·연습 서버 프로세스는 0입니다. 셸 밖(다른 세션) 프로세스는 확인하지 못했습니다.
- **대기 포트**(`ss -ltnp`): `0.0.0.0:22`·`[::]:22`(sshd)뿐이고 `127.0.0.1` 대기 포트는 0입니다(Ch 23 55432·Ch 28 58028·Ch 34 58034 없음).
- **디스크 여유**: 루트 `/`(=`/tmp`) 9.6G 중 여유 1.5G(사용 86%) · 세션 디스크 `/sessions`(세션 홈·`$TMPDIR`) 9.8G 중 여유 830M(92%) · 연결 폴더 461G 중 여유 73G(85%).
- **`/tmp` 전체 2,189,012 KiB(2.09 GiB)**:
  - 작업 폴더 21개 203,980 KiB — `ch31-02`~`06`·`ch31-close`·`ch31-pg`(DB 데이터 65,856 포함) 131,028 · `ch34-01`~`06`·`ch34-close`·`ch34-prep` 70,636 · `reviewA31`·`reviewB31`·`reviewA34`·`reviewB34` 1,912 · `cumdocs31`·`cumdocs34` 404.
  - 공용 도구 1,984,744 KiB — `pptr-cache` 677,388 · `mmd` 481,280 · `pw-browsers` 275,260 · `uv-cache` 246,976 · `npm-cache` 246,540 · `npm-cache-ch31close` 38,520 · `pw` 18,720 · `libs` 60.
  - 이 점검이 만든 `finalcheck` 256 KiB.
  - 작업 기기는 04:34Z 기준 가동 12시간 27분(`/proc/uptime`)으로, 2026-09-29 16:07Z 무렵 다시 시작되었습니다. 체크리스트 §2-x가 적은 `/tmp/ch13-*`~`/tmp/ch30-*`·`/tmp/reviewA15`~`reviewB30` 등은 지금 없습니다.
- **세션 홈**: `~/ch16work` 70,208 KiB, `$TMPDIR` 72항목 7,740 KiB(`ch03-05-*`·`ch23-04-*`·`ch24-01-*`·`ch27-04-*`·`ch31-03-*`·`ch31-05-*` 등).
- **`.cache/` 29,424,720 KiB(28.06 GiB)**: `vm/venv-ch*` 27개 13,536,808 · `vm/bundle-check` 8,093,088 · `vm/hf` 6,182,812 · `vm/mamba` 812,440 · `vm/pgembed-try` 207,936 · `vm/pgdata` 64,708 · `vm/pg` 58,804 · `vm/pgenv` 45,924 · `vm/shot` 15,452 · `vm/pgtool` 80 · 챕터 작업 폴더 145개(`ch*-view`·`ch*-close` 등) 406,668. 항목을 나눠 잰 합이라 서로 하드링크를 공유하면 실제 점유보다 클 수 있습니다. `vm/venv-ch13-firstattempt-unused`(체크리스트 §2-2 3번)는 없습니다.

## 9. 남은 일

### (가) 사람이 정해야 할 것

**챕터별 건수**. 「강사 확인」은 각 챕터 요약 「강사 확인 대상」 절의 최상위 항목 수입니다(한 항목에 결정이 여럿 묶인 경우가 있어 결정 수의 하한입니다). Ch 1은 요약에 절이 없어 체크리스트 §3의 1건, Ch 22는 강사 확인이 끝났습니다. 설계 승인(예외 문법·실험 설계)은 각 요약에서 이 항목 안에 들어 있습니다. 나머지 칸은 삭제 승인 대상의 실측입니다.

| 챕터 | 강사 확인 | 옛 그림 파일(바이트) | gates-wip 등 | 캐시 폴더 | 실습 `.venv` KiB | `.cache` 챕터 몫 KiB |
|---|---|---|---|---|---|---|
| Ch 01 | 1 | 10 (97,630) | 7 | 0 | 77,276 | 0 |
| Ch 02 | 5 | 24 (236,645) | 14 | 2 | 140,392 | 0 |
| Ch 03 | 6 | 10 (79,674) | 7 | 6 | 78,488 | 0 |
| Ch 04 | 5 | 10 (55,749) | 7 | 5 | 180,508 | 0 |
| Ch 05 | 8 | 16 (41,850) | 9 | 1 | 762,680 | 947,640 |
| Ch 06 | 6 | 12 (88,007) | 7 | 3 | 210,684 | 239,956 |
| Ch 07 | 6 | 16 (135,778) | 10 | 3 | 168,568 | 195,512 |
| Ch 08 | 6 | 14 (922,424) | 7 | 8 | 181,484 | 201,148 |
| Ch 09 | 8 | 17 (2,312,870) | 7 | 9 | 291,208 | 312,180 |
| Ch 10 | 8 | 25 (166,813) | 10 | 7 | 350,012 | 379,472 |
| Ch 11 | 8 | 12 (13,395) | 8 | 5 | 235,584 | 235,824 |
| Ch 12 | 9 | 39 (169,580) | 22 | 5 | 72 ※ | 5,951,152 |
| Ch 13 | 8 | 21 (138,968) | 8 | 4 | 72 ※ | 411,096 |
| Ch 14 | 8 | 27 (168,628) | 12 | 5 | 160,192 | 227,980 |
| Ch 15 | 10 | 24 (123,252) | 9 | 5 | 153,824 | 199,480 |
| Ch 16 | 13 | 18 (110,796) | 14 | 6 | 176,320 ※ | 242,824 |
| Ch 17 | 19 | 15 (53,960) | 12 | 4 | 106,848 ※ | 258,160 |
| Ch 18 | 13 | 18 (125,813) | 15 | 5 | 137,360 ※ | 199,748 |
| Ch 19 | 14 | 18 (89,461) | 14 | 4 | 248,300 ※ | 417,872 |
| Ch 20 | 13 | 12 (69,308) | 10 | 3 | 179,192 ※ | 267,296 |
| Ch 21 | 14 | 18 (72,942) | 17 | 2 | 215,588 ※ | 371,368 |
| Ch 22 | 0 | 24 (102,914) | 1 | 0 | 66,468 | 0 |
| Ch 23 | 14 | 18 (64,932) | 16 | 1 | 145,344 ※ | 271,628 |
| Ch 24 | 14 | 9 (32,433) | 9 | 0 | 127,232 ※ | 230,452 |
| Ch 25 | 12 | 9 (24,288) | 9 | 0 | 176,360 ※ | 262,264 |
| Ch 26 | 14 | 12 (42,927) | 11 | 1 | 177,536 ※ | 266,772 |
| Ch 27 | 16 | 24 (86,496) | 19 | 3 | 220,144 ※ | 316,700 |
| Ch 28 | 14 | 15 (89,014) | 13 | 2 | 226,760 ※ | 319,564 |
| Ch 29 | 14 | 12 (45,867) | 11 | 0 | 190,508 ※ | 292,740 |
| Ch 30 | 14 | 27 (97,188) | 21 | 4 | 175,068 ※ | 298,584 |
| Ch 31 | 15 | 15 (25,891) | 13 | 3 | 221,404 ※ | 382,800 |
| Ch 34 | 16 | 10 (44,723) | 13 | 1 | 142,304 ※ | 243,264 |
| **합** | **331** | **551 (5,930,216)** | **362** | **107** | | |

- 옛 그림: 그림 폴더에서 지금 `_src`가 `{{mermaid:}}`·`{{img:}}`로 부르지 않는 파일(대기 삽화 prompt·caption과 `_gen_figures.py`는 제외). Ch 13~31·34 수는 체크리스트 §2-x와 모두 같습니다. **Ch 22 24개는 체크리스트에 없습니다.** Ch 8·9에는 개선 전 삽화 PNG(예: `01-오픈북-비유.png`)가, Ch 9에는 `figures/verification.md` 1개가 들어 있습니다.
- gates-wip 등: `qa/upgrade/gates-wip*`·`gates-closecheck`·`gates-pre*` JSON. Ch 15~34 수는 체크리스트와 같습니다(Ch 22 1개는 Ch 16 마감이 만든 `gates-wip-02.json`).
- 캐시 폴더: 챕터에 속한 `__pycache__`·`.pytest_cache`·`.ruff_cache`(`.venv` 밖). 전체는 128개 8,821,813바이트이며, 표의 107개 밖에 Part·공용 폴더 16개(`textbook/_notebook/__pycache__` 등)와 제외 챕터 Ch 32·33의 5개가 있습니다.
- ※ 체크리스트가 삭제 승인 대상으로 적은 실습 폴더 `.venv` 18개. 합 2,866,412 KiB(2.73 GiB), 34개 전체는 6,150,696 KiB(5.87 GiB). Ch 31 `.venv`는 Part 7 `check_bundle_execution.py`의 노트북 실행기(32행)라 러너를 고치기 전에는 지우면 안 됩니다.

**과정 전체에 걸친 결정 19건**

1. 제목·슬러그의 금지어·영문 말을 한 번에 바꿀지(Ch 15 03 「프롬프트」, Ch 16 05·06, Ch 17 05·06, Ch 18~34 요약마다 강사 확인 1번 「제목 말」). 바꾸면 파일 이름·`chapter.json`·공개 목록 두 곳·Part 목차·검사 허용 목록·zip을 함께 다시 만듭니다.
2. 코드 양 증가를 받아들일지(규격 §2-7 「코드를 늘려 가면서 개선할 필요는 없다」 ↔ Ch 17~34 요약의 코드 줄 증가, 예: Ch 27 252 → 1,461줄, Ch 34 192 → 841줄).
3. Part 5·6 옛 검사 스크립트(`check_scope.py`·`check_figures.py`·`check_notebook_readiness.py`·`finalize_evidence.py`·`check_visual_reports.py`)와 Part 7 `check_figures.py` 20행을 고칠지 둘지.
4. Part 7 `check_delivery.py`가 읽는 `existing-artifacts-before.json`을 다시 만들지(체크리스트 §2-4 9번).
5. `textbook/_notebook/build_index.py` 절 수에 실습 절을 넣을지(§2-13 10번).
6. 묶음 실행 검사에 넣을 후보(Ch 25 01, Ch 26 02·03 앞 절반, Ch 27 01, Ch 29 01·02·04, Ch 30 10, Ch 31 06, Ch 34 02·04·05). 넣으면 그 노트북에 계약이 생깁니다.
7. Part 7 `check_bundle_execution.py` 러너(Ch 31 macOS `.venv`)를 어떻게 고칠지.
8. 실습 폴더 잠금 정리(Ch 12 `pgvector`·`pypdf`, Ch 13 쓰지 않는 패키지 넷, Ch 15 `langsmith`, Ch 21·29 `pillow`, Ch 28 `httpx`·`psutil` 직접 의존, Ch 31 dev `pip==25.2`). 바꾸면 `uv lock`과 묶음 재생성이 따릅니다.
9. `openai` 판 차이(Ch 18 잠금 2.29.0 ↔ Part 5 다른 챕터 3.11.0, 교재 출력 환경 ↔ 학생 잠금).
10. Part 6 묶음에 Ch 19 잠금을 넣을지(§2-8 7번).
11. 도구 파일 가져오기와 작업 폴더 안내 문장(과정 공통, §2-4 7번·§2-8 4번).
12. 「예상 비용」의 과정 뜻(과정 요약 152행 ↔ Ch 16 요약 §4, §2-6 7번).
13. 규격에 넣을지: 앱 파일 문법 예외(§2-18 8번), 입력 토큰 결론 선례(§2-16 7번), 모델 요청 0인 실습 절(Ch 23·24·30·31 — 규격 §7-2 「3~5번」과 다름).
14. 기록 파일의 옛 해시를 다시 모을지(`textbook/part6/qa/final-artifact-hashes.json` 등, §2-10 7번).
15. `.moai` 스크립트 처리(막힌 5개를 옮길지·지울지, 막히지 않은 11개를 막을지 — 7절).
16. 삽화: Ch 4 02-5를 새로 생성할지(재생성 한도 소진), 각 요약이 적은 재생성 후보.
17. 2차 검토(한국어 감사 3단·삽화 판독·Windows·macOS 실제 실행) 진행 방식과 시기.
18. 제외 챕터로 넘긴 문장(Ch 31 §2-19 11번의 Ch 32 04 b7, Ch 34 §2-20 12번의 Ch 33 04)을 언제 고칠지.
19. 삭제 승인(아래 표)과 계정에 남은 Batch 파일((다)).

**삭제 승인 대상 — 실측 합계**

| 대상 | 개수 | 실측 크기 | 비고 |
|---|---|---|---|
| 옛 그림 | 551파일 | 5,930,216 B | 위 표 |
| gates-wip 등 | 362파일 | 408,527 B | 위 표 |
| `__pycache__`·`.pytest_cache`·`.ruff_cache` | 105·9·14폴더 | 8,821,813 B | `textbook`·`labs`, `.venv` 밖 |
| 개별 파일·폴더 | 16항목 | 1,689,676 B | Ch 13 `runs/graph-integrated-result.json` 1,078 · Ch 34 옛 `runs/` 셋 4,057 · 루트 `batch-input.jsonl` 483 · Ch 27 `workspace`·`workspace-05`·`workspace-08` 432,929 · `textbook/qa/_to_delete/_trim_tmp.py` 10,788 · Ch 16 `depth-notes.json` 6,341 · Ch 34 `probe/02-batch.md.tmp` 9,121 · Ch 12 `runs/continuity/` 사본 셋(`20260918T231546`·`231622`·`231828`) 1,224,879 · 빈 폴더 `textbook/_notebook/checks/--chapter`·`checks/ch34-cost-optimization` 0 |
| 실습 폴더 `.venv`(체크리스트 18개) | 18 | 2,866,412 KiB | 34개 전체 6,150,696 KiB |
| `.cache/` 전체 | — | 29,424,720 KiB | 8절 내역. 다음 세션이 쓰는 것: `vm/pgenv`(Ch 23·31 `pre_exec.sh`), `vm/bundle-check`(묶음 실행 검사), `vm/venv-ch*`·`vm/hf`(재실행 때) |
| 작업 기기 `/tmp` 작업 폴더 | 21 | 203,980 KiB | `/tmp/ch31-pg`는 Ch 31 훅의 DB 데이터(지우면 다음 훅이 `initdb`부터) |
| 작업 기기 `/tmp` 공용 도구 | 8 | 1,984,744 KiB | Mermaid·Playwright·npm·uv 캐시 |
| 세션 홈 `~/ch16work`·`$TMPDIR` | — | 77,948 KiB | |
| **합계** | | **약 32.97 GiB** | 연결 폴더 30.81 GiB(파일 합 16.07 MiB + `.venv` 2.73 GiB + `.cache` 28.06 GiB) · 작업 기기 2.16 GiB |

보존 대상(체크리스트 §4)은 합계에 넣지 않았습니다: `qa/upgrade/before/`(옮긴 생성기 포함)·`probe/`·`review-pack/`, Ch 12 `runs/continuity/20260918T232052`·`20260921T082024`, Ch 9·10 옛 사본, `*.render.json`, 계약 노트북·자료 파일, Ch 23·31 `pre_exec.sh`.

### (나) 사람 결정 없이 다음 세션이 할 수 있는 전체 마감 일(순서대로)

(가) 1번(제목·슬러그)을 바꾸기로 하면 그 작업을 먼저 해야 묶음·목차를 두 번 만들지 않습니다.

1. **옛 생성기 정리**(규격 §8 1번, 삭제 아님): 7절의 막히지 않은 12개에 막음 줄을 넣고 `qa/upgrade/before/generators/`로 `mv -n`. 특히 Ch 3 `labs/part1/ch03-git-github/_make_notebooks.py`. 막혔지만 제자리인 6개(Ch 10·11·12·13)도 옮김.
2. **도구 파일 머리 줄**(체크리스트 §2-13 6번): Ch 24 `approval_tools.py`·Ch 25 `stream_tools.py`·Ch 26 `delegation_tools.py`·Ch 27 `harness_tools.py`·Ch 29 `eval_tools.py`·Ch 30 `serve_tools.py`(Ch 28은 해당 없음). 각 생성기 대조 사슬과 챕터 공개 목록 해시를 함께 맞춤(노트북 재실행 불필요).
3. **「청크」 표기**: Ch 6 04 본문 「청크」 → 「스트림 청크」(미결 Part 2 1번 결정). 같은 작업에서 Ch 25 02 b3·b4와 「사용량 청크」 다섯 곳(§2-13 12번, 마크다운만).
4. **누적 문서**: 과정 요약(Ch 16~34 용어·선례, 「예상 비용」 줄은 결정 뒤), `upgrade-contracts.md`(Ch 21 06 → Ch 29 04 출력 계약 줄, §5 새 zip 해시·`bundle-execution.json` 값), 진행표의 §2-7 뒤 코드 셀 수, 필요하면 Ch 22 `chapter-summary.md`.
5. **묶음 재생성**: `ch01-practice.zip`·`ch02-practice.zip`·`llm-practice.zip`, 그리고 1~3단계로 안의 파일이 바뀐 Part zip(Part 2·6·7 등). 뒤이어 Part별 `check_delivery.py`(Part 7은 (가) 4번 결정 뒤).
6. **묶음 실행 검사**: Part 3 `run_continuity_bundle.py`(`--reuse-upstream` 없이 — Ch 9 06·Ch 10 08·Ch 11 06), Part 4·5·6 `check_bundle_execution.py`(`UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache UV_LINK_MODE=symlink`). Part 7은 (가) 7번 결정 뒤. 끝나면 각 `bundle-execution.json`이 새 zip 기준이 됩니다.
7. **화면 재촬영**(`visual.cjs`): Ch 9 HTML 8쪽(14 → 16행, 공용·챕터 두 파일), Part 6 `visual-results.json`의 Ch 22 18줄·목차 두 쪽 4줄(지금 HTML 해시와 다름 — 다른 110줄은 같음), Ch 21, 2~3단계로 바뀐 쪽.
8. **`textbook/part3/qa/finalize_continuity_evidence.py`**: 25행 `assert len(visual) == 94`를 96으로 올린 뒤 실행(체크리스트 §1 4단계는 「15행」이라 적었으나 15·19·20행은 설명 주석).
9. **연속성 검사 끝까지**: Part 2 `check_continuity.py`, `textbook/qa/check_course_continuity.py`(시스템 파이썬 3.10에는 `tomllib`이 없어 3.12 가상환경으로).
10. **목차 재생성**: Part 1 `_build_index.py`(Ch 3~5 절 수), Part 2·3 목차, `textbook/_notebook/build_index.py`의 Ch 17~34 설명(절 수는 (가) 5번 결정 뒤), 전체 `textbook/index.html`.
11. **검토 묶음 다시 만들기**: 각 챕터 `qa/upgrade/review-pack/`를 `textbook/_notebook/upgrade/pack.py`로 새로 만들어 2차 검토를 준비.

### (다) 서비스 계정에 남은 것

- **OpenAI 계정 — Ch 34 02 Batch**(노트북 밖 한 번, 제출 2026-09-29 23:08Z): 입력 파일 1(1,780바이트, `purpose` batch) · 결과 파일 1 · 오류 파일 1 · 작업 기록 1 = **4건**. 기록(`textbook/part7/ch34-cost-rate-limits/qa/upgrade/probe/02-batch.md` 67행, 체크리스트 §2-20 6번): 서비스 파일 지우기 API는 부르지 않았고, 결과 파일은 작업 뒤 30일에 자동 삭제되며 올린 파일은 기본 30일 뒤 만료된다는 공식 안내를 인용합니다. 지울지는 사람이 정합니다.
- 다른 챕터의 작업 기록(`qa/upgrade/*.md`)과 노트북에는 계정에 파일을 남겼다는 기록이나 `files.create`·`batches.create` 호출이 없습니다.

### 체크리스트와 지금 상태가 다른 곳

- §1 4단계 `finalize_continuity_evidence.py` 「15행」 → 실제 값은 25행.
- §2-x의 기기 `/tmp` 작업 폴더(Ch 13~30)·`/tmp/pw`(Ch 16 판) 등 → 작업 기기 재시작으로 없음. 지금 있는 것은 8절 목록.
- §2-2 3번 `.cache/vm/venv-ch13-firstattempt-unused` → 없음.
- 「§2-7 리팩터가 남긴 것」 1번(Part 6 묶음이 품질 개선 전) → 해소됨(Part 6 zip 노트북 61개 = 디스크, Ch 22 09 포함).
- Part 6 `visual-results.json`은 `all_current_and_passed` true로 적혀 있으나 Ch 22 18줄과 목차 두 쪽 4줄의 `html_sha256`이 지금 HTML과 다릅니다.
- Ch 22 옛 그림 24개는 삭제 승인 목록에 없습니다.

## 점검 방법

모든 셈은 기기 셸(`mcp__remote-devices__device_bash`, 파이썬 3.10.12, `PYTHONDONTWRITEBYTECODE=1`)에서 했고, 교재·실습 파일은 읽기만 했습니다. 노트북 실행·모델 요청·삽화 생성·`.env` 읽기는 0입니다.

1. **챕터와 상태**: `textbook/part*/ch*` 폴더와 `_src/[0-9][0-9]-*.html`을 세고, `qa/upgrade/chapter-summary.md` 유무, 진행표 `grep -n '^| Ch '` 줄의 상태 칸을 읽었습니다.
2. **게이트**(`gates.py`): `upgrade_gates.py`를 `importlib`으로 불러 `check_section()`만 236절에 호출. 결과를 절마다 `gates-after.json`과, 차이가 난 챕터는 `gates-after-2-7.json`·`gates-wip-NN.json`과 견줌(`gates_cmp27.py`).
3. **노트북**(`nbverify.py`·`verifyro.py`): `execute.py`와 같은 식으로 `code_sha256`·`outputs_sha256`을 다시 셈하고 `metadata.verification`과 견줌. 출력의 `error` 항목·`Traceback`·`Error`로 시작하는 줄을 찾아 앞뒤 설명 셀과 셀 첫 줄로 의도 여부를 판단. `verify.py`의 `discover_lessons()`·`verify_lesson()`(쓰기 없음)만 호출.
4. **그림**(`figs.py`): `_src`의 `{{mermaid:}}`·`{{img:}}` 수, SVG·PNG 유무, `<!-- 삽화 대기` 주석, prompt만 있는 이름. 빌드 HTML 276개의 `{{`·`[[` 앞뒤 글을 보고 자리 표시와 코드·출력을 구분.
5. **묶음**(`zips.py`): zip 파일 sha256·크기·수정 시각, 항목을 디스크 같은 경로 파일과 sha256으로 비교, 금지 파일 이름 검사, 공개 목록·선행 목록·도구 파일 포함 여부, 묶음 실행 기록 JSON의 해시를 지금 zip·노트북 `code_sha256`과 대조.
6. **금지 표현**(`banned.py`): 금지 표현을 유니코드 이스케이프로 만든 문자열을 `textbook`·`labs` 텍스트 파일에서 글자 그대로 셈(노트북은 셀 종류별, 출력은 따로).
7. **옛 생성기**: `find`로 이름 패턴, `grep`으로 `.ipynb`·`_src`를 쓰는 파이썬 파일을 찾고, 맨 위 60줄의 최상위 `raise SystemExit`를 확인. `.moai`의 파이썬 109개도 같은 기준.
8. **기기 상태**: `ps`·`ss -ltnp`·`df -h`·`du -sk`(`/tmp`, 세션 홈, `.cache` 항목별, 실습 폴더 `.venv` 34개 — 모두 `timeout`으로 나눠 실행), `/proc/uptime`.
9. **삭제 대상 크기**(`delsize.py`): 그림 폴더에서 `_src`가 부르지 않는 파일, `gates-wip*` 등, 캐시 폴더, 개별 파일은 바이트 합. 큰 폴더는 `du -sk`(KiB). 1 GiB = 1,048,576 KiB로 환산.

**만든 임시 파일**(기기 `/tmp/finalcheck/`, 지우지 않음): `gates.py`·`gates-result.json`·`gates_cmp27.py` · `nbverify.py`·`nbverify-result.json` · `verifyro.py`·`verifyro-result.json` · `figs.py`·`figs-result.json` · `zips.py`·`zips-result.json` · `banned.py`·`banned-result.json` · `delsize.py`·`delsize-a.json`·`perch-del.json` · `du-cache-top.txt`·`du-cache-vm.txt`·`du-cache-hf.txt`·`du-cache-bc.txt`·`du-venv-a.txt`·`du-venv-b.txt` · 보고서 조각 `report-part1.md`·`report-part2.md`·`report-part3.md`와 합친 사본 `report-full.md`.
