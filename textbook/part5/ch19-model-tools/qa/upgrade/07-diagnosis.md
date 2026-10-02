# 07절 「모델과 도구 실습」 신규 집필 기록 (챕터 끝 실습 절, experiment)

새로 만든 챕터 끝 실습 절입니다(규격 `textbook/QUALITY-UPGRADE.md` §7-2, PLAYBOOK §3, handoff 「§06 → 실습(07)」). 수정 전 원본이 없어 `qa/upgrade/before/`에 넣을 파일이 없고, 게이트는 처음부터 이 절 기준으로 잽니다.

- 작업 2026-09-24(03:40~04:20 UTC) · 생성기 `qa/upgrade/author_07.py`(본문과 노트북을 함께 씀, `--src-only`는 본문만, `AUTHOR07_NB_ONLY=1`은 노트북만, `author_06.py`·Ch 18 `author_07.py`가 본 — 06 상수 `PATH`·`DEF_READ`, 05 `html_text`를 import).
- 파일: `_src/07-모델과-도구-실습.html` · `labs/part5/ch19-model-tools/notebooks/07-모델과-도구-실습.ipynb` · 빌드 `07-모델과-도구-실습.html` · `figures/07-1`~`07-4` · `qa/upgrade/07-figures.md` · `qa/upgrade/07-probe.md` · `qa/upgrade/probe/probe07.py` · `qa/upgrade/review-pack/07-모델과-도구-실습.md`.
- **슬러그 `07-모델과-도구-실습`**, 제목 「모델과 도구 실습: 주문 취소 문의를 도구 둘로 처리하고 사람 확인 값 바꾸기」, `chapter.json`에 `format: experiment`로 더함. 규격 §7-2 `{NN+1}-{챕터 이름}-실습`에서 챕터 이름 = `chapter.json` 제목 「모델과 도구」(선례 `06-Agent-개요-실습`·`07-가드레일-실습`·`07-워크플로우-패턴-실습`·`09-Middleware-실습`과 같은 모양, handoff 「§06 → 실습(07)」·작업 지시서 권고와 같음). `textbook/_notebook/build_index.py` 42행 제목은 「LangChain Model과 Tool」이라 다름 — 마감 몫(§13).
- **`hours` 그대로**(「총 16h · 강의 6h · 실습 10h」). 이 절 meta는 「실습 30분 · 새 용어 0」이고 챕터 시수에 더하지 않았습니다(Ch 13~18 선례).
- **서비스 모델 절**입니다. 설명만 고칠 때는 `mdpatch.py` → `run_section.sh … 07 --no-exec`.

## 1. 게이트

| 항목 | 값 |
|---|---|
| 게이트(첫 실행 전, 노트북·본문만 쓴 상태) | `upgrade_gates.py … --label wip-07 --section 07` → **G1 0 · G2 0** · G3 0 · G4 0 · G5 0 · **G6 3** · G7 14(그림 파일·설계표 없음). G6 셋 = b3 뺀 것 단락 한 문장 70자 초과 · b10 기준 버전 한 줄 70자 초과 · b7 목록 항목이 「O102는」으로 시작. 고치자 b10에서 새 70자 초과 하나가 나와 한 번 더 고쳐 **실행 전 G1~G6 0**(`gates-wip-07-07.json`에는 마지막 실행 전 값). 게이트 때문에 다시 실행한 일 없음 |
| 게이트(최종, `--no-exec`) | **G1~G7 모두 0 · PASS**(`gates-wip-07.json`), 코드 셀 **23**(준비 셀 4: 설치·가져오기·자리 찾기·키 — 모델 셀은 준비 셀 아님), 검사 문장 **354** |
| 셀 모양 | 준비 셀이 아닌 셀 최대 **10줄**(주석 뺀 코드 — `COST`), 함수 본문 `get_order_by_id` 4 · `request_cancel` 2 · `handle_inquiry` 6 · `summarize_run` 8 · `print_summaries` 3(모두 8 이하). verify는 주석까지 세어 챕터 최대 13줄(`summarize_run` 셀) |
| 새 커널 | `PASS 07-모델과-도구-실습.ipynb: 23 cells`. 같은 코드(`code_sha256` `5cbee6c49167…`)로 **새 커널 두 번** — 셀별 출력 **20/23 같음**(§5) |
| verify | `PASS 7 sections / 171 code cells (max 13 lines)` |
| 빌드 | 챕터 HTML 여덟 개(절 일곱 + `index.html`) `{{` 잔존 **0건**. 07절 HTML에 Mermaid `svg` 3 · 삽화 1 |
| 그림 | Mermaid 3장(`07-1`~`07-3`, 원본 폭 776·815·609, 빨강 0) · 삽화 1장(`07-4`, 2차 채택) |
| 요청 | 노트북 한 번에 **모델 5번**(실행 1 두 번 + 실행 2 세 번, 준비물 「4~5번」), 임베딩 0. 규격 §7-2의 3~5번 안(위 끝) |

