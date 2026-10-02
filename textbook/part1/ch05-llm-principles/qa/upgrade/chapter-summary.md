# Ch 05 LLM 동작 원리 — 챕터 요약 (다음 챕터 작업자용)

작성 2026-09-16(품질 개선 8절 + 실습 절 09 + 별도 세션 검토 1차 A·B 반영 뒤). 규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md` §6. 앞 챕터 요약: `textbook/part1/ch01-development-environment/qa/upgrade/chapter-summary.md`, `textbook/part1/ch02-python/qa/upgrade/chapter-summary.md`, `textbook/part1/ch03-git-github/qa/upgrade/chapter-summary.md`, `textbook/part1/ch04-data-tools/qa/upgrade/chapter-summary.md`. 절 사이 인계 원문: `qa/upgrade/handoff.md`(절마다 「새로 가르친 것」「아직 안 가르친 것」 전체 목록). 검토: `qa/upgrade/review-round1-A.md`(01~05)·`review-round1-B.md`(06~09), 끝에 「반영 결과」.
절: 01 토큰화와 한국어 효율 · 02 임베딩과 의미 유사도 · 03 어텐션 직관 · 04 컨텍스트 윈도 · 05 컨텍스트 로트 · 06 temperature와 샘플링 · 07 환각의 구조적 원인 · 08 모델 선택 기준 · 09 LLM 동작 원리 실습(모두 experiment). **API 키 불필요, 인터넷 서비스 모델 호출 0번**, 모든 모델은 내 컴퓨터(CPU)에서 실행. 코드 셀 119개(12·15·16·15·13·12·13·14·9, 2026-09-21 §2-7 리팩터 뒤 — 전 132개·코드 1033줄 → 911줄), 게이트 9/9(G1~G7 0, 수정 전 262건), Mermaid 35장·삽화 9장(대기 없음).

## 1. 새로 가르친 개념·API·함수·용어

### 절별 (노트북에서 실행한 것만)

| 절 | 모델(모두 판 번호 고정) | 새 API | 직접 만든 함수 | 용어 표 |
|---|---|---|---|---|
| 01 | 토큰화기 `openai-community/gpt2`·`klue/bert-base` | `AutoTokenizer.from_pretrained(이름, revision=)`, `vocab_size`, `tokenize()`(조각 글자, 특수 토큰 없음), `encode()`(ID 목록, KLUE는 `[CLS]`·`[SEP]` 더함), `decode()`, `convert_ids_to_tokens()`, `json.loads()`(Ch 4 `article-text.json` 읽기) | 없음 | LLM, 토큰, 토큰화·토큰화기, 어휘, 토큰 ID, 특수 토큰, 판 번호(revision), 바이트 |
| 02 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | `SentenceTransformer(이름, revision=)`, `get_sentence_embedding_dimension()`(384), `max_seq_length`(128), `model.tokenizer.tokenize()/encode()/convert_ids_to_tokens()`(`<s>`·`</s>` 더함), `model.encode(문장 목록)`(NumPy 배열 `(행, 384)`), `normalize_embeddings=True`, `import math`·`math.sqrt()`, **8절 `import numpy as np`·`np.array()`·`@`(점곱)·`np.linalg.norm()`(§2-7, 반복문 판과 값 비교)** | `dot_product(first, second)`·`vector_length(vector)`·`cosine_similarity(first, second)`(반복문 판, 02만 씀) | 임베딩, 벡터, NumPy 배열, 점곱, 벡터의 길이, 코사인 유사도, 정규화 |
| 03 | `Qwen/Qwen2.5-0.5B-Instruct`(eager) | `AutoModelForCausalLM.from_pretrained(…, attn_implementation="eager")`, `config.num_hidden_layers`(24)·`num_attention_heads`(14), `encode(글, return_tensors="pt")`(텐서), 모델 객체 호출 `model(input_ids=…, output_attentions=True)`, `outputs.attentions`, `.shape`·`.tolist()`, NumPy 표 `@` 벡터·비중 `@` 표·`np.exp()`·`sum()`·`np.round()`·`mean(axis=0)`·`np.argmax()`(§2-7). **심화 셀만**: `outputs.logits[0][자리].tolist()`·`배열 > 값`·`np.sum()` | `softmax(scores)`·`average_heads(layer_table, row_number)`(둘 다 NumPy; §2-7에서 `weighted_sum`·`largest_position`은 `@`·`np.argmax()`로 바꿔 뺌) | 어텐션, 어텐션 점수, 소프트맥스, 비중, 가중합, 층과 머리, 텐서 |
| 04 | Qwen | `config.max_position_embeddings`(32768), `tokenizer.model_max_length`(131072), 메시지 목록 `[{"role": "system", "content": …}, {"role": "user", …}]`, `apply_chat_template(메시지, tokenize=False, add_generation_prompt=True)`, `model.generate(input_ids=, max_new_tokens=, do_sample=False)`, `transformers.logging.set_verbosity_error()` | `make_document(repeat)`·`make_input_text(document_text)` | 컨텍스트 윈도, 시스템 지시, 메시지와 역할, 채팅 템플릿, 토큰 예산(`입력 한도 = 전체 한도 - 출력 몫`), **출력 몫**(교재에서 정한 이름 = `max_new_tokens`), 끝 표시 `<|im_end|>` |
| 05 | Qwen | 새 API 없음 | `make_document(filler_count, fact_place)`·`make_input_without_system()`·`make_input_with_system()`·`ask_model(input_text)` | 컨텍스트 로트(입력 길이 기준), 근거 문장, 무관한 문장, 근거 앞 문장 수, 정답 판정, 기본 지시 |
| 06 | Qwen | `from transformers import set_seed`, `model.generation_config`(기본 `do_sample` True·`temperature` 0.7·`top_p` 0.8·`top_k` 20·`repetition_penalty` 1.1), `generate(…, do_sample=True, temperature=, top_p=)`, `import torch`는 `torch.__version__`만 | `count_top_p(probabilities, cutoff)`·`ask_with_sampling(temperature, seed)` + `llm_tools`에서 `softmax`·`ask_model`(§2-7; `divide_scores`는 배열 나누기로 바꿔 뺌) | 로짓, 샘플링, temperature, top-p, top-k, 시드, 생성 설정 |
| 07 | Qwen | 새 API 없음. `isdigit()`, `not in` | `make_input(system_text, user_text)`·`find_numbers(text)`·`find_new_numbers(answer, source_text)` + `llm_tools`에서 `ask_model`(§2-7) | 환각, 주장, 근거, 사전학습(이 모델은 그 뒤 사후 학습도 거침, 모델 카드), 다음 조각 예측, 답변 보류, 판정 규칙 |
| 08 | Qwen + `HuggingFaceTB/SmolLM2-135M-Instruct`(EXAONE-3.5-2.4B는 카드만) | `model.num_parameters()`, `model.dtype`(`torch.float32`), `time.perf_counter()`(Ch 2 12) | `run_evaluation(items)`(튜플 반환)·`load_candidate(model_name)` + `llm_tools`에서 `ask_model`·`find_numbers`·`make_input`(§2-7) | 모델 카드, 작업 종류(task), 라이선스, 필수 조건, 파라미터, 평가 자료, 선택 기준 |
| 09 | Qwen + MiniLM(한 커널) | 새 API 없음 | `pick_document(question)`(`@`·`np.argmax`)·`run_check(question, system_text)` + `llm_tools`에서 `ask_model`·`find_new_numbers`·`make_input`·`print_report`(§2-7) | 새 용어 없음 |

### Python 쪽에서 Ch 5가 새로 쓴 모양 (모두 처음 쓰는 자리에서 한 문장씩 풀었음)

- 함수 정의는 **타입힌트 없음**(목록과 NumPy 배열·텐서를 함께 넘기므로), 셀 하나에 하나, 함수 안에서 바깥 이름(`tokenizer`·`model`·`output_budget`·`system_text`) 읽기, 08은 「바깥 이름에 후보를 담고 함수 부르기」
- 두 겹 `for`로 자리마다 곱해 더하기(§2-7 뒤에는 02절 반복문 판만 남고 03은 NumPy `@`), `for`+`if`로 최댓값 자리 찾기(§2-7 뒤 `np.argmax()`, `max()`·`index()` 안 씀), `int(n / 2)`(`//` 안 씀), 세 칸 목록 풀어 담기 `for a, b, c in conditions:`, `answer.replace("\n", " ")`로 한 줄 출력, 표 모양 `print(a, "|", b)`와 라벨 줄, `set()`으로 서로 다른 답 세기(06), `try/except ValueError as error`(06), 튜플 반환(08), 딕셔너리 값에 목록(08), 텐서 `.tolist()` 뒤 목록 인덱스·슬라이싱
- 기본 경로 132셀(§2-7 뒤 119셀)에서 조건 표현식·내포식·`lambda`·f-string 형식 지정·f-string 안 식·목록/글 곱하기·`zip`·`max`·내장 `sum`·`enumerate`·`**` 풀기·`with torch.inference_mode()`·`tokenizer(글)` 객체 호출·데코레이터 `@`·`BaseModel`·`*args`·`Path`·`raise`는 0건(검토 A·B AST). NumPy 행렬곱 기호 `@`와 배열 메서드 `sum()`은 §2-7 뒤 02·03절부터 씀

