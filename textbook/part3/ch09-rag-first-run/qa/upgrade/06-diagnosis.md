# 06 실험 하네스 — 품질 개선 진단 (2026-09-17)

규격 `textbook/QUALITY-UPGRADE.md`, 절차 `textbook/_notebook/upgrade/PLAYBOOK.md`. 앞 절 인계는 `handoff.md` §05 → §06.

## 1. 게이트 전후

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 문법 사다리 | 6 | 0 |
| G2 셀 모양 | 4 | 0 |
| G3 주석 | 10 | 0 |
| G4 실제 모델 | 1 | 0 |
| G5 노트북 설명 | 13 | 0 |
| G6 문장 | 27 | 0 |
| G7 그림 | 2 | 0 |
| 합계 | **63** | **0** |

수정 전 값은 챕터 첫 절 작업에서 만든 `gates-before.json`의 06절 행입니다. 수정 후 값은 `gates-wip-06.json`입니다.
코드 셀 11개 → 32개, 노트북·본문 문장 133개 → 638개. 빌드 HTML SHA-256 `ccee14a489931a00aae539ed4596dfad956ed9efa932265e2181e77b38a67d0e`. `verify.py --chapter` → `PASS 6 sections / 148 code cells (max 16 lines)`.
`visual.cjs` 1280px·390px 2건 PASS(`/tmp/ch09-01/vis/vis.cjs` 사본에 `/tmp/ch09-06/html` 넘김). 빌드 HTML에 `{{` 잔존 0건.

## 2. 수정 전 주요 문제

- **G1·G2**: 제너레이터 식 3곳·내포식 3곳(`sorted(path for tier in ... for path in ...)`, `[{...} for rank, (hit, score) in enumerate(hits, start=1)]`), 15줄 넘는 셀 4개, `next(parent for parent in [Path.cwd(), *Path.cwd().parents] ...)`로 프로젝트 맨 위 찾기, `deepcopy`·딕셔너리 합치기 `|`·`**cfg["split"]` 풀어 넘기기.
- **G3**: 코드 셀 11개 가운데 10개에 첫 줄 주석이 없었습니다.
- **G4**: 모델 셀이 `init_chat_model(run_config["generation"]["model"])`만 불러 `temperature`·`reasoning_effort`가 없었습니다.
- **G5**: 제목 셀(「이 노트북에서 할 일」)과 「오늘 볼 그림」 첨부가 없었고, 결과 읽기 셀이 출력 값을 인용하지 않았습니다. 마지막 셀 뒤에는 결과 읽기가 아예 없었습니다.
- **G6**: 70자 넘는 문장 12개, 영문 용어·코드 이름에 조사를 바로 붙여 시작한 문장 13개(`YAML은`·`JSONL은`·`k는`·`Before와`·`` `json.dumps(...)`는 ``), 5문장 넘는 단락 2개.
- **G7**: Mermaid 0장(옛 Excalidraw SVG `06-하네스-루프.svg` 하나), 그림 설계표 없음. 삽화 `06-실험-노트.png`는 사람과 다이얼과 흩어진 메모를 그려 01~05절 삽화 계열(책상·카드·상자)과 이어지지 않았습니다.
- **사람 검토로 본 것**: 마지막 셀이 `jupyter nbconvert --execute` 명령 글만 출력하고 실행하지 않았습니다. Before가 `try/except AssertionError`로 실패를 만들었고, After는 `assert new_sha != config_sha`로 코드가 정한 값을 확인했습니다. 본문 b4에 「캐시」를 새 용어로 두었으나 노트북은 색인을 저장·다시 불러오지 않았습니다. 셀 15의 마지막 줄 `assert save`는 잘린 채 남아 있었습니다(실행은 통과, 이름 `save`가 없어 실제로는 `NameError` 없이 `saved`를 쓰지 않음 — 옛 노트북 출력에는 오류가 없어 이 줄이 실행되지 않았습니다).

## 3. 바꾼 것

