# 09-LLM-동작-원리-실습 — 챕터 끝 실습 절 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md` §7-2, `textbook/_notebook/upgrade/PLAYBOOK.md` §3, `.claude/agents/easy-upgrade-editor.md` 6.8. 기준 사례: Ch 22 `09-Middleware-실습`(LLM 챕터 실습), Ch 4 `06-데이터-도구-실습`(`author_06.py`, 검토 반영본).
새 절이라 수정 전 원본은 없습니다. 08절에서 고친 두 문장의 수정 전 파일은 `qa/upgrade/before/08-to-09/`(`_src`, 노트북, 생성기 사본)에 두었습니다.
생성기: `qa/upgrade/author_09.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 09`(환경 변수 없이). 설명만 고칠 때는 `mdpatch.py` → `--no-exec`.
먼저 읽은 것: Ch 1~4 `qa/upgrade/chapter-summary.md`, 이 챕터 `qa/upgrade/handoff.md` 전체(특히 `## §08 → 실습`), `_src/01`~`08` 「정리와 다음 절」, `_src/08` 전체, `author_02·03·07·08.py`, 04-5·08-5 삽화 프롬프트, Ch 4 `_src/06`·`author_06.py`·`06-figures.md`·06 그림, Ch 22 `_src/09`, Ch 9 01 본문(검색 단계 문장 확인).

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 새 절 | 0 |
| G2 | 새 절 | 0 |
| G3 | 새 절 | 0 |
| G4 | 새 절 | 0 |
| G5 | 새 절 | 0 |
| G6 | 새 절 | 0 (첫 검사 11건: 70자 초과 10 → 문장 나눔, 6문장 단락 1 → 단락 나눔. `<|im_end|>`를 태그로 지워 「다.」 뒤가 빈칸이 되어 한 문장이 둘로 세어진 곳) |
| G7 | 새 절 | 0 |
| 코드 셀 | 새 절 | 15 (준비 1 + 본 경로 14, 함수 정의 셀 8개, 심화 셀 없음) |
| 검사한 문장 | 새 절 | 364 (`gates-wip-09.json`) |
| 모델 실행 | 새 절 | 내 컴퓨터에서 Qwen2.5-0.5B-Instruct `generate()` 4번(질문 2 × 실행 2, `do_sample=False`, 출력 몫 64), MiniLM `encode()` 5번(문서 목록 1 + 질문 4). API 호출 0, 비용 0 |

- 새 커널 실행 PASS 두 번(`PASS 09-LLM-동작-원리-실습.ipynb: 15 cells`). 두 번 모두 `outputs_sha256` `981329b466b45dc7990d3e2d2ef13e80b087a92f73ac5f6437430f93cd143c72`로 같음(첫 실행 21:18, `run_section.sh` 전체 실행 21:27 UTC). 기기 셸 프로토타입(`/tmp/ch05-09/proto3.py`, 노트북과 같은 코드)의 출력도 글자까지 같음.
- 실행 환경: 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(Python 3.12.13, torch 2.8.0+cpu, transformers 4.56.2, sentence-transformers 5.1.1)와 모델 캐시 `$ROOT/.cache/vm/hf`(Qwen `7ae5576…`, MiniLM `e8f8c21…`, 새로 받은 모델 없음). `run_section.sh` 전체 약 16초. 같은 계산 스크립트의 `ru_maxrss` 3176MB(약 3.2GB, Qwen 먼저 적재 뒤 MiniLM). 기기 루트 여유 558MB(변화 없음).
- `verify.py --chapter` `PASS 9 sections / 130 code cells (max 17 lines)`. `visual.cjs` 08·09·index HTML × 1280·390px 6건 PASS(`/tmp/ch05-09/vis/vis.cjs`, 08절 작업자 사본 복사, 공용 도구는 고치지 않음). 빌드 HTML: SVG 3·삽화 1, 남은 `{{` 0, 챕터 `index.html` 「절 9개」와 09 링크, 08 HTML에 09 링크.

## 주제와 구성