## 2. 반복해 쓴 모델·함수·데이터·비유·이름

- **모델 이름**: 변수 `model_name`·`model_revision`·`tokenizer`·`model`(03~08 같은 이름). 09는 임베딩 모델을 `embedding_model`로 따로 부름
- **입력 모양**: 04~09 모두 `apply_chat_template(…, tokenize=False, add_generation_prompt=True)` → `encode(…, return_tensors="pt")` → `generate(input_ids=, max_new_tokens=, do_sample=False)` → `decode(새 조각)`. 답 끝의 `<|im_end|>`를 **그대로 출력**(`skip_special_tokens` 안 씀) → 끝 표시가 있으면 출력 몫 안에서 끝남, 없으면 끊김
- **출력 몫 값**: 04 64·8, 05·06 32, 07·08·09 64. 연습용 한도 512, 입력 한도 448(04·09)
- **시스템 지시 문장**: 04·05·09 `"주어진 문서 범위에서만 답하세요."`, 07·09 보류 지시(보류 문장 `"제공된 정보로는 확인할 수 없습니다"`). 시스템 메시지가 없으면 Qwen 기본 지시 「You are Qwen, created by Alibaba Cloud. You are a helpful assistant.」가 들어감
- **데이터**: 01 `오늘 주문 상태를 확인해 주세요.`(GPT-2 39 / KLUE 9)·환불 7일 문장 쌍·Ch 4 기사 A10 `text`, 02 취소 문장 네 개(0.8987 등)·부정문 0.6716, 03 「상품 A는 파란색이고 상품 B는 노란색입니다. 상품 B는」, 04 환불 문장 20번 문서(400조각), 05 「해바라기 작전의 확인 코드는 314159입니다.」+무관한 문장 2·20·60개, 06 「오프라인 서점의 가을 행사 이름…」, 07·08·09 지어낸 「해바라기 연구소 초록 패스」(300만 원)·「노을 워커 3」(4200mAh), 09 새 질문 「노을 워커 3의 무게는 몇 g인가요?」
- **「조각」은 이 챕터 내내 토큰을 뜻함**(「입력 56조각」「출력 몫 64조각」「입력 조각 수」). 청크는 「문서 덩어리(청크)」로만 씀(09 b8, 검토 09-1)
- **비유와 삽화**: 01-5 나무 쟁반 홈과 정육면체·막대(블록 = 토큰) → 02-5 둥근 판 연필 방향 → 03-5 주스 층 컵(층 두께 = 비중) → 04-5 칸막이 쟁반(빈칸 = 출력 몫, 쟁반 밖 = 넘친 입력) → 05-5 쟁반 세 개(블록 = 문장, 주황 블록 자리) → 06-5 블록 두 그릇(temperature) → 07-5 모양은 맞지만 그림이 틀린 퍼즐 조각 → 08-5 빵 썰 도구 고르기 → 09-4 카드 꽂이·칸막이 쟁반·돋보기. 일상 예: 낱말 카드, 지도 위도·경도, 달걀판, 신청서 양식, 긴 회의록, 제비뽑기 통, 영수증 없는 가계부, 같은 시험지, 제품 설명서