- **게이트가 세지 않는 과정 금지 문법은 AST로 따로 셈**(`/tmp/ch19-07/extra_check.py` — 06 판 복사, 허용 데코레이터 맨 `tool`과 `tool(args_schema=CancelForm)`): 노트북 **3건 = 모두 02절 허용 범위**(양식 클래스 `CancelForm` 1 · 칸 주석 2). 도구 파일 **3건 = 01~06과 같은 허용 범위**(`fetch_orders`의 `status=None` · `estimate_cost`의 `.get` 둘). f-string·내포식·제너레이터 식·`lambda`·조건 표현식·`elif`·`else`·`+=`·기본값 매개변수(노트북)·반환 힌트·튜플 풀기·별표 풀기·`set`/`next`/`sum`/`zip`/`sorted`/`isinstance`·`try` `else`·클래스(양식 클래스 밖)·`raise`(06 읽기 도구 셀 그대로의 한 곳 밖)·파일 쓰기·`time` **0**. `try`는 5절 `except ValidationError as error` 한 곳뿐. `assert`는 준비 셀 둘(자리 찾기·키)과 CSV에서 정해지는 O102 상태 한 곳 — 모델 글·출력에 건 `assert` 0.
- 금지어 확장 목록(인계 용어 표 전부 + 「최대」·「스키마」·「지연」·「순차」·「트레이스」·「돌려주」·「돌려보」·「겹」, `_src`·노트북 설명·코드·출력·`07-*.mmd`·캡션·prompt 파일): 걸린 것은 모두 허용 자리 — 「반환」·「스키마」·「병렬」·「지연」은 02·05절·Ch 6 06절 **링크 파일 이름**, 「로그」는 「프로그램」, 「프롬프트」는 `.prompt.md` 소제목(01~06과 같은 양식), 「겹」은 `.prompt.md`의 「겹치지 않게」. 「한 겹 더」 0.
- 생성기 대조(`/tmp/ch19-07/gen_match.py`): `cells()` 51개가 노트북과 글자까지 같고 `src_html()`이 `_src`와 같음. 06절 셀과의 문자열 대조: `author_07.PATH == author_06.PATH`, `author_07.DEF_READ == author_06.DEF_READ`(생성기 `assert`).

## 2. 주제와 붙인 앞 절 기능 (b3 두 단락)

**주제(새 작은 일)**: 주문 취소 창구. 손님의 주문 문의 하나 「O102 주문이 아직 결제 대기 중이면 취소해 주세요. 다른 상품을 잘못 주문했어요.」(이 절에서 실행 전에 정한 글, 출력 줄 `출처: 이 절에서 실행 전에 적은 글`)를 읽기 도구와 쓰기 도구로 처리합니다. O102는 실습 CSV의 결제 대기 주문 하나뿐이라 골랐고(3절 셀이 `find_order`로 CSV에서 출력), 문의에 조건(「결제 대기 중이면」)을 넣어 모델이 먼저 상태를 읽게 했습니다. 실행 1은 `person_confirmed = False`, 실행 2는 그 값 하나만 `True`.

- **붙인 기능 셋**(인계 권고 「06 사람 확인 값의 실행 1 → 실행 2 모양 + 02 입력 검사 또는 06 오류 담기를 부품으로」):
  1. **02절 입력 검사** — 쓰기 도구 `request_cancel(order_id, reason)`의 입력 형식을 양식 클래스 `CancelForm`(`order_id: str = Field(…)` · `reason: Literal["changed_mind", "wrong_order", "late_delivery"] = Field(…)`)으로 정하고 `@tool(args_schema=CancelForm)`(02 모양, 매개변수 힌트 없음). 몸통은 06처럼 흉내(`{"order_id", "reason", "cancel_requested": True}`), 몸통 첫 줄 `print`(02 `search_orders` 방법). 정해 둔 셋에 없는 까닭 `too_expensive` → 몸통 전 `ValidationError`(**모델 요청 0**, 5절). 실행 2에서는 모델이 적은 까닭이 이 검사를 지나 몸통이 실행됨(몸통 줄).
  2. **05절 도구 실행 반복** — 조립 함수 안 `ask_until_answer`(도구 파일)가 도구 호출 요청을 실행하고 도구 메시지를 넣어 다시 묻는다. 실행 2에서 읽기 결과(`pending`)를 본 모델이 다음 응답에서 쓰기 도구를 요청 — 앞 절이 따로 보인 「읽기」와 「쓰기」가 한 흐름에서 이어짐.
  3. **06절 읽기·쓰기 분리** — `pick_tools(read_tools, write_tools, person_confirmed)`가 알려 줄 목록을 고르고, `bind_tools`·`make_tools_table`도 같은 목록(06 After 모양). 바꾸는 값 = 사람 확인 값.
  읽기에 이어 쓴 것(기능으로 세지 않음): 06 읽기 도구 셀 그대로(오류 담기 설정 `True`) · 03 `find_order`·자세한 판 네 기준(쓰기 도구 설명) · 04 `tool_call_names`·입력 토큰 · 06 `spec_names`·`show_messages` · 05 `sum_usage`·Ch 6 06 `estimate_cost`.
- **고른 까닭**(b3 셋째 단락): 두 실행의 요청 수를 실행 전에 셀 수 있음(요청한 도구 수 + 최종 답 하나), 02 입력 검사는 도구 안에서 일해 모델 요청을 늘리지 않음.
- **뺀 것과 까닭**(b3 넷째 단락):
  - 04절 선택 채점(`ask_questions`) — 질문 × 반복만큼 요청(04 노트북 28번).
  - 05절 여럿 담기(`parallel_tool_calls=True`) — 한 응답의 요청 수를 모델 답이 정함(인계 「05 병렬 조심」).
  - **06절 오류 담기 장면(없는 주문 번호)** — 읽기 도구에 켜 두기만 함(b7 「이번 흐름에서는 도구 오류가 나지 않았다」). 없는 주문에 쓰기 도구까지 알려 주면 흉내 쓰기 도구가 그 취소도 등록할 수 있어, 06 b7이 「다루지 않음」으로 둔 **쓰기 도구 안 주문 번호 재검사**가 필요해짐(작업 지시 「새로 풀지 않기」).
  - 06절 한 목록/나눈 목록 견주기 — 06 실험 되풀이(규격 §7-2 5항). 이 절의 실행 1·2는 06 값 바꿔 보기와 달리 **새 문의·새 쓰기 도구**이고, 실행 2에서 읽기 → 쓰기가 한 흐름에 이어지는 것을 봄(06 값 바꿔 보기는 첫 응답이 곧바로 쓰기 도구).
