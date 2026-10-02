# 06-temperature와-샘플링 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/06-temperature-sampling.*`).
생성기: `qa/upgrade/author_06.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 06`(환경 변수 없이). 설명만 고칠 때는 `mdpatch.py` → `--no-exec`(생성기를 다시 실행하면 출력이 지워짐).
수정 전 수치는 01절 작업 때 남긴 챕터 기록 `gates-before.json`의 06절 값입니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 2 | 0 |
| G2 | 3 | 0 |
| G3 | 2 | 0 |
| G4 | 0 | 0 |
| G5 | 7 | 0 |
| G6 | 36 | 0 |
| G7 | 3 | 0 |
| 합계 | 53 | 0 |
| 코드 셀 | 6 | 14 (준비 1 + 본문 13, 함수 정의 셀 4개) |
| 검사한 문장 | 143 | 391 (`gates-wip-06.json`) |
| 모델 실행 | `generate()` 6번(temperature 0.3·1.0 × 시드 3) | 내 컴퓨터의 Qwen2.5-0.5B-Instruct `generate()` 16번(뽑기를 끈 답 1 + temperature 0.3·1.0 × 시드 11·22·33·44·55 = 10 + temperature 1.0 같은 시드 다시 5), temperature 0.0 호출 1번은 생성 전 `ValueError`. API 호출 0, 비용 0 |

## 실행 환경