## 3. 09 실습 절 주제와 결과

- 「LLM 동작 원리 실습: 문서를 골라 넣고 답 점검하기」(30분, 따로 과제 없음). 문서 세 개(04 환불, 07 배터리·초록 패스)에서 02절 유사도로 문서를 고르고(`pick_document`), 04절 템플릿으로 조각 수·남는 칸을 세고, 뽑기를 끈 `ask_model()`로 답을 받아, 07절 `find_new_numbers(answer, input_text)`·보류 문장으로 판정. 기록장 칸 7개, `print_report()`
- 실행 1(04절 지시): 환불 `0.7636`·57조각·`환불은 결제일로부터 14일 이내에 신청합니다.<|im_end|>`·`['14']`(문서의 7일을 바꿈), 무게 배터리 문서 `0.5174`·66조각·`약 150g`·`['150']`(지어냄)
- 실행 2(값 하나 `system_text` → 보류 지시): 환불 79조각·`7일 이내에<|im_end|>`·`[]`, 무게 88조각·보류 문장 `True`. `달라진 칸 수: 9`, 고른 문서·유사도는 같음(`assert`)
- 결론은 「질문 두 개·모델 하나·한 번 실행」으로 한정. 같은 보류 지시가 답이 있는 질문(초록 패스·해바라기 작전)을 보류한 것은 기기 셸 기록

## 4. 다음 챕터(Part 2 Ch 06 LangChain 시작)가 이어받을 것

Ch 06은 실제 인터넷 서비스 모델을 `init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none")`(규격 §3)로 부릅니다. Ch 5에서 로컬 모델로 배운 것이 어떻게 이어지는지는 아래와 같이 씁니다. **Ch 5는 서비스 모델을 한 번도 호출하지 않았으므로, 아래 「API에서」 쪽은 모두 Ch 06이 실행으로 확인해야 합니다.**