- **06 b7 「다루지 않음」은 새로 풀지 않았습니다**: 입력 검사는 **취소 까닭 칸만** 보고 주문 번호·상태를 다시 검사하지 않음(b4 「비교와 경계」·b7) · 사람 확인 값은 참/거짓 하나(b7) · 서비스 오류 다루지 않음(b7) · `ValueError`는 쓰지 않음.
- **손으로 적은 새 값**(실행 전에 정함, 출처를 출력과 b7에): 문의 글(출력 `출처:` 줄) · 주문 번호 O102(3절 출력 `주문 상태: pending`, b7 「결제 대기 중인 주문 하나뿐이라 골랐다」) · 취소 까닭 셋과 막히는 예 `too_expensive`(4·5절 설명, b7). 모두 `07-probe.md` §0에 첫 요청 전에 적었습니다.

## 3. 흔들림 확인 — `qa/upgrade/07-probe.md`

- 첫 요청(03:48:42Z) 확인 1번: `args_schema` 쓰기 도구를 읽기 도구와 함께 `bind_tools`한 요청이 **받아들여짐**(명세에 `enum` 셋 실림, 입력 319·출력 21). 02절 도구 모양이 모델 요청에 실린 것은 이 절이 처음.
- 5회차(03:48:50~49:13Z, 요청 25): 실행 1 **5/5** 읽기 도구만·success·요청 2 · 실행 2 **5/5** 읽기 → 쓰기(`O102`·`wrong_order`, 몸통 줄 한 번)·success 둘·요청 3 · 흐름 끝 도구 호출 요청 0건 10/10 · 첫 요청 입력 토큰 203·319 10/10 · 캐시 입력 50/50 0. 흔들린 것은 실행 1 끝 응답의 출력 토큰(74~127)과 답 글뿐.
- 실행 전에 적은 후보 A·B 가운데 A가 §0 조건을 모두 만족해 A(B는 보내지 않음). 원하는 값이 나올 때까지 다시 보낸 일은 없습니다. 노트북 실행은 A·B 두 번뿐입니다.

## 4. 셀과 함수

제목 → 오늘 볼 그림(`07-1`) → 1 준비(설치 여섯 / 가져오기 — 도구 파일 함수 아홉 알파벳 순 + 고정 세 문장 + 커널 폴더 한 문장 / 자리 찾기 — 01~06과 글자 같음) → 2 키와 모델(`nbkit.key_and_model_cells`) → 3 상황과 대상 주문(문의·출처 → `find_order` O102) → 4 부품 하나(06 읽기 도구 셀 그대로 → 오류 담기 설정 `True`·읽기 목록) → 5 부품 둘(양식 클래스 → 쓰기 도구 → 쓰기 목록·취소 까닭 칸 → `too_expensive` 막힘) → 6 조립 함수와 기록 장치(`handle_inquiry` · `summarize_run` · `print_summaries`) → 7 실행 1(예상 → 실행 → 요약) → 8 실행 2(바꿀 값 하나 · 예상 → 실행 → CSV 확인) → 9 두 실행 견주기(요약 표 → 첫 요청 입력 토큰) → 10 요청 수와 예상 비용 → 정리 세 줄. PLAYBOOK §3 차례(준비 → 주제 → 재료 → 기록 장치 → 조립 → 실행 1 → 실행 2 → 정리)와 같습니다.

- **새로 만든 함수 셋(노트북에만)**: `handle_inquiry(model, read_tools, write_tools, person_confirmed, question, turn_limit)`(본문 6, 주석에 05·06절, 흐름 결과 `{"사람 확인", "명세", "메시지"}`) · `summarize_run(result)`(본문 8, 실행 요약 `{"사람 확인", "명세", "요청한 도구", "결과 상태", "요청 수"}`) · `print_summaries(summaries)`(본문 3). 노트북 전역 이름을 읽지 않음. 실습 절 전용이라 도구 파일에 옮기지 않음(Ch 17 06·Ch 18 07 선례).
- 새 도구 정의 하나(`request_cancel`)와 양식 클래스 하나(`CancelForm`)는 **02·06 문법 그대로**(`@tool(args_schema=…)`·`BaseModel`·`Field`·`Literal`). 새 문법·API·말 **0개**: 말은 조립 함수·기록 장치·실행 요약(Ch 15~18 실습 절 말), 취소 까닭·주문 문의(일상어), 나머지는 01~06절 말(도구·도구 설명·입력 형식·도구 명세·양식 클래스·고를 수 있는 값·입력 형식 클래스·입력 검사·값 검사 오류·몸통 함수·공개 이름·도구 호출 요청·도구 메시지·도구 찾기 표·바퀴 한도·읽기 도구·쓰기 도구·오류 담기 설정·결과 상태·사람 확인 값·흉내).

## 5. 새 커널 두 번 실행 (셀별 대조)