- **설정을 파일에서 읽기**: 임시 폴더에 YAML을 써서 다시 읽던 것을 실습 폴더 `config.yaml` 읽기로 바꿨습니다(읽기만, 고치지 않음). 그 파일의 `split`이 01~05절과 같은 500·50이고 `retrieval.k`가 4라, 「값 하나만 바꾼다」를 파일 값과 실행 값의 차이로 보여 줄 수 있습니다. `TemporaryDirectory`·`Path`·`next(... for ...)`를 모두 뺐습니다.
- **경로 찾기**: 01~05절 후보 목록 + `for`·`break` 모양을 그대로 쓰되, 읽을 파일이 여럿이라 경로의 앞부분(`labs/`·`../../`·`../../../`)만 고르게 했습니다.
- **라벨은 평가셋에서 읽기**: `qid`·`question`·`gold_doc_ids`를 노트북 안 YAML에 적던 것을 `labs/part3/ch11-evaluation/data/evaluation-queries.jsonl` 첫 줄 읽기로 바꿨습니다. 실습 자료 `queries.jsonl`의 같은 질문도 읽어 `두 파일의 질문 글이 같은가: True`와 정답 쪽 `[2]`를 함께 보여 줍니다(05절 쪽 단위 정답 출처와 잇는 자리).
- **색인 이름표**: `hashlib.sha256(...)[:10]`을 함수 `make_index_key(index_settings)`로 묶고, 넣는 설정에 `corpus`를 더했습니다(실습 폴더 `harness.py` `index_key()`와 같은 생각). 계산 방법은 Ch 7 08절에서 배운 SHA-256을 그대로 쓰고, `harness.py`가 SHA-1이라 값이 다르다는 것을 b7에 적었습니다.
- **검색 항목 함수**: 내포식으로 만들던 `retrieved`를 `make_hit_item(hit, score, rank)` 함수와 반복문으로 바꿨습니다. 04·05절 `make_note()`·`build_notes_messages()`·`find_cited_notes()`는 같은 코드로 이어 씁니다.
- **기록 검사**: 파일에 쓰기 전에 필수 키·순위·답의 출처 표시를 확인하는 셀을 새로 넣었습니다(`record_keys` 목록 = 다음 챕터가 읽는 계약).
- **파일 쓰기**: `Path.write_text`·`with_suffix`를 `with open(...)`과 `os.replace()`로 바꿨습니다. 폴더는 `os.path.exists` 확인 뒤 `os.makedirs`(Ch 7 08절에서 배운 모양)로 만듭니다.
- **값 바꿔 보기**: 마지막 셀의 `nbconvert` 명령 글 출력을 없애고, 검색 개수만 4로 바꿔 이름표가 같은지와 검색 결과 4건을 보는 셀로 바꿨습니다.
- **Before/After**: `try/except AssertionError`로 만든 실패를 없앴습니다. Before는 문서 청크 크기만 1000으로 바꾼 실행 설정으로 500자 색인을 검색해 `이름표가 chunk_id에 들어 있는가: False`를 보이고, After는 1000자로 다시 나눠 새 색인을 만들어 `True`를 보입니다. 두 조건 모두 기록 파일을 쓰지 않습니다.
- **용어**: 「캐시」와 「설정 해시」를 쓰지 않고 「색인 이름표」로 정했습니다(`index.html` 새 용어 줄은 마감 대조 대상). 「청크」 단독 표기 0건, 「조각」 0건.
- **그림**: Mermaid 4장(06-1 하네스 한 바퀴, 06-2 기록 한 줄, 06-3 검색 개수만 바꾸기, 06-4 Before-After)과 삽화 1장(06-5)을 새로 만들었습니다. 옛 `06-하네스-루프.svg`·`06-실험-노트.png`는 지우지 않았습니다.
- **모델 셀**: `nbkit.key_and_model_cells()`로 바꿔 `temperature=0`·`reasoning_effort="none"`과 실행일 문장을 넣었습니다.