- **temperature**: Ch 5 06은 transformers에서 temperature가 **뽑기를 켠 호출(`do_sample=True`)에서만** 쓰이고, 뽑기를 켠 채 `temperature=0.0`이면 생성 전에 `ValueError`, 「temperature 0」에 해당하는 설정은 `do_sample=False`라고 가르쳤습니다. 뽑기를 끈 답은 같은 기기·버전에서 글자까지 같았습니다(05·06·07 새 커널 두 번). 시드 답도 같은 기기에서는 같았지만 torch 판이 바뀌면 달라졌습니다(`evidence/06-seed-platform.md`). → Ch 06은 **API의 `temperature=0`을 `do_sample=False`와 같다고 쓰지 않습니다**(06 b6도 그렇게 쓰지 않음). 규격 §3 Ch 22 시범에서 temperature 0에서도 글자 수가 398 → 381로 달랐으므로, 「매번 비슷한 답, 똑같다고 보장하지 않음」으로 씁니다(Ch 22 01 셀 8·10 문장과 같음). Ch 5가 본 반복 벌점 1.1·top_k 20 같은 모델 파일 기본값은 서비스 모델에서 보이지 않을 수 있다는 점을 연결 문장으로 둘 수 있습니다(확인 전 단정 금지)
- **출력 몫**: Ch 5 = `max_new_tokens`(04 용어 표), 모자라면 **오류 없이 답이 끊기고 끝 표시 `<|im_end|>`가 없음**(04 `새 조각 수: 8`). 입력 한도는 `전체 한도 - 출력 몫`. 같은 값을 **Ch 06 01·02·06 `_src`는 「출력 상한」**(개선 전 노트북 `max_tokens=180`), **Ch 08 01은 「출력 예약분」**(`max_tokens=300`)이라 부릅니다. 04 용어 표에 「Ch 6에서는 같은 뜻의 값을 출력 상한, Ch 8 01절에서는 출력 예약분」을 적어 두었으니, Ch 06 작업자는 처음 쓰는 자리에서 「Ch 5 04절의 출력 몫(`max_new_tokens`)과 같은 뜻」 한 문장으로 잇고 이름을 정합니다. API 응답에서 끊김을 알아내는 방법(응답 메타데이터 등)은 Ch 5에서 가르치지 않았습니다(Ch 5는 끝 표시 글자로만 판단)
- **시스템 지시와 메시지**: Ch 5는 딕셔너리 메시지 목록 `{"role": "system"/"user", "content": …}`과 `apply_chat_template`으로 **템플릿이 붙인 표시 조각(04 `13`)과 기본 지시까지 눈으로** 봤습니다. 서비스 모델은 템플릿을 제공자 쪽에서 붙이므로 그 글이 보이지 않습니다. Ch 06의 `SystemMessage`·`HumanMessage`(또는 튜플)는 「04절 역할 딕셔너리와 같은 역할·내용 묶음」으로 이을 수 있습니다. Ch 5 05에서는 시스템 지시 한 문장으로 가운데 자리 오답 3개가 모두 맞는 답으로 바뀌었고, 07·09에서는 보류 지시가 답이 있는 질문도 보류하게 했습니다 → **지시의 효과를 일반화하지 않는다**는 태도를 이어 씁니다
- **환각 판정**: Ch 5 07의 판정 규칙은 새 숫자(`find_new_numbers`: 입력에 없던 숫자)·정답 숫자(글자 포함)·보류 문장 세 가지이고, 숫자 없는 주장·다른 말로 한 보류·번호 목록의 1·틀린 뜻의 맞는 숫자(08 `4200 * 1000 = 420`)는 놓칩니다. 환각 설명은 「이 로컬 `generate()` 계산에는 찾아보는 단계가 없음」까지이고, OpenAI 2025 글은 여러 설명 가운데 하나로만 인용했습니다. Ch 06 01 복습 4(거부된 메시지를 환각으로 기록하지 않음)와 이어집니다. 서비스 모델 답에 이 함수를 쓰려면 노트북이 독립이라 다시 정의해야 하고, 판정 한계도 함께 적습니다
- **모델 선택**: Ch 06 01 `_src` b3은 「Ch 5의 모델 선택표」라고 부르지만, Ch 5 08에는 「선택표」라는 말이 없고 **후보 표 → 필수 조건(작업 종류·라이선스) → 평가 자료로 재기 → 미리 정한 선택 기준**으로 가르쳤습니다. Ch 06 작업자는 「Ch 5 08절의 필수 조건과 선택 기준」으로 고쳐 씁니다. 08의 기준 값(한국어 정답 3개·메모리 어림 2.0GB)과 출력 몫 64는 **탐색 실행 뒤 정한 교재 예**라고 본문 b7에 밝혔습니다(검토 08-1). Ch 06 06의 토큰·비용·지연 비교는 08의 「한 번 잰 시간은 모델 속도가 아님」「같은 답 길이로 여러 번」과 이어지고, 09 b8은 Ch 06 06 원문대로 「성능 순위를 만들지 않습니다」를 인용합니다
- **토큰 수**: Ch 5 01은 같은 문장이 토큰화기마다 39·9·23·47조각으로 다름을 봤습니다. 서비스 모델의 사용량 토큰 수는 제공자 토큰화기 기준이므로 Qwen 조각 수와 비교하지 않습니다
- **뒤 챕터 인계(검토 A C-5·B C-B3)**: (1) MiniLM은 `<s>`·`</s>`를 더해 ID가 조각보다 2개 많고, 평균 합치기와 128 한도가 특수 토큰을 포함함(02). (2) Qwen은 03절 문장 뒤에 노란색을 먼저 잇지 않았음(03 심화 셀 출력: 1위 ` 상` 0.2224, 파란색 첫 조각 2위 0.1008, 노란색 첫 조각 0.0087·더 큰 후보 14). (3) Qwen 생성 설정의 반복 벌점 1.1은 `do_sample=False`에도 적용되고, top_k·top_p·temperature는 뽑기를 켠 호출에서만 적용(transformers 4.56.2 `generation/utils.py` 1143·1252행). 04·05의 「가장 큰 후보」는 반복 벌점을 적용한 점수 기준. (4) **컨텍스트 로트 정의는 Ch 8 05절과 같은 「입력 길이」 기준**이고, Ch 5 05 노트북이 본 것은 길이 저하가 아니라 **근거의 자리에 따른 차이**(lost in the middle로도 보고됨). Ch 8 05는 근거를 가운데에 두는 규칙을 씀. (5) 출력 몫·출력 상한·출력 예약분 세 이름(위). (6) **Ch 9 01 `_src` 42행은 청크를 「문서를 검색 단위로 자른 조각」으로 정의 → Ch 9 작업자는 청크를 「조각」으로 풀지 말 것**(Ch 5 조각 = 토큰). (7) Qwen2.5-0.5B-Instruct는 사전학습 뒤 사후 학습(post-training)을 거친 모델이고, Ch 5는 「사후 학습」을 용어로 가르치지 않음. (8) 뒤 챕터 문장 확인 기록: Ch 6 01 b3·50행·복습 4, Ch 6 06(가격 기준일·성능 순위), Ch 9 01·04·05, Ch 11 01(질의셋), Ch 15 02(Correctness·Groundedness), Ch 22 01 셀 8·10 — 모두 **개선 전 파일**이라 그 챕터가 개선되며 문장이 바뀌면 Ch 5 03 b7·06 b6·07 b7·08 b7·09 b8을 다시 확인
- Ch 4 연결 유지: 01 노트북은 `labs/part1/ch04-data-tools/data/article-text.json`을 읽기만 함(SHA-256 `e241854443edac502e0a9e090191ace34dbced1885a600db3af29a20a93103d1`, 마감 뒤에도 같음)