| 실행 | UTC(첫 셀 입력 → 마지막 셀 응답) | 코드 | outputs | 비고 |
|---|---|---|---|---|
| **A(교재 출력)** | 03:57:43.23 → 03:57:50.85(7.62초) | `5cbee6c4916753323d23b813f1dd6305d0899026a43e0e94975aa6be0a1c0725` | `5d08a908edf7c864e558ffa659a1d4bc278c5ca2a26de652ed4283aceb0a69af` | `run_section.sh … 07`(그림 전이라 첨부 단계에서 `FileNotFoundError`로 멈췄지만 실행은 저장됨), 사본 `/tmp/ch19-07/A.ipynb` |
| B | 03:58:05.63 → 03:58:12.10(6.47초) | 같음 | `27797500d94a…` | 사본 `/tmp/ch19-07/B.ipynb`(인계 「챕터 공통」 명령) |

- **셀별 출력 20/23 같음.** 다른 세 셀: ① 실행 1 셀의 답 글(A 「… 이라서 취소 가능합니다 … 실제 취소 실행 기능이 없어, 제가 바로 상태를 변경하진 못합니다 …」 / B 「… 이라 취소 가능합니다. … **취소 처리해 드릴게요**. 원하시면 제가 바로 취소 완료로 안내하겠습니다.」) ② 실행 2 셀의 답 글(「이어서」/「이라」 한 낱말) ③ 10절 출력 토큰 합·예상 비용(A 194·`0.002079` / B 154·`0.001899`). 같은 셀의 흐름 줄·몸통 줄·명세는 두 번 같음.
- **B의 실행 1 답 글**은 쓰기 도구를 모르는데도 취소를 해 줄 것처럼 적었습니다. 흐름에 쓰기 도구 요청은 없었고 CSV도 그대로였습니다 — 7절 결과 읽기 둘째 단락과 b7에 「모델이 무엇을 했는지는 답 글이 아니라 도구 호출 요청과 도구 메시지로 확인」으로 적었습니다(결론·그림 밖).
- 그림은 A·B를 마친 **뒤에** 처음 렌더했습니다(Mermaid 03:59, 삽화 제출 04:00:57). 준비물 `[[RUNSEC]]`, 결과 읽기 둘째 단락 셋(`[[RUN_ONE_READ2]]`·`[[RUN_TWO_READ2]]`·`[[COST_READ2]]`), 그림 alt·도식 읽기·삽화 글, b6·b7 자리표시는 A·B 대조 뒤 `mdpatch.py`(`/tmp/ch19-07/reps1.json`)로 채우고 `author_07.py --src-only`(삽화 풀이 단락·긴 문장 둘) 뒤 `run_section.sh … 07 --no-exec` 세 번. **노트북 `code_sha256`·`outputs_sha256`·`executed_at`은 A 그대로**(최종 노트북과 `A.ipynb` 셀별 23/23 같음).
- **두 번 모두 같음 → 결론·그림·정리에 씀**(밖 다섯 번과도 같음): `취소 까닭 칸: {… 'enum': ['changed_mind', 'wrong_order', 'late_delivery'] …}` · `받은 오류: ValidationError`·`1 validation error for CancelForm` · 실행 1 `실어 보낸 도구 이름: ['get_order_by_id']`·`['get_order_by_id']` → `success` → `[]`·`False | ['get_order_by_id'] | ['get_order_by_id'] | ['success'] | 2`·`쓰기 도구 요청이 있었는가: False` · 실행 2 `쓰기 도구 몸통 실행 | 주문 번호: O102 | 까닭: wrong_order`·`['get_order_by_id']` → `['request_cancel']` → `[]`·`success` 둘·`True | … | 3` · `CSV의 O102 상태: pending` · `쓰기 도구 요청 | 실행 1 False | 실행 2 True` · `두 실행의 질문이 같은가: True` · `첫 요청 입력 토큰 | 실행 1 203 | 실행 2 319` · 요청 5·입력 토큰 합 1608.
- **결론에 쓰지 않은 값**: 답 글 문장(둘째 단락에만), 출력 토큰 합·예상 비용(둘째 단락·「확인할 점」만), 취소 까닭 `wrong_order`(7/7 같았지만 모델이 고른 값 — b7에 「결론에 쓰지 않음」), 첫 응답 도구 이름(7/7 `get_order_by_id`였지만 결론은 「쓰기 도구 요청 유무」로 적음).
- 준비물 「10초 안에」 = A 셀 실행 기록 7.6초(설치 셀 포함, 커널 시작 뺌). 본문은 「걸린 시간은 재지 않았습니다」(b7).

## 6. 도구 파일 (§2-7)

- **바꾸지 않았습니다.** 해시 **`f2f48a150dd9cd80cf13c74669489830282394812e9cc7b05bb039fd2419fda5`** 그대로(06절 끝, 함수 14). 이 절이 가져오는 함수 아홉(`ask_until_answer`·`estimate_cost`·`find_order`·`make_tools_table`·`pick_tools`·`show_messages`·`spec_names`·`sum_usage`·`tool_call_names`)은 모두 이미 파일에 있고, 노트북에만 있는 앞 절 **평범한 함수**를 다시 쓰지 않았습니다. 03·05·06 노트북이 가져오는 이름 영향 없음.
- 06절 **도구 객체** `get_order_by_id`는 06절 3절 셀을 그대로 다시 적었습니다(`author_06.DEF_READ`와 문자열 같음 — 챕터 리드 결정 2, 도구 객체는 파일에 두지 않음). 06 쓰기 도구 `cancel_order`는 쓰지 않고, 02 입력 검사를 붙인 새 쓰기 도구 `request_cancel`을 만들었습니다(설명은 03 자세한 판 네 기준, 06 `author_06.WRITE_DOC`과 첫 문장 모양만 이음).

## 7. 함께 고친 파일