## 4. 데이터와 설정 결정(탐색 실행 뒤)

- **문서 범위**: 01~05절은 E01 한 건만 색인했습니다. 06절은 개선 전 06과 같은 디지털 PDF 18건(`corpus.tiers` = easy·medium·hard)을 색인합니다. 정답 문서 ID 대조가 문서 단위라, 문서가 한 건이면 대조가 언제나 맞아 뜻이 없기 때문입니다. `/tmp/ch09-06/probe1.py`(easy 6건)·`probe3.py`(18건)로 먼저 검색만 실행해, 두 경우 모두 1·2위가 E01 표지 45자와 2쪽 498자임을 확인하고 18건으로 정했습니다.
- **검색 개수 2**: Ch 11 06절 본문이 「Ch 9처럼 후보를 2개만 저장했다면 Recall@5·50과 Precision@5·nDCG@5는 측정하지 않는다」고 적고 있고, `textbook/part3/qa/finalize_continuity_evidence.py`가 ch09 실행의 `recall_at_5` 등이 `None`이고 `recall_at_logged_candidates`가 1임을 확인합니다. 그래서 개선 전과 같은 k=2를 유지했습니다(값 바꿔 보기의 k=4는 기록을 쓰지 않음).
- **Before/After 크기 1000**: 실습 폴더 `harness.py` 사용법과 `tests/test_harness.py`가 예로 쓰는 `split.chunk_size=1000`과 같은 값입니다. 300으로 탐색해 보니 2쪽 문서 청크가 242자로 줄어 휴관 문장이 빠져 조건이 둘로 늘어났고(`/tmp/ch09-06/probe4.py`), 1000에서는 2쪽 전체 905자가 한 문서 청크에 들어와 바뀌는 조건이 색인 하나로 남습니다.
- 위 세 결정은 본문 b7 주의 메모와 노트북 결과 읽기에 「흐름을 보여 주려고 정한 값」으로 적었습니다(규격 §3).

## 5. 산출 파일과 계약

