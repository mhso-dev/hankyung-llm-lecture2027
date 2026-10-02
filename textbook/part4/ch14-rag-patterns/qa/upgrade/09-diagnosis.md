# Ch 14 09절 「패턴 비교와 선택」 품질 개선 기록

- 작업일 2026-09-19 · 규격 `textbook/QUALITY-UPGRADE.md` · 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`
- 대상 `_src/09-패턴-비교와-선택.html` · `labs/part4/ch14-rag-patterns/notebooks/09-패턴-비교와-선택.ipynb`
- 형식 `experiment` 유지 · 수정 전 원본은 `qa/upgrade/before/`
- 생성기 `qa/upgrade/author_09.py`(본문 HTML + 노트북을 함께 씀, `--src-only`를 주면 본문만). 설계 결정과 탐색 실행 값은 그 파일 머리말에 모두 적혀 있습니다.
- **이 절은 이 챕터에서 유일하게 파일을 쓰는 절입니다**(`labs/part4/ch14-rag-patterns/runs/pattern-comparison.json`).

## 1. 게이트 전후

| 게이트 | 개선 전 | 개선 뒤 |
|---|---|---|
| G1 문법 사다리 | 22 | **0** |
| G2 셀 모양 | 21 | **0** |
| G3 주석 | 1 | **0** |
| G4 실제 모델 | 0 | **0** |
| G5 노트북 설명 | 9 | **0** |
| G6 문장 | 28 | **0** |
| G7 그림 | 3 | **0** |
| 합계 | **84** | **0 (PASS)** |

- 기록 파일: `qa/upgrade/gates-before.json`(챕터 아홉 절 합계 501) · `qa/upgrade/gates-wip-09.json`.
- 코드 셀 **9개 → 29개**(준비 셀 12개 포함) · 검사 문장 **117개 → 339개**.
- `verify.py --chapter` → `PASS 9 sections / 259 code cells (max 23 lines)`. 빌드한 HTML 열 개 모두 `{{` 잔존 **0건**이고 `_build.py`를 두 번 돌려 열 개의 sha256이 모두 같았습니다.
- 새 커널 실행 기록: `code_sha256 6393e086…` · Python 3.12.13 · 코드 셀 29개.

## 2. 수정 전 주요 문제

개선 전 코드 셀 아홉 개를 모두 읽고 미교육·금지 문법을 목록으로 만들었습니다.

- **`numpy`**: `%pip`의 `numpy==2.5.3`, `np.array`, `vectors@q`, `np.linalg.norm(vectors,axis=1)`, `np.argsort(scores)[::-1]`.
- **내포식과 제너레이터 식 아홉**: 문서 글 모으기, `search`의 결과 만들기, 변형 질문 줄 고르기, `show_hits`, 근거 글 잇기, 패턴별 합계 넷(`sum(... for r in part)`).
- **`next(p for p in ...)`** 두 곳: 프로젝트 맨 위 찾기와 정답 자리 찾기.
- **`sorted(rrf, key=rrf.get, reverse=True)`**: `key=`·`reverse=`와 딕셔너리 정렬을 한 줄에 섞었습니다.
- **`f-string`** 셋(`f"검색 질문 2개를 줄마다 쓰세요:{item['question']}"` 꼴)과 **기본값 매개변수** `def search(question, k=3)`, **복합 타입힌트** `list[dict[str, float | int]]`·`list[tuple[dict[str, Any], float]]`, `from typing import Any`.
- **한 줄 다중 대입**(`text,_,_=ask(...)`) 셋과 **한 글자 이름 일곱**(`q`·`d`·`x`·`r`)과 **`import os, time`**.
- **`time.perf_counter()`와 `usd` 단가 추정**: 토큰 수·걸린 시간·달러를 셀 하나에서 함께 계산했습니다(Ch 12부터 걸린 시간을 재지 않기로 한 약속과 어긋남).
- **모델 이름이 `gpt-4.1-mini`**였고 b10에 그 모델의 단가 줄이 있었습니다.
- **`hashlib`**은 개선 전에도 썼고 이 챕터에서는 이 절만 씁니다. Ch 7 08절에서 연 이름이라 빼지 않고 **처음 쓰는 자리에 한 문장을 붙였습니다**(노트북 1절 결과 읽기).
- **용어**: 「임계값」·「분기」·「Recall@3」·「지연 시간」·「벽시계 시간」이 섞여 있었습니다.
- **그림 0장**(Mermaid·삽화·설계표 모두 없음)이고 옛 토큰 `{{svg:09-패턴-비교와-선택-flow}}` 한 장만 있었습니다. 노트북에 제목 셀과 「오늘 볼 그림」이 없었습니다.
- **비교 조건이 어긋나 있었습니다**: 패턴마다 최종 답 생성까지 넣고 그 토큰·시간·비용을 같은 줄에 담아, 「검색에 넣을 글」 말고도 달라지는 것이 여럿이었습니다.

## 3. 바꾼 것

### 설계 결정 (`author_09.py` 머리말 1~9번 그대로 이어받음)

1. **견줄 패턴을 기준선·변형 질문(02절)·가상 문서(05절) 셋으로 골랐습니다.** 셋 다 「검색에 넣을 글」 하나만 다르고 검색 뒤 처리와 답 만들기가 없어 같은 조건으로 견줄 수 있습니다(handoff §08→§09 2번).
   - **뺀 다섯과 까닭**: 03절 하위 질문과 04절 넓힌 질문은 질문의 성질(사실 둘 섞임·한 사례의 세부)이 달라 같은 질문 벌로 견주면 그 패턴에 불리합니다. 06절 보정 검색과 07절 근거 검사는 검색 뒤와 답 뒤를 손봐 견주는 값이 「정답 문서의 자리」가 아니게 됩니다. 08절 한 단계 요약은 질문을 받기 전에 요약 셋을 만들어 두어 요청이 질문 수와 따로 듭니다. 이 다섯은 b7에 「이번에 견주지 않았습니다」로 밝혔습니다.
2. **질문 셋을 자료의 `C02`·`C05`·`C06`으로 골랐습니다.** 갈래가 `library`·`facility`·`account`로 겹치지 않고 정답 문서 ID가 자료에 적혀 있습니다. 탐색 실행에서 자료의 여덟 질문 가운데 여섯은 기준선만으로도 정답 문서가 첫 자리였고, 그 사실을 b7에 적었습니다.
3. **패턴마다 다른 것은 검색에 넣을 글 하나뿐입니다.** 문서 12건·임베딩 모델과 256·답 모델 `gpt-5.4-mini`·`top_all` 12·`top_three` 3·질문 벌과 정답 문서를 고정했습니다. **앞 절 숫자를 표로 옮기지 않고 이 절에서 다시 쟀습니다.**
4. **견주는 값을 「정답 문서의 자리」와 「서비스 요청 수」 둘로 잡았습니다.** 자리는 `top_all` 12에서 세어 1~12 눈금이라 정답 포함률(0·0.333·0.667·1)보다 촘촘합니다. 요청 수는 코드가 세는 값이라 추정이 아닙니다.
5. **값 바꿔 보기는 자리를 셀 때 재는 문서 수를 열둘에서 셋으로 바꿉니다.** 서비스 요청이 늘지 않고 같은 기록 아홉 줄을 다시 셉니다.
6. **걸린 시간·토큰·달러 추정을 모두 뺐습니다.** b10의 옛 모델 단가 줄도 뺐습니다.
7. **변형 질문 수를 02절 셋에서 둘로 줄였습니다.** 질문 셋을 돌리면 요청이 곱으로 늘기 때문이고 그 사실을 b7에 적었습니다.
8. **모델 답에 `assert`를 걸지 않았습니다.** `assert`는 키 확인·요청 수·파일 줄 수와 칸 이름 넷뿐입니다.
9. **쓰지 않은 것**: `numpy`·`re`·`time`·`lambda`·내포식·제너레이터 식·조건 표현식·f-string·`key=`·`reverse=`·`set`·`setdefault`·기본값 매개변수·복합 타입힌트·세미콜론·한 줄 다중 대입·한 줄 복합문·클래스 정의·`enumerate`·`zip`·`next`·`join`·`max`·`min`·`float`. 부른 내장 이름은 `len`·`open`·`print`·`range`·`round`·`sorted`·`str`뿐입니다.

### 이어 쓴 함수와 새로 만든 함수

- Ch 12·Ch 11에서 이어 쓴 일곱: `dot_product`·`vector_length`·`cosine_similarity`·`cosine_distance`(Ch 12 01절), `rank_by_distance`(Ch 12 05절), `unique_doc_ids`·`find_gold_rank`(Ch 11 01절). `author_08.py`에서 글자 그대로 옮겼습니다. **`print_ranked`는 가져오지 않았습니다**(이 절은 순위 표를 보이지 않고 자리만 셉니다).
- Ch 12 06절 순위 합치기 둘 `fuse_scores`·`fuse_rank`와 순위 상수 `60`·가중치 `1.0`은 `author_03.py`에서 그대로 가져왔습니다. 04~08절은 쓰지 않았고 이 절이 다시 씁니다.
- 02절 `split_lines`·`search_ids`·`build_variant_prompt`와 05절 `join_lines`·`build_hyde_prompt`도 각 절 생성기에서 글자 그대로 옮겼습니다. **머리글 둘을 글자 그대로 써야 앞 절과 같은 조건이 됩니다.**
- 가져오지 않은 것: 01·07절 답 만들기 부품 넷(`text_by_doc`·`keeps_word`·`answer_head`·`build_answer_prompt`), 06절 `search_hits`·`needs_retry`·`correct_once`, 07절 점수 함수 다섯, 08절 갈래 함수 넷. 이 절은 답을 만들지 않고 기준값도 쓰지 않습니다.
- 새로 만든 넷: `run_baseline(question_text)` · `build_search_texts(question_text)` · `run_multi(question_text)` · `run_hyde(question_text)`. 넷 모두 「질문 글 하나 → 문서 ID 목록과 서비스 요청 수」라는 같은 모양을 냅니다.
- 기록 함수 `run_row`는 **08절 판(`run_name, chosen_name, seen_ids, place`)을 본으로 삼아 칸을 다시 짰습니다**: `run_row(pattern_name, item, result)`가 산출 파일 칸 일곱(`pattern`·`qid`·`question`·`gold_doc_id`·`found_ids`·`rank`·`service_calls`)을 만듭니다. **이 절만 칸 이름이 영어입니다** — 기록 한 줄이 산출 파일 줄이고, Ch 12 `runs/*.json`이 영어 칸 이름을 쓰기 때문입니다.

### 노트북 (코드 셀 9 → 29)

- 준비 셀 열둘(설치 · import · 키 · 값 다섯 · 문서 글 · 거리 함수 넷 · 순위와 검색 둘 · 자리 세기 둘 · 합친 점수 · 합친 순위 · 줄 다루기 둘 · 머리글 둘)에 `lesson_role="setup"`을 주었고 묶음 셀에는 `upgrade_allow=["multiple_defs_in_cell"]`을 함께 주었습니다.
- 준비 셀 묶음 넷만 15·14·15·14줄이고 **비준비 셀 열일곱은 모두 10줄 이하**입니다. 함수 본문은 가장 긴 `run_multi`가 8줄입니다.
- 정의 셀 다섯(`run_baseline`·`build_search_texts`·`run_multi`·`run_hyde`·`run_row`)의 결과 읽기에 「정의 셀이라 출력이 없습니다」를 적었습니다.
- 차례: 준비 → 키·모델 → 자료 읽기 → 값 정하기 → 앞 절 부품 여덟 → 문서 임베딩 → 질문 셋 고르기 → 패턴 함수 넷 → 기록 한 줄 → 아홉 실행 → 견주기 표 → 값 바꿔 보기 → 지문·파일 쓰기·다시 읽기.

### 본문 (`_src/09-패턴-비교와-선택.html`)

- b4에 용어 표 둘을 두었습니다. 새 말은 **「견주기 표」 하나**뿐이고 나머지 넷(변형 질문·가상 문서·순위 합치기·정답 자리)은 앞 절 뜻을 이어 씁니다. meta의 「새 용어 4 → 1」.
- b4 소제목 「어느 자리를 손보는 패턴인가」로 01~08절이 손본 자리 넷을 한자리에 모았습니다(handoff §08→§09 1번).
- b6은 질문 셋 고르기 → 기준선 → 변형 질문 → 가상 문서 → 갈린 칸 차례로 읽고, 마지막 두 단락에서 「눈금이 성기다」와 「넓혀 읽지 않는다」를 적었습니다.
- b7은 열여덟 줄이고 그 가운데 아홉 줄이 견줄 패턴을 고른 까닭·뺀 패턴·탐색 실행·갈린 값·`assert` 범위·재지 않은 값을 적은 정직성 메모입니다.
- b8의 「다음 학습과 이어지는 지점」은 **실습 절**을 가리킵니다. 실습 절이 아직 없으므로 규격 §7-2가 정한 것만(챕터 마지막에 붙는다·앞 절 이름과 함수만 쓴다·새 문법과 새 서비스는 쓰지 않는다) 적었고 Ch 15로 넘기지 않았습니다.

### 그림 (0장 → Mermaid 4장 + 삽화 1장)

- 설계표 `qa/upgrade/09-figures.md`. 원본 viewBox 폭 419·824·241·320으로 모두 868 아래이고 네 장 모두 처음 렌더에서 통과했습니다.
- 이 절은 기준값도 조건 갈래도 없어 **점선 화살표가 없습니다**(06·07·08절과 다른 점). 빨강도 0장입니다.
- `09-4`는 handoff §08→§09 10번의 권고대로 칸 셋을 `flowchart LR`이 아니라 **`flowchart TB`로 세로로 쌓았습니다**(폭 320).
- 삽화 `09-5`는 나무판 계열을 이어 「같은 구멍 하나에 마개 셋을 차례로 대 보기」로 그렸습니다. 1차 채택(재생성 0회)이고 채택 job 결과와 픽셀 대조에서 **다른 픽셀 0개**입니다. 판이 비스듬히 위에서 본 각도로 그려져 alt와 「그림 읽기」를 그린 대로 고쳤습니다.
- 다섯 장 모두 PNG를 직접 열어 보고 「도식 읽기」·「그림 읽기」와 맞는지 확인했습니다(설계표 「칸 순서 확인」).

## 4. 새 커널 실행과 갈린 값 (규격 §3)

- **최종 코드로 새 커널을 네 번 돌렸습니다**(`code_sha256 6393e086…`가 네 번 모두 같음). 코드는 한 번도 바뀌지 않았고 마크다운만 두 차례 고쳤습니다.
- **셀 29개 가운데 갈린 것은 견주기 표 셀과 값 바꿔 보기 셀 둘뿐**입니다. 1·2차 실행에서는 27/29, 3·4차 실행에서는 27/29가 글자까지 같았습니다.
- **갈린 칸은 패턴을 얹은 여섯 칸 가운데 셋**입니다.
  - `변형 질문 | C02`의 자리: 6 · 5 · 5 · 4
  - `가상 문서 | C02`의 자리: 5 · 3 · 1 · 1
  - `가상 문서 | C05`의 자리: 1 · 2 · 1 · 1
- **네 번 모두 같았던 값**: 기준선 자리 셋(`C02` 7 · `C05` 1 · `C06` 1), `변형 질문 | C05`·`변형 질문 | C06`·`가상 문서 | C06`의 자리 1, 패턴별 서비스 요청 수(1 · 4 · 2), `실제로 센 서비스 요청 수: 21`, 질문 벌 세 줄, 파일 줄 수 9와 칸 이름 일곱.
- **처리**: 갈린 칸은 본문 결론·표 해설·그림 라벨·정리·복습에 넣지 않았습니다. 견주기 표 셀의 「결과 읽기」 첫 단락은 기준선 세 줄과 요청 수만 인용합니다. 그림 `09-4`는 갈린 칸을 「네 번 실행에서 갈린 칸 하나」·「네 번 실행에서 갈린 칸 둘」로만 적었습니다.
- **교재에 실린 출력은 네 번째 실행 결과입니다.** `runs/pattern-comparison.json`도 그 실행이 쓴 파일입니다. 실행마다 그 파일의 `rank` 칸 셋이 달라집니다(`found_ids`도 그 줄에서 함께 달라집니다).
- **마음에 드는 값을 고르려고 다시 돌린 적이 없습니다.** 네 번 돌린 까닭은 (1) 1·2차로 갈리는 칸을 찾고, (2) 그 칸을 인용하던 마크다운을 고친 뒤 3·4차로 다시 대조하기 위해서입니다. 코드가 같으므로 네 실행 모두 같은 자격의 실행입니다.
- **탐색 실행**(`/tmp/ch14-09/probe1.py`·`probe2.py`): 임베딩 30번·답 모델 12번. probe1은 자료의 여덟 질문을 기준선으로 한 번씩 재었고(`C01` 자리 2 · `C02` 자리 7 · 나머지 여섯은 자리 1), probe2는 고른 질문 셋을 세 패턴으로 두 번씩 돌렸습니다. 이 사실을 b7에 적었습니다.

## 5. 산출 파일 `runs/pattern-comparison.json`

- **다시 쓰기로 한 까닭**: 이 파일은 `qa/public-files.json`과 `textbook/part4/public-files.json`에 **학생 묶음 파일로 올라 있습니다.** 다시 쓰지 않으면 학생이 받는 묶음에 개선 전 `gpt-4.1-mini` 기록이 그대로 남아 새 교재와 어긋납니다.
- **읽는 쪽 확인**: `grep -rln "pattern-comparison" --include="*.py" --include="*.json" --include="*.ipynb" --include="*.cjs" --include="*.sh" textbook labs qa`로 훑었습니다. 나온 파일은 일곱이고 **코드로 이 파일을 읽는 곳은 하나도 없습니다**: 묶음 목록 둘(`qa/public-files.json` 18행·`textbook/part4/public-files.json` 27행), `qa/upgrade/before-manifest.json`, 이 절 생성기와 노트북, `qa/upgrade/before/`의 개선 전 사본, 실행이 막힌 옛 생성기 `labs/…/_make_notebooks.py`뿐입니다. 그래서 칸 구성을 바꿔도 깨지는 검사가 없습니다.
- **칸 구성**(handoff §08→§09 4번 권고 그대로):
  - 머리 다섯 `chat_model`(`gpt-5.4-mini`) · `embedding_model`(`text-embedding-3-small`) · `embedding_dimensions`(256) · `document_hash` · `query_hash`.
  - `rows` 아홉 줄, 줄 칸 일곱 `pattern` · `qid` · `question` · `gold_doc_id` · `found_ids` · `rank` · `service_calls`.
  - **뺀 칸**: `source_provenance` · `answer` · `retrieved_ids`(→ `found_ids`) · `gold`(→ `gold_doc_id`) · `input_tokens` · `cached_tokens` · `output_tokens` · `usd` · `ms`.
- **`hashlib`**: 문서·질문 지문을 만드는 데 필요해 남겼습니다. Ch 7 08절에서 연 이름이고 이 챕터에서는 이 절이 처음 씁니다. 노트북 1절 결과 읽기에 「파일 내용이 같은지 견줄 지문을 만듭니다」 한 문장을 붙였고 지문 값은 길어서 출력하지 않고 글자 수만 출력합니다(출력 읽기 관례: 해시는 인용하지 않음).
- **파일을 쓰면 해야 하는 일 넷**(handoff §08→§09 5번): (1) 준비물에 「새로 쓰는 파일은 `runs/pattern-comparison.json` 하나」를 적었습니다. (2) 쓴 뒤 다시 읽어 줄 수와 칸 이름을 출력하고 그 둘만 `assert` 합니다. (3) 묶음 목록 둘에 이미 이 경로가 있어 **고칠 것이 없었습니다**(`qa/public-files.json` 18행·`textbook/part4/public-files.json` 27행). (4) 보호 파일 해시 변화는 아래 §6에 적었습니다.
- 파일 크기 4540바이트 → **4454바이트**.

## 6. 보호 파일 20개

- **스무 개 가운데 `labs/part4/ch14-rag-patterns/runs/pattern-comparison.json` 하나만 의도적으로 달라졌고 나머지 열아홉은 그대로입니다.**
  - 개선 전 sha256 `8b1fd13cd844fcf9d62d5abaa616932b015ed3d3d8b6dc40a73bb7ffd3e8a091`
  - 개선 뒤 sha256 `94d10997803eabdc37111b484bc832ccaf6d2e07b6ebd4c9855b0311de897f50`
- `data/documents.json`·`data/queries.json`과 Ch 12·Ch 13의 `runs/`·`data/` 열일곱 개는 모두 `before-manifest.json`의 값과 같습니다.
- **`before-manifest.json`은 고치지 않았습니다.** 수정 전 기록이므로 그대로 두고 이 문서에 변화를 적습니다. 챕터 마감에서 다시 계산하면 이 한 줄이 어긋난 것으로 나오는 것이 정상입니다.
- 이 파일은 실행마다 `rank`·`found_ids` 칸이 달라지므로 **다시 실행하면 해시가 또 바뀝니다**. 지금 값은 네 번째 실행이 쓴 것입니다.

## 7. 실행 환경 메모

- 가상환경 `$ROOT/.cache/vm/venv-ch14-rag-patterns`(Python 3.12.13)를 그대로 썼고 패키지를 새로 넣지 않았습니다.
- 서비스 요청: 노트북 한 번 실행에 **스물두 번**(임베딩 16 = 문서 1 + 실행 아홉에서 15, 답 모델 6 = 변형 질문 3 + 가상 문서 3). 실행 하나에 드는 요청은 기준선 1 · 변형 질문 4 · 가상 문서 2입니다.
- 이번 작업에서 새 커널 실행을 네 번 했으므로 임베딩 64번·답 모델 24번이고, 탐색 실행 임베딩 30번·답 모델 12번을 더하면 합 **130번**입니다. 예상 비용은 미화 **0.05달러 아래**입니다.
- 삽화 1장 = 2크레딧, 잔액 2669 → **2667**.
- Mermaid 렌더는 `PUPPETEER_CACHE_DIR=/tmp/pptr-cache`와 `LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/aarch64-linux-gnu`를 주고 돌렸습니다.

## 8. 산출 파일과 챕터 밖 파일

- 새로 쓴 파일: `figures/09-1`~`09-4`의 `.mmd`·`.svg`·`.png`·`.render.json`·`.caption.md`, `figures/09-5-같은-구멍에-마개-셋을-차례로-대-보기.png`·`.caption.md`·`.prompt.md`, `qa/upgrade/author_09.py`, `qa/upgrade/09-figures.md`, `qa/upgrade/09-diagnosis.md`, `qa/upgrade/gates-wip-09.json`, `qa/upgrade/review-pack/09-패턴-비교와-선택.md`.
- 다시 쓴 파일: `_src/09-패턴-비교와-선택.html`, `labs/…/notebooks/09-패턴-비교와-선택.ipynb`, **`labs/…/runs/pattern-comparison.json`**, 챕터 HTML 열 개, `qa/upgrade/handoff.md`, `집필점검표.md`, `qa/verification.md`.
- **챕터 밖 파일 하나가 도구에 의해 자동으로 다시 쓰였습니다**: `textbook/_notebook/checks/notebook-contracts-part4-ch14-rag-patterns.json`. `verify.py --chapter`가 남기는 파일이고 01~08절 작업에서도 같은 자리가 갱신되었습니다. 손으로 고친 것이 아닙니다.
- **그 밖의 챕터 밖 파일은 고치지 않았습니다.** 묶음 목록 둘(`textbook/part4/public-files.json` 포함)은 이미 이 파일 경로를 담고 있어 고칠 것이 없었습니다.

## 9. 검토에서 볼 곳

- b6 셋째·넷째·다섯째 단락과 b7의 「갈린 칸」 줄이 네 번 실행에서 본 것과 맞는지.
- 견줄 패턴을 셋으로 좁힌 까닭과 뺀 다섯의 까닭(b7 첫 세 줄)이 납득되는지.
- 산출 파일의 칸 일곱과 머리 다섯이 이 챕터가 실제로 재는 값만 담고 있는지.
- b8이 실습 절을 가리키되 아직 정해지지 않은 것을 적지 않았는지.
- 코드 셀이 29개이고 준비 셀이 열둘인 것(앞 절보다 준비 셀이 많음)이 괜찮은지 — **강사 확인 대상**.

## 10. 남은 것

- 실습 폴더 `README.md`는 아직 개선 전 판입니다(옛 모델 이름·비용 문장·「임계값」). 챕터 마감 때 고치기로 한 자리입니다.
- `pyproject.toml`의 `numpy==2.5.3`은 **이제 아홉 절 노트북 가운데 어느 것도 쓰지 않습니다**(09절이 마지막이었습니다). 뺄지는 챕터 마감에서 정합니다(`qa/upgrade/chapter-lead-notes.md`).
- 옛 생성기 셋(`_make_sources.py`·`figures/_gen_figures.py`·`labs/…/_make_notebooks.py`)은 실행이 막힌 채 그대로 있습니다. 챕터 마감 때 `qa/upgrade/before/generators/`로 옮기기로 되어 있습니다.
- 옛 그림 `figures/09-패턴-비교와-선택-flow.{svg,excalidraw,caption.md}`는 본문에서 더는 참조하지 않지만 **지우지 않았습니다**(챕터 리드 메모의 삭제 승인 대상).
- **지워야 한다고 판단했지만 지우지 않은 것은 위 옛 그림 셋뿐입니다.**

## §2-7 리팩터 (2026-09-21)

- 도구 파일에서 일곱 개(`build_variant_prompt(question, variant_count)`·`build_hyde_prompt(question, doc_sentences)`·`search_ids`·`fuse_rank(…, rank_constant)` 등)를 가져오고 준비 셀 일곱을 뺐습니다. 코드 셀 29 → 22, 코드 줄 258 → 168.
- **산출 파일 `runs/pattern-comparison.json` `94d10997803eabdc37111b484bc832ccaf6d2e07b6ebd4c9855b0311de897f50` → `49eabfd40d5363bc76b0a58d2394a5d2878917058630c3f26b80995db71db814`**(4454바이트, 머리 다섯 + `rows` 아홉 줄 × 칸 일곱 그대로, A 실행이 한 번 `7853c28e…`로 쓴 뒤 B가 다시 씀). `rank` `C02` 7·5·3 / `C05` 1·1·1 / `C06` 1·1·1. 코드로 읽는 곳 0건.
- 새 커널 두 번 20/22 같음(`가상 문서 | C02` 6 ↔ 3). 11절 결과 읽기·b7 한 항목에 이번 두 실행 값을 더했고 그림 `09-4`의 「네 번 실행」은 앞선 네 번이라 그대로 둠. 핵심 관찰(기준선 7·1·1, 요청 수 1·4·2, 패턴 칸이 갈려 어느 패턴이 낫다고 적지 않음) 유지, 10항 수정 없음. 서비스 요청 22 × 2.