## 5. 아직 가르치지 않은 것 (Ch 06이 설명 없이 전제하면 안 되는 것)

- **서비스 모델**: API 키·`.env`·`init_chat_model`·LangChain 전체, 메시지 클래스(`SystemMessage` 등), 응답 객체·`usage_metadata`·`response_metadata`, 스트리밍, 구조화 출력, 타임아웃·재시도·폴백, 요금 계산. Ch 5에는 `reasoning_effort` 같은 추론 설정도 없음
- **로컬 모델 쪽 미실행**: `tokenizer(글)` 객체 호출·`**inputs`·`attention_mask`·`pad_token_id`·`skip_special_tokens=True`, `with torch.inference_mode()`/`no_grad`, `torch.softmax`·`torch.topk`·`import torch`로 텐서 계산(06은 버전 출력만), `outputs.logits`는 **03 심화 셀에서 한 자리만**(기본 경로 전제 금지), `top_k`·`repetition_penalty`·`min_p` 인자 넘기기, `num_return_sequences`, `torch_dtype`·양자화, 32768 근처 긴 입력, 잘라내기 옵션(`truncation`), 첫 조각 시간·반복 측정의 가운데 값, `model.similarity()`, GPU
- **평가·검색**: 비율 지표(정확도·환각률 %), LLM 판정자·의미 비교 평가(Ch 15), 검색·벡터스토어·청크·RAG(Ch 9), 질의셋 평가(Ch 11)
- **Python**: Ch 4 요약 §5 목록 그대로 — 조건 표현식·f-string 형식 지정과 f-string 안 식·목록/글 곱하기·`zip`·`max`·`sum`·`enumerate`(Ch 2 02에서 배웠지만 Ch 5 기본 경로에서 안 씀)·내포식·`lambda`·`pathlib.Path`·`raise`·try `else`/`finally`·상속·`threading`·`global`·숫자 밑줄·`repr()`. Ch 5 기본 경로에서 쓴 것: `set()`·`try/except ValueError`(06), `isdigit()`·`not in`(07), 튜플 반환·딕셔너리 값에 목록(08), 타입힌트 없는 함수