- 쓴 파일: `labs/part3/ch09-rag-first-run/runs/continuity-ch09-search.jsonl`(한 줄)과 사본 `runs/continuity/{source_run_id}.jsonl`.
- **키와 모양은 바꾸지 않았습니다.** 기록 키 여덟 개(`qid`·`question`·`gold_doc_ids`·`source_chapter`·`source_run_id`·`config`·`retrieved`·`answer`), 검색 항목 키 다섯 개(`doc_id`·`chunk_id`·`page`·`rank`·`score`), `config` 안에 라벨 없음, 순위 1부터 차례, 답에 `[E01 p.2]` 모양 출처 표시가 있고 그 (문서, 쪽)이 `retrieved` 안에 있음.
- 읽는 쪽을 파일로 확인했습니다: `textbook/qa/check_course_continuity.py` 94~112행, `textbook/part3/qa/check_continuity.py` 60~78행, `labs/part3/ch11-evaluation/evaluate.py` 176~200행(`retrieved` 항목에 `score`까지 **필수**), `textbook/part3/qa/finalize_continuity_evidence.py` 44~56행, Ch 11 06 노트북(줄 수만 읽음). 계약을 그대로 재현하는 검사를 손으로 실행해 통과했습니다.
- `config` 안에서 바뀐 것(2026-09-17 검토 B R-2 정정): **최상위 키 여덟 개와 `retrieved` 항목 키 다섯 개는 바꾸지 않았고, `config` 안에 `corpus` 한 키를 더했습니다**(`{"tiers": ["easy","medium","hard"]}` — 옛 기록의 `config` 키는 `name`·`split`·`embedding`·`retrieval`·`generation`·`inputs` 여섯 개였습니다). `name`은 `k2`로 같습니다. 이 칸을 읽는 쪽은 없습니다(`evaluate.py`는 보고서 `settings`로 실어 나르고, 검사 스크립트는 라벨 세 개가 `config`에 없는지만 봅니다). `inputs.corpus_scope`는 `"18 digital PDFs"` → `"디지털 PDF 18건"`(읽는 쪽 없음), `inputs.corpus_manifest_sha256`·`evaluation_dataset_sha256`은 개선 전과 같은 값(`27541f4121…`·`9544b332d5…`).
- **해시가 바뀐 것**: `continuity-ch09-search.jsonl` `4f9fce62…ae61` → **`294713765a115b567e162aaf37a25467577841965c1075b86553adc4080666d5`**. 사본 폴더는 7개 → 9개(새 파일 `20260917T180502-ch09.jsonl`·`20260917T181822-ch09.jsonl`, 앞 7개는 그대로). `runs/` 나머지 파일(`runs.jsonl`·`examples/`·2026-09-07 기록 4개)은 해시 전후 같습니다.
- `chunk_id` 앞부분이 `ch09:d853036bf1:0000` → `ch09:6f9f83db90:0`으로 바뀝니다. 이름표 입력에 `corpus`가 들어가고 번호에 0을 채우지 않기 때문입니다. 읽는 쪽은 `chunk_id`가 빈 값이 아닌지만 봅니다(위 두 검사 스크립트·`evaluate.py`).
- **마감 때 다시 만들 것**: `textbook/part3/qa/run_continuity_bundle.py`는 `--reuse-upstream`에서 `labs/part3/ch09-rag-first-run/` 파일 해시를 앞 manifest와 비교하므로 「Upstream execution inputs changed」로 걸립니다. `textbook/part3/qa/continuity-evidence/`의 증거 파일(`bundle-execution-results.json`·`evaluation-verification.md`·`upstream-verification.md` 등)과 `finalize_continuity_evidence.py`가 기대하는 실행 ID 7개도 개선 전 값입니다. `textbook/downloads/part3-practice.zip` 재생성 뒤 함께 다시 만듭니다.
- `config.yaml`·`harness.py`·`prompts.py`·`rag.py`는 읽기만 했고 해시가 그대로입니다(`6da4af21…`·`fc4269d0…`·`4613ba02…`·`16caec34…`). 실습 폴더 테스트 전후 `10 passed`.
- Ch 6·7·8 비용 기록 사슬 파일은 읽지도 쓰지도 않았습니다(`125fc147…58ad`·`a8aaafb7…95e9`·`f18920c6…4f4c` 전후 같음).

## 6. 실행 기록

- 새 커널 두 번. 1차는 생성기 + `execute.py` 직접 실행(18:05:02, 자리 표시 결과 읽기로 출력 먼저 보기), 2차는 `run_section.sh`(18:18:22, **교재 출력**). 두 실행의 구조·검색 순위·이름표·문서 청크 수는 같았습니다.
- **모델 답이 두 실행에서 달랐습니다.** 1차는 한 문장(`미르시립도서관의 정기 휴관일은 매주 월요일입니다. [E01 p.2]`), 2차는 두 문장이고 문장마다 표시를 붙였습니다(`… 매주 월요일입니다. [E01 p.2] 법정 공휴일에도 휴관하며, … 화요일에도 휴관합니다. [E01 p.2]`). 다시 돌려 고르지 않고 2차 출력으로 결과 읽기와 본문을 고쳤습니다(규격 §3, Ch 8 07 선례). 기록 한 줄의 글자 수도 876 → 936으로 달라져 결과 읽기에서 인용하지 않았습니다.
- 점수는 1차 `E01 p.2 | 0.5652`, 2차 `0.5647`로 소수 넷째 자리가 달랐습니다(03절에서 본 변동). 그래서 점수는 그림 라벨·캡션·결과 읽기 첫 단락에 넣지 않았습니다.
- 서비스 요청은 실행마다 7번입니다. 임베딩 `text-embedding-3-small` 6번(색인 2 + 검색 4), `gpt-5.4-mini` 1번. 탐색 실행 4번(probe1~4)을 더해 임베딩 약 21번·mini 1번을 썼습니다. 색인 한 번의 토큰 수는 61,071(`probe3.py`, 비용 어림 0.0012달러)입니다.
- 설명만 고칠 때는 `mdpatch.py`(reps 3회: `/tmp/ch09-06/reps1.json`·`reps2.json`·`reps3.json`) → `run_section.sh … 06 --no-exec`로 재실행 없이 맞췄습니다.