**챕터 안**
- `chapter.json` — `sections`에 07 한 줄(`06823dbdea1b…` → `73efb2749508…`, `hours`·`objectives` 그대로 — objectives는 마감 몫).
- **06절 마지막 문장은 고치지 않았습니다**: b8·노트북 정리 끝 줄 「07절 실습에서는 이 챕터에서 만든 도구와 함수를 모아, 주문 문의 하나를 처리합니다.」 — 07이 이 챕터의 도구·함수(06 읽기 도구·02 입력 형식·03~06 함수 여덟)를 모아 주문 문의 하나를 처리하므로 **그대로 참**. `mdpatch.py`·`--src-only` 쓰지 않음. **06 노트북 `f3d5351af024…` · `code_sha256` `87a30720b3e2…` · `outputs_sha256` `0271e22d7387…` · `executed_at` 03:20:26 그대로**, 06 `_src` `fd92c3e74d9b…` 그대로, 06 게이트 **0**(검사 문장 399 그대로 — 파일을 쓰지 않는 방식으로 `check_section` 직접 호출). **06 빌드 HTML만 `628e910b…` → `f5e9c73c…`**: `_build.py`가 다음 절 링크를 「챕터 끝」에서 07절 링크로 바꾼 한 줄뿐(그 한 줄을 「챕터 끝」으로 되돌리면 `628e910b3bf4…`와 같음을 확인).
- 새 파일: 노트북 07 · `_src/07` · 빌드 `07-모델과-도구-실습.html` · `figures/07-*`(mmd 3·svg 3·png 4·render.json 3·caption 4·prompt 1) · `qa/upgrade/author_07.py` · `07-figures.md` · `07-probe.md` · `07-diagnosis.md` · `probe/probe07.py` · `gates-wip-07.json`·`gates-wip-07-07.json` · `review-pack/07-모델과-도구-실습.md`. 챕터 `index.html`(07 링크) 다시 빌드(`ee28f1a267eb…`). 01~05절 빌드 HTML도 `_build.py`가 다시 썼습니다(원고 변경 없음, 07 링크 없음 — 보호 목록에 있는 03·05 빌드 HTML은 06절 끝 해시 그대로).
- `qa/upgrade/handoff.md` 「실습 → 챕터 검토」, `집필점검표.md` 품질 개선 표 07 행(`a9058d7cd651…` → `625de7b6bbdb…`), `qa/verification.md` 품질 개선 검증 표 07 행(`b35744b267ae…` → `f20fca130e88…`).
- 챕터 `qa/public-files.json`은 **고치지 않았습니다** — `labs`가 `notebooks/*.ipynb`·`notebooks/order_tools.py` 글롭이라 07 노트북이 자동으로 들어갑니다(새 zip에 있음 확인).

**챕터 밖**
- `labs/part5/ch19-model-tools/README.md` — 맨 아래 **07절 한 단락만** 더함(`15d43c735a0c…` → `917725f6a949…`). 옛 문장(「노트북은 서로 독립적」 등)은 손대지 않음 — 마감 몫.
- `textbook/part5/index.html`·`textbook/downloads/part5-practice.zip`·`textbook/part5/qa/integration-results.json` — `python3 textbook/part5/_build_index.py`로 다시 만듦(**`Part 5: 24 verified sections; 63 bundled files`**). 목차 `768a67901657…` → `29775f045671…`, zip `fe86015301d5…`(Ch 18 마감 판, 23절·61파일) → **`40c10aeca375a4efb31ddfdbce02b9a26bca29999ff20f834d6db9591359fa1b`**, `integration-results.json` `60df3c5d63c5…` → `f00380838ee8…`. 새 zip에 Ch 19 개선 노트북 01~07과 도구 파일 `order_tools.py`가 처음 들어갔습니다(Ch 19 01~06 작업 중에는 zip을 다시 만들지 않았음). `_build_index.py`의 Ch 19 설명 한 줄(「입력 검증」 — 금지어)은 고치지 않음 — 마감 몫.
- `textbook/_notebook/checks/notebook-contracts-part5-ch19-model-tools.json` — `verify.py --chapter`가 다시 씀(공용 검사 산출 파일, `31a50bbdf167…`).
- **`textbook/part5/public-files.json`은 고치지 않았습니다** — 노트북은 `build_bundle.practice_files`가 `_src` 슬러그로 자동으로 고름(Ch 17·18 선례). **Part 6 묶음(`part6-practice.zip`)은 돌리지 않았습니다** — 07은 Part 6 선행 목록에 없음(`textbook/part6/prerequisite-files.json`·Ch 28 `qa/prerequisite-files.json` 확인만, 마감 몫).
- 공용 도구(`textbook/_notebook/`·`textbook/_template/`) 코드·규격·과정 요약·계약 파일·Part 6 파일·완료 챕터 파일·Ch 20·Ch 28 파일은 고치지 않았습니다.

## 8. 그림 — `qa/upgrade/07-figures.md`