## 6. A·B 트랙 제약 (Ch 2에서 넘어온 것, 그대로 유지)

- A 트랙(기본 경로)은 Ch 2 09~11절(데코레이터 `@`·컨텍스트 매니저 원리, Pydantic `BaseModel`, 패키징·픽스처)을 건너뜀. Ch 5는 이 문법을 한 번도 쓰지 않았음
- 규격 §2-2: Part 2 이후 절이 `@` 줄이나 `BaseModel`을 처음 쓰면 세 문장으로 풀고 Ch 2 09·10절을 링크. **Ch 06 03 구조화 출력이 `BaseModel`을 쓰면 이 규칙 대상**. `*args`·`**kwargs`·`*목록` 풀어 넘기기, `**inputs`도 A 트랙 미교육
- try `finally`는 B 트랙에서만 배움

## 7. 기준 버전·모델 revision (교재 출력 2026-09-16, Linux aarch64, Python 3.12.13, CPU)

- 실습 폴더 `labs/part1/ch05-llm-principles/uv.lock`: torch **2.8.0**(+cpu), transformers **4.56.2**, sentence-transformers **5.1.1**, tokenizers **0.22.2**, numpy **2.3.3**. 준비물마다 기준 버전과 「다른 버전, GPU, Windows·macOS는 실행하지 않았습니다」를 적음
- 모델: `openai-community/gpt2`@`607a30d783dfa663caf39e06633721c8d4cfcd7e`(토큰화기), `klue/bert-base`@`77c8b3d707df785034b4e50f2da5d37be5f0f546`(토큰화기), `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`@`e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, `Qwen/Qwen2.5-0.5B-Instruct`@`7ae557604adf67be50417f59c2c2f167def9a775`(Apache-2.0, 494,032,768 파라미터, 모델 카드 Context 32,768·생성 8,192), `HuggingFaceTB/SmolLM2-135M-Instruct`@`12fd25f77366fa6b3b4b768ec3050bf629380bac`(Apache-2.0), EXAONE-3.5-2.4B-Instruct@`ccce25b…`(카드·LICENSE만, `license: other`·`exaone`, 연구 목적만)
- 노트북 `outputs_sha256`(마감 기준): 01 `060a9d48…`, 02 `f43ffa90…`(재실행마다 stdout 조각 수로 해시가 바뀔 수 있음, 글자는 같음), 03 `fb798b7e…`, 04 `974b9fe0…`, 05 `642f2147…`, 06 `df95f660…`, 07 `f6b8bcc8…`, 08 `6d188945…`(시간 값이 있어 재실행마다 다름), 09 `981329b4…`

## 8. 실행 환경 (Cowork 기기 셸)

- 가상환경·uv 캐시·모델을 사용자 디스크 `$ROOT/.cache/vm/`(`venv-ch05-llm-principles` 926M, `uv` 979M, `hf` 1.7G)에 둠. `run_section.sh`가 자동으로 씀. 직접 실행할 때는 `UV_CACHE_DIR=$ROOT/.cache/vm/uv UV_PROJECT_ENVIRONMENT=$ROOT/.cache/vm/venv-ch05-llm-principles HF_HOME=$ROOT/.cache/vm/hf`(`HF_HUB_OFFLINE=1`이면 새로 받지 않음). `/tmp`에 torch 설치 없음. 기기 루트 여유 약 660MB
- 메모리 3.8GB: Qwen float32 적재 순간 약 3.25GB, 적재 뒤 약 2.3GB, 1,200조각 입력 생성 중 약 3.2GB, **약 3,500조각 입력은 강제 종료(137)**, 두 모델 한 커널 약 3.4GB(Qwen을 먼저 올릴 것). 모델은 한 번에 하나가 원칙
- 기기 셸 180초 제한: 절 `run_section.sh`는 16초(09)~81초(05). 긴 작업은 `timeout 165`
- **생성기 `author_NN.py`를 다시 실행하면 노트북 출력이 지워지므로**, 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … NN --no-exec`. 코드가 바뀌면 생성기를 고치고 새 커널 실행(노트북 손수정 금지). 시간 출력이 있는 08을 다시 실행하면 본문·결과 읽기·그림 08-3의 초 값을 새 출력에 맞춤
- `visual.cjs`는 공용 도구를 고치지 않고 `/tmp/ch05-close/vis/vis.cjs`(playwright 경로 사본) + `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`, HTML을 사본 폴더에 복사해 실행
- Ch 06은 API 호출 챕터라 torch가 필요 없음. `.cache/vm`은 전체 마감 때 삭제 승인을 받아 지움

## 9. 그림 색 판단 선례