- 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`(`Qwen/Qwen2.5-0.5B-Instruct`@`7ae557604adf67be50417f59c2c2f167def9a775`). `run_section.sh`가 자동으로 씀. `/tmp`에 torch 설치 없음.
- 새 커널 실행 PASS(`PASS 06-temperature와-샘플링.ipynb: 14 cells`, `run_section.sh` 전체 약 53~56초). **반복 확인**: 새 커널로 두 번 실행해 `outputs_sha256` `df95f660…`이 같았고, 코드 셀 출력 글도 문자열 비교로 같음(`/tmp/ch05-06/run1.txt`·`run2.txt`). 노트북 안에서도 8절이 temperature 1.0 시드 다섯 개를 다시 실행해 `같은 답 수: 5 / 5`. 기기 셸 탐색 스크립트(`/tmp/ch05-06/probe1~3.py`)의 답도 노트북과 글자까지 같음.
- **다른 기기·버전 확인(노트북 밖, 클라우드 작업 컨테이너)**: Linux x86_64, Python 3.12.3, torch 2.8.0+cpu, transformers 4.56.2, 같은 모델·판 번호로 5·6절 답 11개(뽑기를 끈 답 + 시드 답 10)를 받아 **11개 모두 기기 출력과 글자까지 같음**. 같은 컨테이너에서 torch만 **2.5.1+cpu**로 바꾸자 뽑기를 끈 답은 같고 **시드 답 10개는 모두 다름**(예: 0.3·11 `"가을의 풍경 - 오프라인 서점의 전시회"<|im_end|>`, 1.0·11 `"봄빛 책의 화제 - 오프라인서점 가을 행사"…`; 7절 셈은 0.3 `5 | 4 | 5`, 1.0 `5 | 1 | 3`). 스크립트 `scratchpad/x86/cmp.py`(세션 임시 폴더, 교재에 없음)
- 메모리(기기 셸 `/tmp/ch05-06/probe4.py`): 모델 적재 뒤와 생성 뒤 `ru_maxrss` 3249MB(약 3.2GB). 입력 56조각이라 05절보다 가벼움.
- `verify.py --chapter` `PASS 8 sections / 93 code cells (max 17 lines)`(17줄은 개선 전 다른 절). `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-06/vis`에 05절 작업자 사본 복사, 공용 도구는 고치지 않음). 루트 여유 약 568MB(변화 없음).

## 소스·문서로 확인한 것 (transformers 4.56.2 설치본, 2026-09-16)

- `generation/utils.py` `_get_logits_processor`: 반복 벌점(`repetition_penalty != 1.0`이면, 뽑기와 관계없이) → `do_sample`일 때만 temperature(`!= 1.0`일 때) → top_k(`!= 0`) → top_p(`< 1.0`) 순서. `_sample`은 `torch.multinomial`로 뽑음
- `TemperatureLogitsWarper.__init__`: `temperature > 0`인 실수가 아니면 `ValueError`, 0.0이면 「If you're looking for greedy decoding strategies, set `do_sample=False`.」를 덧붙임(int 0은 덧붙이지 않음 — 기기 셸 확인). `__call__`은 `scores / self.temperature`
- `TopPLogitsWarper`: 오름차순 누적 확률이 `1 - top_p` 이하인 후보를 뺌 = 큰 순서로 더해 기준 이상이 되는 후보까지 남김(3절 `count_top_p()`와 같은 규칙, 경계 동률은 다루지 않음)
- `trainer_utils.set_seed`: `random.seed`·`np.random.seed`·`torch.manual_seed`·`torch.cuda.manual_seed_all`(과 설치된 가속기)을 한꺼번에 정함
- 모델 `generation_config.json`(판 7ae5576): `do_sample: true`, `temperature: 0.7`, `top_p: 0.8`, `top_k: 20`, `repetition_penalty: 1.1`. 기기 셸 확인: `top_k=20`을 넘긴 답 = 넘기지 않은 답(1.0·11), `top_k=0`이면 다른 답. 뽑기를 끈 5절 입력에 `repetition_penalty=1.0`을 넘기면 `"가을의 푸른 풍경 속 서점"<|im_end|>`로 바뀜 → 기본 반복 벌점이 04·05절 `do_sample=False` 생성에도 적용됐음(b7 메모)
- PyTorch 2.8 `docs/source/notes/randomness.rst` 첫 단락: 「Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms. Furthermore, results may not be reproducible between CPU and GPU executions, even when using identical seeds.」
- 뒤 챕터 파일 확인: Ch 22 01 노트북 셀 8 「temperature 값은 답을 고를 때의 무작위 정도입니다. 0으로 두면 매번 비슷한 답을 고릅니다.」, 셀 10 「temperature 값을 0으로 두어도 답 문장이 매번 똑같다고 보장하지는 않습니다.」, Ch 9 04 노트북 `init_chat_model("openai:gpt-5.4-mini", temperature=0)`, Ch 6 01 `_src` 「`temperature`, 출력 토큰 상한, `timeout`처럼 … 모든 제공자와 모델에서 같은 범위로 지원된다고 가정하지 않습니다」. Ch 6 노트북에는 temperature 인자가 없음(개선 전)

## 수정 전 주요 문제

- 기본 경로 금지·미교육 문법: 조건 표현식 `temperature if temperature > 0 else None`·`0.9 if … else None`(G1 2), `do_sample=temperature > 0`(비교 결과를 인자에 바로), `*` 키워드 전용 인자와 타입힌트 `-> str`, `**inputs`·`tokenizer(글)` 객체 호출·`with torch.inference_mode()`·`skip_special_tokens`·`pad_token_id`·`model.eval()`·`num_parameters()`·`f"{n:,}"`·f-string 형식 지정 `{temperature:.1f}`·`torch.tensor`·`torch.softmax(…, dim=0)`·`torch.isclose`·`for …, _, answer in`·`output[0, …shape[1]:]` 2차원 슬라이싱. 15줄 넘는 셀(G2), 두 겹 호출 2곳, 첫 줄 주석 없는 셀 2개와 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」 3곳(G3)
- `set_seed`·`top_p`·temperature·로짓을 뜻 → 일상 예 → 코드 순으로 풀지 않음. 03절에서 직접 만든 소프트맥스와 이어지지 않고 `torch.softmax`를 씀
- 모델 기본 생성 설정(`top_k` 20, `repetition_penalty` 1.1)이 모든 샘플링 호출에 적용된다는 사실을 적지 않음(「top-p와 최대 생성 길이도 고정」만 적음)
- 시드 3개씩이라 `unique=3/3` 두 줄로 차이를 볼 수 없었고, 시드 고정의 한계를 문서 일반론으로만 적음(확인 없음)
- 제목 셀·준비물·핵심 그림·결과 읽기 없음(G5 7). 설명 셀이 `generate()`·`set_seed()`·`do_sample`·temperature 등으로 문장 시작(G6 english_start 다수), 70자 넘는 문장 13개(G6 36). 옛 Excalidraw 도식 1장, Mermaid 0·삽화 0·설계표 없음(G7 3)
- b3 「04절과 05절에서는 모델이 받을 수 있는 입력 길이와 긴 문맥에서의 관찰 범위를 구분했습니다」·「03절에서는 어텐션이 … 가중치를 두는 방식」이 개선된 03~05절과 어긋남(handoff §05 → §06), b3 `torch.inference_mode()` 설명은 개선된 04·05 모양과 다름. 복습 4문항에 난이도 표시 없음

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「같은 프롬프트에서 temperature를 바꾸면 반복 출력의 다양성이 어떻게 달라질까요?」를 본문 「이 절의 질문」 두 개로 이어 씀, 개선 전 데이터 — 요청 「오프라인 서점의 가을 행사 이름을 한국어 5어절 이내로 하나 제안하세요.」·사용자 메시지 하나·temperature 0.3·1.0·시드 11·22·33·top_p 0.9·교재 점수 [2.0, 1.0, 0.0] — 유지): 제목(할 일 3, 생성 16번·비용 0·1분 안팎, 모델 약 1GB·메모리 약 3.2GB, transformers 4.56.2·torch 2.8.0·모델·revision, 시드 한계 10절 안내) → 오늘 볼 그림(06-1) → 1 준비(`math`·`torch` 버전·`set_seed` import) → 2 `softmax()`(03절과 같은 코드)·`divide_scores()` 정의·교재 점수 temperature 0.3·1.0·2.0 → 3 `count_top_p()` 정의·`top_p = 0.9`로 남는 후보 1·2·3 → 4 모델(03~05 모양)·기본 생성 설정 다섯 줄 → 5 입력 56조각·출력 몫 32·뽑기를 끈 답 → 6 시드 뜻·`ask_with_sampling(temperature, seed)` 정의·10번 실행 → 7 서로 다른 답·끝 표시·「가을」 셈 → 8 같은 시드 다시 `5 / 5` → 9 값 바꿔 보기 temperature 0.0 `ValueError` → 10 시드가 보장하는 범위(설명만) → 정리
- 시드를 44·55까지 늘림(세 번씩은 너무 적음, 결과를 보기 전 11·22·33 다음 두 수로 정함). 출력 몫 24 → 05절과 같은 32(끝 표시로 끊김을 셈). 개선 전 T=0.5 교재 확률(0.8668)은 복습 3 적용 문제로 옮김
- 기본 경로에서 조건 표현식·`**` 풀기·`with`·`tokenizer(글)`·`skip_special_tokens`·`pad_token_id`·f-string 형식 지정·목록 곱하기·`zip`·`max`·`sum`·내포식·`Path`·`raise`·`try/finally`·상속·`threading`·`@`·`BaseModel`·`*args`를 쓰지 않음. `import torch`는 버전 출력에만(03절 텐서 패키지로 한 문장). 새로 쓴 모양: `set()`으로 서로 다른 답 세기(Ch 2 03), `try/except ValueError as error`(Ch 2 05), temperature를 키로 한 딕셔너리 `answers_by_temperature[temperature] = answer_list`, `for` 안 `break`(Ch 2 02). 함수 네 개는 타입힌트 없이 셀 하나에 하나, 정의·호출 분리
- 새 생성 인자 `do_sample=True`·`temperature`·`top_p`와 `set_seed`는 처음 쓰는 자리에서 뜻 → 일상 예(제비뽑기 통, 결선 투표, 주사위 눈 목록) → 코드로 풂. 로짓·top_k·생성 설정도 용어 표에
- 본문 10블록 전체를 다시 씀: 이 절의 질문 두 개, b3 01·03·04·05절 개선본 기준(03 `softmax()`·`math.exp()`, 04 출력 몫·끝 표시, 05 같은 입력 같은 답, Ch 2 03 `set()`·05 `try/except`), 비유(블록 두 그릇, 01-5·04-5·05-5 블록을 이어 씀), 용어 7개 표, 조각 하나를 뽑는 순서 → temperature(말 → 식 → 숫자) → top_p, 실행 예제 해설(넘긴·넘기지 않은 설정, 두 temperature 답), 실험 해석(가짓수 5·5로 다양성 비교 불가, 끝 표시 4·1과 「가을」 5·1은 품질이 아니고 일반화하지 않음, 시드 되풀이, x86·torch 2.5.1 확인과 PyTorch 문서, temperature 0.0 ValueError, 뒤 챕터 temperature 0 연결은 파일에서 확인한 문장만), 주의 메모 8개, 복습 5문항(기초 2·적용 1·분석 2)
- 기기 셸에서만 확인하고 본문 주의 메모에 「노트북에 넣지 않음」으로 적은 것: 첫 조각 후보 점수 1위 `"` 14.28·2위 `1` 13.87(3위는 입력에 있는 바이트 조각), 후보 20개로 반복 벌점 없이 계산한 temperature 0.3 확률 0.6752·0.169(`probe2.py`), `repetition_penalty=1.0`이면 뽑기를 끈 답이 바뀜(`probe3.py`), 시드 없이 두 번 뽑으면 다른 답(`probe4.py`)
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/06-temperature-sampling.*`는 본문에서 뺌(원본 `before/figures/`, 옛 파일은 삭제하지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 06-1 TB(초록 입력 → 보라 모델 → 회색 점수·확률·남은 후보 → 노랑 뽑은 조각 → 모델로 되돌아감), 06-2 TB 세 갈래(초록 교재 점수 → 노랑 확률·남는 후보 수), 06-3 TB 세 갈래(초록 같은 입력 → 노랑 뽑기 끈 답·0.3·1.0 셈), 06-4 TB 두 줄기(노랑 6·8절, 초록 temperature 0.0 → 노랑 ValueError → 초록 뽑기 끄기). viewBox 폭 323·약 640(06-2 줄바꿈 뒤)·715·460으로 모두 860 미만. 06-2는 처음 확률 한 줄이 상자에서 두 줄로 넘어가 `<br>`로 나눠 다시 렌더
- 색: 입력·교재 점수·노트북에서 넣은 값 초록, 출력 확률·답·셈·ValueError 노랑(받아서 출력한 오류, 규격 §5-3), 실행한 모델 보라, `generate()` 안에서 출력하지 않는 값 회색, 빨강 없음
- 삽화 06-5(블록 두 그릇): 1회차 job `f8949249-810e-4231-a815-2fc549735df1` 채택, 2크레딧(생성 전 잔액 2888). 요청 그릇마다 12개 → 결과 11개씩(왼쪽 파랑 10·주황 1, 오른쪽 파랑 6·주황 3·초록 2). 두 그릇의 블록 수가 같고 「거의 한 색 vs 섞임」 관계가 그대로라 채택, 그림 읽기는 저장 파일 개수로 씀. 저장 PNG(1100×614)를 기기에서 다시 받아 채택 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0

## 검토에서 볼 곳

- 7절 셈 세 가지(서로 다른 답·끝 표시·「가을」)를 고른 판단과 해석 범위(b6 둘째·셋째 단락, 복습 4). 「가을」 셈은 결과를 본 뒤 더한 값이라 품질 지표가 아니라고 적음. torch 2.5.1에서 1.0의 「가을」 수가 3으로 바뀐 것을 b6에 적음
- 시드 한계 문장(노트북 10절, b6, 복습 5): 같은 기기 두 번 + x86_64 같은 버전 같음 + torch 2.5.1 다름은 이 세션의 확인이고, GPU·Windows·macOS는 실행 안 함. x86 확인은 노트북 밖(클라우드 작업 컨테이너)이라는 표시
- 뒤 챕터 연결(b6 마지막 단락, b7, 노트북 정리): Ch 22 01 노트북·Ch 6 01 `_src` 문장만 인용하고, 서비스 모델의 temperature 0 = `do_sample=False`라고 쓰지 않음. Ch 6·Ch 9는 아직 개선 전이라 문장이 바뀔 수 있음
- 기본 반복 벌점이 04·05절 생성에도 적용됐다는 b7 메모(04·05 본문은 고치지 않음 — 결과는 그대로 유효). meta는 개선 전 「강의 1.5h · 실습 1h」 유지

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-B.md`