- Mermaid **3장**(규격 §7-2 넷 가운데 셋): `07-1`(b4 조립도 + 노트북 오늘 볼 그림, flowchart TB, 폭 **776**, 노드 7) · `07-2`(b5 실행 1의 실제 순서, `sequenceDiagram`, 폭 **815**) · `07-3`(b6 실행 1·2 비교, subgraph 둘 + 회색 공통 상자, 폭 **609**). 모두 868 아래, **보라는 `07-1`의 모델 한 상자만**(`07-2` 세로줄 머리는 기본 회색 — 05-1·Ch 18 07-2 선례), **빨강 0**. 첫 렌더 고침: `07-1` 「06절 pick_tools로 목록 / 고르기」 꺾임, `07-2` 첫 메모 글이 상자 가장자리에 닿음(두 줄로 나눠 폭 856 → 815), `07-3` 공통 상자 「같은 두 도구 · / 바퀴 한도 5」 꺾임 — 모두 `<br>`로 미리 나눔. PNG를 직접 열어 본 **뒤에** alt·도식 읽기를 썼습니다(`.cache/ch19-07-view/v1-07-1~3.png`·`v2-07-1~3.png`·`v3-07-3.png`). 답 글·출력 토큰·예상 비용은 어느 그림에도 없습니다.
- 삽화 **1장** `07-4-도장-받은-전표와-취소-상자`: 「식당 주문 전표와 내주는 창」 계열의 새 조립 장면 — 열린 창(두 실행이 모두 쓴 읽기 도구) · 입구가 있는 나무 상자(쓰기 도구) · 나무 도장(사람 확인 값) · 표시 없는 전표(실행 1)와 도장 자국 전표(실행 2). 앞 절 소품(02 덧문·주황 별·빈 접시, 03 흐린 카드, 04 빈 이름표·칠한 칸·회색 집게, 05 색 집게·같은 그릇 둘·걸린 전표, 06 걸쇠 서랍·창턱 그릇·국자)과 금지 소품(자물쇠·열쇠·칼·쟁반·울타리·발자국·저울·바구니·길·공구판 구멍)은 쓰지 않음. `nano_banana_pro`(응답 `nano_banana_2`) · 16:9 · 2k · `use_unlim: false` · count 1. 생성 전 잔액 **2551.25**.
  - **1차 job `d949cca9-00a8-41e9-ae09-f2f6577deea2` 탈락** — 구성은 맞았지만 상자에 꽂힌 전표가 흰 바탕 가운데 빨간 원 하나라 **한 나라의 국기로 읽힘**(관계와 무관한 연상), 창 안쪽도 칠하지 않은 흰 칸. 원본 `2b76592e…`.
  - **2차 job `3e98a3ed-befc-4d8f-a315-85cac89996b8` 채택**(재생성 1회 — 상한). 원본 `7ffd3049…`(2752 × 1536) → 저장 1100 × 614 `876b6c6d…`. 결과 URL을 다시 받아(같은 해시) 같은 폭으로 줄여 저장 PNG와 픽셀 대조: bbox `None`, 세 칸 extrema `(0, 0)`. 저장본 사본(`.cache/ch19-07-view/saved-07-4.png`)과 상자 부분 확대(`illu-2-box.png`)를 열어 셌습니다 — 문짝 하나가 열린 나무 틀 창 **하나**(안쪽 짙은 초록, 창턱 비어 있음) · 카운터 앞쪽 표시 없는 줄 그은 전표 **하나**(상자와 떨어짐) · 윗면 입구가 있는 나무 상자 **하나**(입구에 전표 한 장이 반쯤 꽂힘, 앞면에 드러난 종이 오른쪽 아래 빨간 동그라미 테두리 도장 자국 **하나**) · 나무 도장 **하나**. 생성 요청의 「no door panel」과 달리 창에 문짝이 그려졌고, 상자 앞면 종이는 꽂힌 전표가 비쳐 보이는 모양이라 그림 읽기에는 보이는 그대로 「상자 앞면에 드러난 종이」로 적음.
  - 크레딧: 거래 기록 **04:00:57Z · 04:02:07Z 「Nano Banana Pro −2」 두 줄 = 이 절 몫 4크레딧**(그 앞 줄은 06절 03:23:40Z), 생성 뒤 잔액 2547.25.

## 9. 검사 스크립트가 멈춘 자리

- `python3 textbook/part5/qa/check_delivery.py` — **115행 `Stale file: labs/part1/ch01-development-environment/notebooks/01-과정-지도와-학습-규칙.ipynb`**(`llm-practice.zip`)에서 멈춤(Ch 14~18 때와 같은 자리, 전체 마감 몫). 멈춰서 `qa/delivery-results.json`은 다시 쓰지 않았습니다(`a446579388c4…` 그대로).
  - 같은 대조를 `llm-practice.zip`만 빼고 파일을 쓰지 않게 따로 돌린 결과: **HTML 30쪽 · 절 24 · 로컬 링크 누락 0 · 비밀값 노출 0 · 복습 문제 오류 0 · `part5-practice.zip` manifest 63항목 어긋남 0 · part5 노트북 24 = 절 24**.
- **학생 묶음 확인**(규격 §7-2): 새 zip에서 Ch 19 폴더만 `/tmp/ch19-07/bundle/`에 풀어, 07 노트북의 모델을 부르지 않는 셀 열넷(가져오기·자리 찾기·문의·대상 주문·도구 정의 둘·설정·양식 클래스·취소 까닭 칸·`too_expensive` 막힘·조립 함수·기록 장치 둘·CSV 확인)을 `OPENAI_API_KEY` 없이 `--cwd …/notebooks`로 실행 → **PASS 14 cells**(도구 파일 가져오기 통과, 자리 찾기 `../../../..`). 커널은 `uv sync --locked`로 만든 `.venv`가 아니라 작업 가상환경입니다.
- `check_bundle_execution.py`(Ch 19 01 대상)는 돌리지 않았습니다(마감 몫). 옛 검사 스크립트 `textbook/part5/qa/check_scope.py`의 `SECTION_COUNTS` Ch 19 = 6·실습 meta 정규식은 07절과 어긋나 멈출 것입니다 — 돌리지 않았습니다(옛 QA 기록을 덮어쓰지 않으려고, 기록만).