- 넣은 문장·문서·교재에서 정한 값·설정·후보 **초록**, 출력으로 확인한 수·답·판정 **노랑**, 실행한 모델 **보라**(실행하지 않은 모델은 회색 점선, 01), 노트북에서 정의한 함수·판정 규칙·필수 조건·선택 기준 **파랑**, `generate()` 안에서 계산되어 출력하지 않는 값·코드 판정이 보지 못한 것·무관한 문장 묶음·실행하지 않은 다음 할 일 **회색**, 빨강 0장(끊긴 답·틀린 답·받은 `ValueError`도 출력으로 확인한 결과라 노랑)
- **xychart 계열 색 `#f59e0b`는 「주황」, `#22c55e`는 「초록」으로 부름**(검토 C-2, 규격 §5-3에 추가). flowchart measure 상자(연노랑 채움)만 「노랑」. 범례가 없어 막대·선 모양으로 구분한다고 도식 읽기에 적음. `plotColorPalette`는 작은따옴표(큰따옴표면 G7이 색 코드 숫자를 라벨 숫자로 셈). 값이 0~3 같은 작은 정수면 세로축이 소수 눈금이 되어 flowchart로 바꿈(05-4·06-2)
- 긴 라벨은 `<br>`로 직접 줄바꿈(08-4 「어림 1.84GB」가 자동 줄바꿈되어 라벨 순서를 바꿈). TB 네 갈래가 860px를 넘으면 LR(07-3), LR 두 갈래 + 긴 라벨은 TB(08-4). `{{mermaid:…|alt|캡션}}`의 alt·캡션에 `|`가 든 글(`<|im_end|>`) 금지
- 삽화는 같은 나무 쟁반·블록을 이어 쓰되, 블록의 뜻이 바뀌면(토큰 → 문장 → 후보 조각) 그림 읽기에 적음

## 10. 강사 확인 대상

- **03절 강의·실습 범위**(검토 03-2): 강의 2~5번(교재 예 점수·비중·새 벡터)과 7·9번 결과, 6·8·10번은 함께 실행·결과 읽기는 실습 시간. 03은 코드 셀 19(심화 2 포함)·검사 문장 420으로 챕터에서 가장 큼. meta 「강의 1h · 실습 0.5h」 유지
- **03절 심화 셀 추가**(검토 03-1 반영): `outputs.logits`를 기본 경로가 아닌 「원리 더 알아보기」에서 한 자리만 보여 준 수준
- **챕터 시수**: `chapter.json` 16h(강의 10·실습 6) 유지, 09 실습 절 30분은 실습 6h 안(Ch 1·3·4·22 선례, 규격 §7-2에 추가)
- 05절 컨텍스트 로트 정의를 입력 길이 기준으로 바꾸고 노트북 결과를 「자리 차이」로 부른 것
- 08절 기준 값을 「흐름을 보여 주려고 정한 예, 탐색 실행 뒤 적음」으로 밝힌 문장
- 01 `warnings.filterwarnings` 한 줄·UTF-8 설명 수준(Q1), 02 부정문 한 문장 결론(Q2), 04 `generate()`를 04절에 넣은 판단(Q4), 05 주 실행 입력 모양(Q5), 06 셈 세 가지·시드 한계 문장(Q6), 07 보류 결론(Q7), 09 결론·구성(Q9)
- 기준 버전 표기(torch·transformers·sentence-transformers, 모델 판 번호)
- 규격에 더한 규칙 다섯 줄(§3 탐색 뒤 정한 값 밝히기, §4 챕터 용어 다른 뜻으로 다시 쓰지 않기, §5-3 xychart 색 이름, §7-2 실습 절 시수, §8 옛 생성기 막기·옮기기)

## 11. 남은 것

- 다운로드 묶음 `textbook/downloads/part1-practice.zip`과 Part 1 목차(`textbook/part1/_build_index.py`·`index.html`)는 **2026-09-21 §2-7 리팩터에서 절 수를 `chapter.json`에 맞춰(Ch1 6·Ch2 13·Ch3 6·Ch4 6·Ch5 9 = 40절) 다시 만듦**(66파일, `llm_tools.py` 포함). `textbook/part1/qa/check_delivery.py`는 81행 실습 절 시수 meta·svg/excalidraw 수·35 노트북 검사가 개선 전 모양이라 멈춤 → 전체 마감 때 검사 스크립트를 고침
- 옛 생성기: `make_sources.py`(챕터 루트)·`labs/part1/ch05-llm-principles/make_notebooks.py`는 실행 막음 줄을 넣고 `qa/upgrade/before/generators/`로 옮김(삭제 아님). `textbook/qa/continuity-evidence/before-manifest.json`에 옛 경로가 남아 있지만 검사 스크립트는 `runs/` 항목만 대조해 영향 없음
- 뒤 챕터 옛 생성기(Ch 6·7·8·11의 `_make_notebooks.py`, Ch 3 `labs/…/_make_notebooks.py`)도 같은 처리가 필요(PLAYBOOK §2 1번)
- 정리 대상(삭제하지 않고 목록만): `figures/01-concept.*`~`05-concept.*`·`06-temperature-sampling.*`·`07-hallucination-conditions.*`·`08-model-selection.*`(옛 Excalidraw·SVG)·`figures/_gen_figures.py`, `qa/upgrade/before/08-to-09/`(빈 폴더)·`before/review-round1-pack/`(반영 전 review-pack), `qa/upgrade/gates-wip-*.json`·`gates-before-08.json`, `.cache/vm/hf`의 SmolLM2(276MiB)와 `.cache/vm` 전체(전체 마감 때 승인 뒤), 기기 `/tmp/ch05-01`~`/tmp/ch05-09`·`/tmp/ch05-01-req-*.txt`·`/tmp/ch05-sync.log`·`/tmp/ch05-reviewA`·`/tmp/ch05-reviewB`·`/tmp/ch05-close`(마감 세션 탐색·visual 사본, Kalai PDF·Chroma HTML 사본 포함)
- `집필점검표.md` 위 체크 목록은 개선 전(2026-09-09) 기록이라 아래 품질 개선 표와 마감 기록을 덧붙임
- 2차 검토(두 보고서 끝 「반영 결과」의 볼 곳), 강사 확인