- 주제: 「문서를 골라 넣고 답 점검하기」. 작은 상담 창구의 문서 세 개(04절 환불 문장, 07절 노을 워커 3 배터리·해바라기 연구소 초록 패스)에서 질문과 가까운 문서를 골라 넣고, 답을 코드로 점검해 기록장에 적음
- 조립한 핵심 네 개: 02절 유사도로 문서 고르기(`pick_document()`), 04절 채팅 템플릿·조각 수·입력 한도(`make_input()`·`encode()`·남는 칸), 05·06절 뽑기를 끈 답(`ask_model()`), 07절 판정 규칙(`find_new_numbers()`·보류 문장). 01절 조각 세기와 03절 `for`+`if` 최댓값 찾기, 08절 모델 선택·두 모델 한 커널·튜플 반환은 보조로 씀. 03절 어텐션 비중과 06절 뽑기를 켠 생성은 쓰지 않는다고 본문 b3·노트북 2번에 적음
- 바꾸는 값: `system_text` 하나(실행 1 04절 「주어진 문서 범위에서만 답하세요.」 → 실행 2 07절 9절 보류 지시). 질문·문서·출력 몫·판정 규칙은 같음
- 질문: 「환불은 며칠 이내에 신청하나요?」(04·08절, 문서에 답 있음), 「노을 워커 3의 무게는 몇 g인가요?」(이 실습에서 새로 만듦, 세 문서에 답 없음)
- 노트북 순서(PLAYBOOK §3): 준비(버전) → 주제 → 재료(두 모델, 문서 세 개·조각 수·벡터, 질문과 정해 둘 값) → 부품 6개(`dot_product`·`pick_document`·`make_input`·`ask_model`·`find_numbers`·`find_new_numbers`) → 기록 장치 `print_report`(Ch 2 13·Ch 4 06) → 조립 `run_check(question, system_text)`(줄마다 절 주석) → 실행 1 → 실행 2 → 칸별 비교(+`assert` 고른 문서 같음) → 정리 3줄
- 실행 1: 환불 `문서 0 유사도: 0.7636`·`입력 조각 수 | 57`·`남는 칸 | 391`·`환불은 결제일로부터 14일 이내에 신청합니다.<|im_end|>`·`새 숫자 | ['14']`·`False` / 무게 `문서 1 유사도: 0.5174`(배터리 문서)·`66`·`382`·`노을 워커 3의 무게는 약 150g 입니다.<|im_end|>`·`['150']`·`False`
- 실행 2: 환불 `79`·`369`·`7일 이내에<|im_end|>`·`[]`·`False` / 무게 `88`·`360`·`제공된 정보로는 확인할 수 없습니다.<|im_end|>`·`[]`·`True`. 비교 `달라진 칸 수: 9`(환불 4칸, 무게 5칸), 고른 문서·유사도 같음
- 설계 과정: 처음에는 실행 2를 출력 몫 64 → 8 또는 시스템 지시 빼기로 두려 했으나, 기기 셸에서 04절 지시를 넣어도 환불 답이 14일, 지시를 빼도 14일(08절과 같은 답)이라 차이가 작았음. 보류 지시에서는 환불 7일·무게 보류로 판정 칸이 뚜렷이 달라져 이 값을 고름. 결론은 「질문 두 개와 모델 하나로 한 번 실행해 관찰」로 한정하고, 보류 지시가 답이 있는 질문도 보류한 기기 셸 기록(초록 패스·해바라기 작전)과 07절 9절 결과를 b7·복습 5에 적음
- 사다리: L1~L4. 셀 하나에 함수 하나, 함수 본문 최대 10문장(`run_check`, 게이트 `long_function` 기준 10 이하가 되도록 기록장 첫 세 칸을 딕셔너리 한 줄로 만듦), 코드 셀 최대 12줄. 두 겹 호출 없음(`input_ids`를 따로 담음). 타입힌트 없음(05~08절과 같음). 함수 안에서 바깥 이름(`embedding_model`·`documents`·`document_vectors`·`tokenizer`·`model`·`output_budget`·`input_budget`·`abstain_sentence`)을 읽는다고 설명 셀에 적음(05~08절 방식). `upgrade_allow` 없음

## 앞 절에서 가져온 이름과 연속성 판단