## 10. 보호 파일 39개

`before-manifest.json` 39개 — 작업 시작(03:4x, 33개 같음·6개 바뀜 = 06절 끝과 같음)과 끝에 다시 계산: **32개 같음, 7개 바뀜**. ① 06절 끝과 같은 여섯(03·05·06 노트북과 03·05·06 빌드 HTML) — 03·05 노트북·03·05 빌드 HTML·06 노트북은 06절 끝 값 그대로이고, **06 빌드 HTML만 `628e910b…` → `f5e9c73c…`**(다음 절 링크 한 줄, §7). ② **`textbook/downloads/part5-practice.zip` `fe860153…` → `40c10aec…`** — 작업 지시(§4 「Part 5 목차·묶음: `_build_index.py` 한 번」)대로 목차·묶음을 다시 만든 결과입니다(준비 조사 ③ 「이 챕터가 바꿀 파일」 목록 밖이지만 묶음 재생성은 Part 5 절을 더하면 따라오는 일 — Ch 18 07 선례). 07 새 파일은 목록 밖입니다. 07은 `data/orders.csv`를 읽기만 합니다(`f2d1e3ee…` 그대로).

## 11. 요청 수 · 비용

- 노트북 실행 한 번 **5번**(규격 §7-2 범위 위 끝, 준비물 「4~5번」 — 실행 2에서 모델이 읽기 도구를 건너뛰면 4번, 바퀴 한도 5라 실행 한 번에 많아야 5번). 작업 합계 **36번**(노트북 밖 확인 1 + 흔들림 25 + 새 커널 A 5 + B 5). 설정 대조·입력 검사 확인·묶음 확인은 0번. 모두 `gpt-5.4-mini`, 임베딩 0, 오류 0.
- 사용량 합: 입력 11,575 · 출력 1,411 토큰(밖 8,359·1,063 + A 1,608·194 + B 1,608·154). 요금표(Ch 6 06, 2026-09-17: 100만 토큰당 입력 0.75 · 캐시 입력 0.075 · 출력 4.50달러)로 어림하면 **약 0.015달러**(청구 금액 아님). 노트북 한 번은 약 0.002달러.
- 삽화 두 장(1차 탈락·2차 채택) 4크레딧(§8).

## 12. 강사 확인 대상

1. **붙인 조합(02 입력 검사 + 05 반복 + 06 목록 고르기)과 뺀 것**(§2) — 특히 06 쓰기 도구 `cancel_order`를 그대로 쓰지 않고 02 입력 형식(취소 까닭 셋)을 붙인 새 쓰기 도구 `request_cancel`을 만든 것. 인계 권고 「02 입력 검사를 부품으로」를 쓰기 도구에 붙이면서, 06 b7의 주문 번호 재검사를 풀지 않으려고 **까닭 칸**만 검사하게 했습니다.
2. **모델 요청 5번**(3~5번의 위 끝). 조건이 든 문의라 실행 2가 읽기 → 쓰기 세 번. 준비물은 「4~5번」.
3. **실행 1 답 글이 도구 없이 취소를 해 줄 것처럼 적은 실행이 있음**(새 커널 두 번째 B). 결론은 흐름의 도구 호출 요청·도구 메시지로만 세웠고, b7에 「답 글이 아니라 도구 호출 요청과 도구 메시지로 확인」을 적었습니다. 학생에게 이 점을 따로 짚을지.
4. **오류 담기 설정을 켜 두었지만 흐름에서 쓰이지 않음**(b7). 06 After와 같은 읽기 도구를 그대로 쓰려고 둔 것입니다.
5. **사람 확인 값은 참/거짓 하나, 입력 검사는 까닭 칸만** — 실행 2의 사람 확인이 어느 주문을 확인했는지는 코드가 가리지 않음(06 b7과 같음).
6. 삽화 `07-4` 2차 채택본의 상자 앞면 종이(꽂힌 전표가 비쳐 보이는 그림)와 창의 문짝 — 「그림만 보고 관계가 읽히는가」 판독은 별도 세션 몫. 1차는 국기 연상으로 탈락.
7. 코드 셀 23(실습 선례 20~25 안), 새 함수 셋은 노트북에만.
8. 한국어 감사 3단은 별도 세션 몫.

## 13. 챕터 마감 몫 (이 절이 더하거나 확인한 것 — handoff 「실습 → 챕터 검토」 §5에 모음)

- `chapter.json` `objectives`(셋째 「반환」·넷째 「제공 경로」, 07 실습 줄을 넣을지) → `_build.py`·`textbook/part5/_build_index.py` 23~24행 Ch 19 설명(「입력 검증」)·`textbook/_notebook/build_index.py` 42행(절 수 6 → 7, 제목 「LangChain Model과 Tool」 ↔ 「모델과 도구」).
- 실습 폴더 `README.md` 전체 다시 쓰기(07 단락은 이번 판) → `part5-practice.zip` 재생성.
- Part 6 선행 목록 둘에 `order_tools.py`를 더할지 · `final-artifact-hashes.json` 355~357행 · `part6-practice.zip` 재생성(07은 Part 6에 없음).
- `check_scope.py` `SECTION_COUNTS`(기록만) · `check_bundle_execution.py`(Ch 19 01) · `check_delivery.py`(`llm-practice.zip` Stale — 전체 마감).
- `gates-after.json`(`upgrade_gates.py textbook/part5/ch19-model-tools --label after`) · `visual.cjs` 1280px·390px(HTML 여덟 개) · `chapter-summary.md`(**실습 30분은 챕터 시수에 더하지 않음**, 07은 새 문법·API·말 0, 도구 파일 함수 14 그대로).