## 12. §2-7 리팩터 (2026-09-21) — 도구 파일 + NumPy

- 규격 §2-7 첫 적용. 세부(도구 파일 표·NumPy 소개 문장·절별 수치·다시 실행 대조·뒤 챕터가 따를 모양)는 `qa/upgrade/handoff.md` 「§2-7 리팩터」, 리팩터 직전 스냅숏은 `qa/upgrade/before-2-7/`.
- **도구 파일** `labs/part1/ch05-llm-principles/notebooks/llm_tools.py`(코드 37줄): `softmax`(03) · `ask_model(model, tokenizer, input_text, output_budget)`(05, 인자로 바뀜) · `make_input(tokenizer, system_text, user_text)`(07, 인자로 바뀜) · `find_numbers`·`find_new_numbers`(07) · `print_report`(Ch 2 13·Ch 4 06). 06~09가 준비 셀 한 줄로 가져옴. 첫 가르침 판(03·05·07)은 노트북에 남김. `make_document`(04 ↔ 05)는 본문이 달라 합치지 않음.
- **NumPy**: 02절 8절 「같은 계산을 NumPy로」가 처음 소개(`import numpy as np`·`np.array`·`@`·`np.linalg.norm`, 반복문 판과 `0.8987` 같음, 반올림 전 끝자리는 다름). 03절이 표 `@` 벡터·비중 `@` 표·`np.exp`·`sum()`·`np.round`·`tolist()`·`mean(axis=0)`·`np.argmax`를, 06절이 `np.round`·`tolist()`를 씀. **「numpy를 쓰지 않음」은 §2-7 전 상태**이고, 이제 Ch 5 기본 경로는 NumPy를 씀.
- **수치**: 코드 셀 132 → 119, 코드 줄 1033 → 911(−11.8%, 도구 파일 포함 948). 늘어난 절은 02(+11, NumPy 소개 셀 둘)뿐.
- **다시 실행**: 02·03·06·07·08·09 새 커널 두 번. 모델 답·유사도·비중·판정은 리팩터 전과 글자까지 같고, 03 배열 출력 모양 4줄과 08 시간 값만 바뀜(08은 마지막 실행 값 `1.6`·`0.9`·`12.4`·`7.7`·`19.3`·`4.7`초). `outputs_sha256`: 02 `93246c92`, 03 `f11fa361`, 06 `61128590`, 07 `f2919e10`, 08 `00de77da`, 09 `c4892442`.
- **실행 환경**: `run_section.sh`가 노트북 폴더를 `PYTHONPATH`에 더함(`execute.py`는 저장소 루트에서 커널을 띄움). 학생 커널은 노트북 폴더에서 시작해 필요 없음(묶음을 풀어 09 실행으로 확인).
- **묶음**: `textbook/part1/public-files.json`(새)과 `build_bundle.py`의 Part 1·2 목록 읽기로 `llm_tools.py`가 `part1-practice.zip`에 들어감. `_build_index.py` 절 수를 `chapter.json`에 맞춰(40절) 묶음·Part 1 목차를 다시 만듦. `check_delivery.py`는 81행(실습 절 시수 meta)에서 멈춤 — §11 전체 마감 몫.
- **뒤 챕터가 이어받을 NumPy 이름**(다시 풀지 않고 「Ch 5 02절처럼」으로 가리킴): `np.array`·`@`(점곱, 표 @ 벡터, 비중 @ 표)·`np.linalg.norm`·`np.exp`·`sum()`·`np.round`·`tolist()`·`mean(axis=0)`·`np.argmax`. **아직 안 가르친 NumPy**: `np.argsort`·`axis=1`·`keepdims`·`.T`·2차원 표끼리 `@`·`np.dot`·불리언 거르기(기본 경로)·`np.mean` 함수형.