- 같은 코드로 가져온 것: 02절 `dot_product`, 07·08절 `make_input`, 05·07·08절 `ask_model`, 07절 `find_numbers`·`find_new_numbers`, Ch 4 06절 `print_report`와 칸별 비교 셀, 준비 셀 경고 끄기 두 줄(01·04절), 모델 이름·판 번호 변수(03~08절 `model_name`·`model_revision`)
- 가져온 값: 04절 `practice_window = 512`·`output_budget = 64`·`input_budget` 식과 「남는 칸」, 04절 시스템 지시, 07절 `abstain_sentence`와 9절 보류 지시 문장, 04·07·08절 문서 세 개와 환불 질문, 02절 `normalize_embeddings=True`와 「길이 1인 벡터끼리는 점곱이 곧 코사인 유사도」, 08절 배터리 문장 23조각(노트북 4번 결과 읽기에서 대조)
- 새 이름: `embedding_model`·`embedding_name`·`embedding_revision`(02절은 `model`이었으나 `ask_model()`이 읽는 이름과 겹쳐 바꿨다고 노트북 3번에 적음), `documents`·`document_vectors`·`questions`·`pick_document`·`run_check`·`reports_1`·`reports_2`, 기록장 칸 이름 일곱 개
- 이름 「기록장」: Ch 2 13·Ch 3 06·Ch 4 06 실습과 같은 이름으로 씀
- 08절 「다음 학습」: Ch 6·11·15 문장을 09 b8로 옮기고(Ch 6 01 문장은 70자 때문에 둘로 나눔), 08 b8은 09절 링크와 두 문장으로 바꿈. 08 노트북 정리 끝 문장도 09 안내로 바꿈(`mdpatch.py`, 재실행 없음, 08 게이트 0 다시 확인)
- 뒤 챕터 연결(09 b8·노트북 정리): Ch 6 01·06, Ch 11, Ch 15 문장은 08절 작업자가 확인한 문장 그대로. Ch 9 문장은 Ch 9 01 `_src`(개선 전)에서 「문서를 미리 잘게 나누고 벡터로 바꿔 저장해 두는 준비 작업」, 「질문과 가장 가까운 청크 k개를 가져오는 것」, 「청크 k개 + 질문 → 답」을 확인하고 씀. 실습 폴더 모듈과 같은 이름·다른 모양 함수 문제는 없음(이 챕터 실습 폴더에 모듈 없음)

## 사실 주장 확인

- 노트북 출력으로 확인: 위 실행 1·2·비교 값, 버전, 컨텍스트 한도 32768, 임베딩 길이 384, 문서 조각 수 17·23·37, 벡터 모양 `(3, 384)`, 입력 한도 448
- 기기 셸에서만 확인했다고 적은 것(b7·복습 5): 이 실습 보류 지시 + 초록 패스 문서·질문 → `제공된 정보로는 확인할 수 없습니다.`, 해바라기 작전 문서·질문 → 같은 보류 문장, 지시 없이 환불 문서·질문 → `환불은 결제일로부터 14일 이내에 신청해야 합니다.`(08절 노트북 답과 같음). 기록은 `/tmp/ch05-09/proto.py`·`proto2.py` 출력
- 앞 절 결과로 인용한 것: 04절 20번 이은 문서의 답 7일(handoff §04), 07절 9절 문서 있음 첫 질문 보류(handoff §07), 08절 14일 답(08 노트북 6절)
- 계산으로만 구했다고 적은 것: 복습 3의 출력 몫 128일 때 남는 칸 305
- 실행하지 않았다고 적은 것: 유사도가 낮을 때 문서를 넣지 않는 기준, 다른 버전·기기, GPU, Windows·macOS

## 그림

- Mermaid 3장(PNG 직접 확인): 09-1 조립도(flowchart TB 7노드, viewBox 526), 09-2 실행 1 순서(sequenceDiagram, 처음 조립 함수·임베딩·언어 모델 순서에서 긴 라벨이 가운데 세로선과 겹쳐 임베딩·조립 함수·언어 모델 순서로 바꿈, 848), 09-3 두 실행 비교(LR 두 칸 + 칸 안 TB, 622)
- 삽화 1장: 09-4 카드 고르기와 돋보기(04-5 칸막이 쟁반 이어 씀). nano_banana_pro 16:9 2k, 1회 생성, 2크레딧(생성 전 잔액 2882). 채택 job `4943e44e-3da9-4c2f-8fe5-aee59089de54`. 오른쪽 답 카드에 세모 없이 별만 보이지만 관계가 읽혀 채택하고 그림 읽기를 저장 파일에 맞춤. 저장 PNG(1100×614)를 기기에서 다시 받아 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0
- 색(§5-3): 재료·바꾸는 값 초록, 노트북에서 정의한 함수 파랑, 답을 만드는 언어 모델 보라, 출력 값·틀린 답 노랑, 참여자 회색, 빨강 없음. 근거는 `09-figures.md`

## 바꾼 다른 파일