## 7. 그림

- 설계표 `06-figures.md`. Mermaid 4장 PNG 직접 확인, viewBox 297·694·479·821(모두 868 이하).
- 삽화 06-5는 1회 생성으로 채택(job `1cc07d6c-b3fa-43a6-8357-3303c76abf76`, 2크레딧, 잔액 2816 → 2814). 저장 PNG를 채택 job 결과와 픽셀 대조해 차이 0(규격 §5-4). 검수 메모는 `figures/06-5-실험-노트와-기록-용지.prompt.md`.
- 빨강은 06-4 Before 결함 결과 한 상자뿐입니다. 06-3 k=4 결과는 결함이 아니라 노랑입니다.

## 8. 남은 것

- `_src/index.html` 06 행(「설정 변경, 실제 PDF 18개 검색, 질문·정답·청크·쪽·순위 JSONL, 최신 포인터」·「반복 실험 흐름 도식 · 실험 노트 삽화」)과 새 용어 줄의 「설정 해시」·「캐시」·「청크」, 챕터 개요 문단의 「설정 딕셔너리의 값 하나를 바꾸고」 문장은 챕터 마감 때 절 본문과 대조합니다.
- `_build.py` `SECTIONS` 06 제목 「06 · 실험 하네스 — 설정·실행·한 줄 기록」은 바꾸지 않았습니다(바꾸면 05 HTML 링크 줄이 바뀝니다). 실습 절 07을 붙일 때 `SECTIONS`·`render_index()`의 「절 6개」·`_src/index.html` 표를 함께 고칩니다.
- 개선 전 QA 스크립트(2026-09-17 챕터 마감에 실행해 확인): `qa/check_content.py`는 **통과**(개선본에 `{{code:}}`·`{{output:}}`이 0개, 보존 출력 12블록·manifest 해시 12개) → `SECTIONS`에 07을 더했습니다. `qa/test_build.py`·`qa/test_code_evidence.py`는 절 목록과 무관하게 **6 passed**입니다. `qa/test_notebook_migration.py`(`{{svg:}}` 5개·노트북 `except ` 요구로 2건 실패)와 `qa/check_structure.py`(b1~b11·instructor 요구로 01~07 전부 실패)는 개선 전 전제라 `qa/upgrade/before/qa-scripts/`로 `mv -n`했습니다. `qa/verification.md`에는 마감 절을 덧붙였습니다.
- 옛 도식·삽화 `figures/06-하네스-루프.svg/.excalidraw`·`06-실험-노트.png/.caption.md`는 정리 대상(삭제 승인 필요).
- 루트 `textbook/qa/upgrade-progress.md`의 Ch 09 행은 아직 「대기」입니다(01~05절도 같음). 챕터 마감 때 오케스트레이터가 고칩니다.
- 색인을 파일로 저장해 두고 다시 불러오는 일(`dump`/`load`), 여러 질문을 한 번에 돌리기, 비용 계산은 이 절에서 실행하지 않았습니다.

## 검토 반영 (2026-09-17, 챕터 마감 세션)

별도 세션 검토 1차 A(§01~04)·B(§05~07)를 받아 반영했습니다. 보고서와 반영 내역 전체는 `review-round1-A.md`·`review-round1-B.md` 끝 「반영 결과」, 챕터 차원 정리는 `chapter-summary.md`입니다. **이 절 노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 전후 같음). 반영 뒤 게이트 `--label after --strict` 7/7 PASS(G1~G7 0), `verify.py --chapter` `PASS 7 sections / 175 code cells`, `visual.cjs` 16건 PASS, 실습 폴더 테스트 10 passed, 빌드 HTML `{{` 0건.