## 14. 지우지 않은 것 (삭제 승인 대상)

- `qa/upgrade/gates-wip-07-07.json`(첫 실행 전 게이트) · `qa/upgrade/gates-wip-07.json`(최종 게이트 — 마감 때 `gates-after.json`으로 모음) · `qa/upgrade/probe/probe07.py`(밖 확인 스크립트 — 04~06 선례대로 남김) · `qa/upgrade/__pycache__/author_07.cpython-310.pyc`·`author_07.cpython-312.pyc`(생성기와 확인 스크립트가 import 해서 생김, 01~06과 같은 폴더).
- 프로젝트 `.cache/ch19-07-view/`: Mermaid 확인 사본 `v1-07-1~3.png`·`v2-07-1~3.png`·`v3-07-3.png`, 삽화 `illu-1-1100.png`·`illu-2-1100.png`·`illu-2-box.png`·`illu-2-window.png`·`saved-07-4.png`.
- 기기 `/tmp/ch19-07/`: `protect.py`·`protect-start.txt` · `chapter.before.json`·`README.before.md`·`author_07.stub.py`(코드 셀 상수만 있던 첫 판)·`code_block.py`·`head.py`·`tail1.py`·`tail2.py`(생성기 조각) · `probe-check.jsonl`·`probe-A.jsonl` · `A.ipynb`·`B.ipynb`·`A-start.txt` · `reps1.json` · `extra_check.py`·`cmpnb.py`·`gen_match.py`·`shrink.py`·`cmpimg.py`·`crop.py` · 삽화 `illu-1-orig.png`·`illu-2-orig.png`·`illu-2-again.png`(각 2752px)·`illu-1-1100.png`·`illu-2-1100.png`·`illu-2-box.png`·`illu-2-window.png` · `part5-before.txt` · 묶음 확인 `bundle/part5-practice/labs/part5/ch19-model-tools/…`(+ `check07.ipynb`).

## 마감 반영 (2026-09-24)

검토 1차(`review-round1-A.md`·`review-round1-B.md`)를 반영했습니다. **노트북은 다시 실행하지 않았습니다**(`code_sha256`·`outputs_sha256`·`executed_at` 그대로, 마크다운만 — `mdpatch.py`로 생성기·노트북·`_src`를 같이 고친 뒤 `run_section.sh … --no-exec`). 전체 기록은 `chapter-summary.md` §15.

- **B-9**: b7 새 항목 「흐름 안에서 모델이 정해 둔 셋 밖의 까닭을 보내면 값 검사 오류가 납니다 · 오류 담기 설정으로 받지 못해 06절 Before처럼 흐름을 멈춥니다 · 오류 담기 설정은 읽기 도구에만 켰고 켜더라도 도구 오류만 받습니다 · 설치한 langchain-core 1.6.2 소스로 확인했고 이번에 실행하지 않았습니다」(새 API 이름 없음 — `tools/base.py` 542~544·1088~1092·1109~1117행). [22]는 「읽기 도구가 도구 오류를 내면 …」으로 한정하고 「이 설정은 읽기 도구에만 켰고, 쓰기 도구의 입력 검사 오류는 받지 않습니다」. 오류 담기 설정 셀은 그대로(06 셀과 글자 같음).
- **B-10**: b3 「요청 수를 실행 전에 셀 수 있기 때문」 → 「범위로 어림할 수 있기 때문」.
- **B-11**: 설계 그대로, b2 둘째 단락 끝에 「바꾸는 값은 06절 값 바꿔 보기와 같고, 새로 볼 것은 입력 검사를 붙인 쓰기 도구가 읽기 결과 뒤에 이어 불리는 차례입니다」.
- **B-12(다시 만들지 않음)**: PNG를 직접 봄 — 꽂힌 전표 아래 상자 앞면에 그 전표의 아래쪽이 비쳐 보이는 모양으로 그려져 있고, 도장 자국은 거기에 있음. 그림 읽기·풀이·alt·캡션을 한 전표·한 관계로(「도장 자국이 찍힌 전표 한 장은 상자 입구에 꽂혀 있고, 표시 없는 전표는 카운터에 그대로」, `07-4-…caption.md`도). 창 문짝이 02 덧문과 가까운 점은 강사 확인.
- **A-8(07 몫)**: 복습 2 해설 「b4 「두 번의 실행」」 → 「본문 4 「핵심 개념」의 「두 번의 실행」」.
- **A-4(07)**: b3 표의 「몸통 전 입력 검사」·b4 「비교와 경계」가 이미 자리를 밝혀 더하지 않음.
- **그대로 둔 것**: B 실행 답 글 어긋남(둘째 단락·b7) · 요청 5번(강사 확인).
- **자리 찾기 셀 결과 읽기(A-11·B-14)**: 「교재 출력은 실행 도구에 도구 파일 폴더를 따로 알려 준 실행이라 `.`이 찍혔습니다」와 「셀 안의 안내 글은 실습 폴더 맨 위도 적었지만, 도구 파일을 가져오려면 `notebooks/` 폴더에서 열어야 합니다」를 더함. 셀 안 `assert` 안내 글(「notebooks 폴더나 실습 폴더 맨 위에서」)과 생성기의 같은 코드는 그대로 — **다음 재실행 때 「notebooks 폴더에서」로**.
- 노트북 파일 `79d5b0d9…` → `4f8f9ed5…`. 게이트 0(검사 문장 354 → 363).