- `chapter.json` sections 끝에 `09-LLM-동작-원리-실습`(「LLM 동작 원리 실습: 문서를 골라 넣고 답 점검하기」, experiment) 추가. `_src/index.html`은 없고, 챕터 `index.html`은 빌드가 chapter.json으로 다시 만듦(「절 9개」)
- `_src/08-모델-선택-기준.html` b8 「다음 학습」, 08 노트북 정리 끝 문장, `author_08.py` 같은 문장(`mdpatch.py`)
- `labs/part1/ch05-llm-principles/README.md`에 09 노트북이 두 모델을 한 커널에 올린다는 문장 하나
- 옛 생성기 `make_sources.py`·`labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않음
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음

## 검토에서 볼 곳

- 결론 범위(b6 마지막 두 단락, b7 셋째·넷째 항목, 노트북 12·13번 결과 읽기, 복습 4·5): 보류 지시의 효과를 두 질문 이상으로 넓히지 않았는지, 기기 셸 기록과 노트북 출력이 구분되는지
- 유사도로 문서를 고르는 부분이 Ch 9 검색을 앞당겨 가르치지 않는지(노트북 2·6번, b4 구성 표, b8 Ch 9 문장), 03절 `largest_position()` 인용이 적절한지
- 삽화 09-4 비유(무늬 = 임베딩, 별 = 새 숫자)가 그림만으로 읽히는지, 09-2 참여자 순서(임베딩·조립 함수·언어 모델)와 도식 읽기 방향 말

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept-with-fixes(중 1, 하 3). 모두 반영했습니다.
- 09-1(중, 결정: 조각을 청크 뜻으로 쓰지 않음): b8 「문서를 작은 문서 덩어리(청크)로 잘라 … 가장 가까운 문서 덩어리 k개 … 문서 덩어리는 이 챕터에서 토큰을 뜻한 조각보다 큰 단위입니다.」, 노트북 정리 「질문과 가까운 문서 덩어리(청크)를 가져오는 검색 단계」. 챕터 전체 `_src`·생성기·그림 설명에 「조각(청크)」가 더 없음을 grep으로 확인
- 09-2: b7 첫 항목 「07절 주의 메모와 08절 영어 넷째 답에서 본 것처럼, 숫자 글자가 맞아도 틀린 뜻으로 쓴 답은 잡지 못합니다.」
- 09-3: b3 표 「05~08절 | 05·07·08절 `ask_model()`, 06절에서 본 뽑기를 끈 설정」, 그림 09-1 라벨 「ask_model() 05·07·08절<br>06절 뽑기 끔」·「find_new_numbers()<br>보류 문장 in 답」(viewBox 526, PNG 확인), 삽화 그림 읽기 「세 칸은 왼쪽에서 오른쪽으로 가는 가는 회색 화살표로 이어집니다.」
- 09-4: b7 새 항목(실행 2 값은 출력 몫 8·지시 빼기를 먼저 해 보고 기록장 칸 차이가 잘 보이는 보류 지시로 고름), b8 「성능 순위」(Ch 6 06 원문). 참고 자료 MiniLM 확인일 2026-09-16
- C-B1: 챕터 시수 `chapter.json` 16h 유지(09 30분은 실습 6h 안), `chapter-summary.md`에 기록
- 재실행 없음. 코드 셀 15, `outputs_sha256` `981329b4…` 그대로, 검사한 문장 368

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/09-LLM-동작-원리-실습.md`(08도 다시 만듦)
- 정리 대상(삭제하지 않고 목록만): `/tmp/ch05-09`(proto·proto2·proto3.py, reps1·reps08.json, visual 사본과 화면 캡처), `qa/upgrade/before/08-to-09/`(08 수정 전 사본)
- 챕터 검토(별도 세션)와 `chapter-summary.md`는 다음 단계(handoff `## 실습 → 챕터 검토`)


## §2-7 리팩터 (2026-09-21)

다시 정의 6개(dot_product·make_input·ask_model·find_numbers·find_new_numbers·print_report)를 빼고 가져옴. `pick_document`는 `document_vectors @ question_vectors[0]`·`np.argmax()`. 옛 7·8·9절(부품·기록 장치)을 「7. 부품 준비 — 가져온 함수 네 개」로 합쳐 뒤 절 번호 당김. 출력 리팩터 전과 같음(묶음을 풀어 한 번 더 실행해도 같음). 코드 셀 15 → 9, 코드 줄 124 → 84.