- 판정 accept(중 0, 하 3, 공통 C-B2). 모두 반영했습니다.
- 06-1: [19] 「반복 벌점 1.1은 이 절의 모든 호출에 쓰입니다. 기본값 top_k 20은 뽑기를 켠 호출에서만 쓰입니다.」, b5 같은 뜻(「설치한 4.56.2 소스에서 확인」), [5] 「반복 벌점(4절에서 봄)을 적용한 점수에서 가장 큰 후보」, b4 도식 읽기 끝 문장
- 06-2: 그림 06-1 화살표 「반복 벌점 1.1 · temperature로 나누기」, 캡션 읽는 법(`기본 repetition_penalty: 1.1`)·alt·노트북 [1]·도식 읽기(G6 70자·영문 시작 때문에 두 문장, 「설정 temperature와」). PNG 확인
- 06-3: b6·7절 설명에 「「가을」 셈은 6절에서 `봄행사` 답을 본 뒤 더한 셈입니다」, [39] 「노트북 밖에서, 다른 CPU 기기」, [5] 소프트맥스 목록 이름 `probabilities`, [29]·b5 「한 후보에 몰리지 않은 자리가 있었습니다」(b5는 첫 조각 점수가 주의할 점 첫 항목에 있다고 가리킴)
- C-B2: `qa/upgrade/evidence/06-seed-platform.md`(답 11개 표, 06 작업·검토 B·마감 세션 실행 기록)와 `evidence/06_seed_platform.py`(노트북 5·6절과 같은 계산 + 노트북 출력 비교). 마감 세션 기기(aarch64·torch 2.8.0+cpu)에서 `노트북 출력과 같은 답 수: 11 / 11`
- 재실행 없음. 코드 셀 14, `outputs_sha256` `df95f660…` 그대로, 검사한 문장 399

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/06-temperature와-샘플링.md`
- 정리 대상(삭제하지 않고 목록만): `figures/06-temperature-sampling.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-06`(탐색 스크립트 probe1~4·run1/run2 출력 글·visual 사본·reps JSON)
- 챕터 안 옛 생성기 `make_sources.py`와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않았습니다(개선본을 덮어씀)
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음
- 07절(개선 전) `_src` b3 「앞 절에서 같은 프롬프트와 모델도 샘플링 설정과 난수 상태에 따라 다른 문자열을 만들 수 있음을 확인했습니다」는 개선된 06과 대체로 맞지만, 07 노트북의 `generate()`는 06 개선 전 모양(조건 표현식·`**inputs` 등)이라 07 작업자가 고칠 곳(handoff에 적음)


## §2-7 리팩터 (2026-09-21)

03절 `softmax`·05절 `ask_model`을 `llm_tools.py`에서 가져옴. `divide_scores`는 배열 나누기로 바꿔 뺌, 표는 `np.round(…).tolist()`로 목록 모양 유지. 생성 16번 출력이 리팩터 전과 글자까지 같음. 코드 셀 14 → 12, 코드 줄 123 → 102.