- **판정 accept-with-fixes**(상 0·중 2·하 4 중 이 절 몫, 검토 B). 반영:
  - **06-1(중)** `figures/06-2-기록-한-줄.mmd` 회색 상자를 「Ch 11이 지표에 쓰는 세 칸<br>question · gold_doc_ids · retrieved<br>이번 절에서는 읽지 않음」으로, 위 칸 왼쪽 상자를 「qid · question<br>Q001」로 바꿨습니다(`evaluate.py` 178행의 필수 키는 일곱 개). b5 도식 읽기에 「나머지 다섯 키가 빠지면 Ch 11 검사가 멈춥니다. 그래서 노트북은 여덟 키를 모두 확인합니다.」를 더했고 alt·캡션·`06-figures.md`도 맞췄습니다.
  - **06-2(중)** 새 용어 여섯 개 가운데 일상 예가 없던 넷에 한 문장씩 더했습니다(실행 설정 = 소금만 한 숟갈 줄이기, 실행 기록 한 줄 = 실험 일지 한 줄, 정답 문서 ID = 시험지 정답표, JSONL = 공책 한 줄에 기록 하나). 네 단락 모두 5문장 상한을 확인했습니다.
  - **06-3(하)** `06-1` `REC`·`06-2` `r3` 라벨을 「답 문장마다 E01 p.2」로, 도식 읽기를 「답은 문장마다 끝에 2쪽 출처 표시가 붙었습니다」로. 이번 답은 문장마다 표시가 붙었고 b5 넷째 단락이 01·04절(끝에 모음)과 대비해 설명합니다.
  - **06-4(하)** 06-1 도식 읽기를 그림 순서(노랑 → 보라 → 노랑 → 초록)대로 다시 썼습니다.
  - **06-5(하)** 노트북 준비물의 없는 절 번호를 「6절 값 바꿔 보기와 Before·After는」으로 고쳤습니다.
  - **R-2(중)** 위 §5의 `config` 문장을 사실(`corpus` 키 추가·`inputs.corpus_scope` 한국어)로 고쳤습니다.
- 라벨을 고친 mmd 두 개는 자동으로 다시 렌더해 PNG를 직접 확인했습니다(viewBox 292.0·723.1, 렌더 도장은 지우지 않음). **노트북은 다시 실행하지 않았습니다**(기록 파일 `294713765a…` 그대로).
- 결정 요청 네 가지(검색 개수 2 유지 / 라벨을 Ch 11 평가셋에서 읽기 / 이름표 입력에 `corpus` 추가 / 두 실행 답 차이 처리)는 권고대로 **모두 유지**했습니다(B Q2). 다만 그 설계를 학생 묶음이 지탱하려면 `config.yaml`·`queries.jsonl`이 묶음에 들어가야 해서(검토 B C-1 = 상) 챕터 밖 허용 목록을 고쳤습니다 → `chapter-summary.md` §7.
- **계약 표에 빠져 있던 읽는 쪽**: `textbook/qa/check_course_continuity.py` 172~198행이 이 절 기록 해시 변경 때문에 182행에서 멈추고 있었습니다(검토 B R-1 = 상). 허용 목록과 분기를 ch10과 같은 모양으로 넓혀 212행 zip 신선도까지 갑니다 → `chapter-summary.md` §8.
- `chunk_id` 자리 채움이 Ch 10과 다른 것(R-3)은 코드를 두고 Ch 10 인계로 적었습니다.
- `config.yaml`의 `[[미정: 임베딩 모델]]` 주석만 정리해 해시가 `6da4af21…` → `1e425071aba21b1a1d99f933003ea423dfe3757a003dabbb5542dd3d9aed1bd1`로 바뀌었습니다. 키 이름·값은 그대로라 `tests/` 10 passed가 유지됩니다.
