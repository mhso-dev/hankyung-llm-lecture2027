# Ch22 검증 기록

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11
- 노트북: 8개를 새 커널에서 순차 실행합니다. 코드 셀은 목적 주석·함수 타입 힌트·25줄 이하·assert 조건을 확인합니다.
- API: 01절 실제 모델 정의 호출과 03절 실제 요약 호출에서 `.env`의 키 존재만 확인하며 키 값은 출력하지 않습니다. 두 절 모두 `usage_metadata`로 예상비용 1달러 미만을 검사합니다.
- 도식: 절별 SVG와 같은 요소의 Excalidraw JSON을 생성합니다. 생성형 삽화와 MCP 미리보기는 사용하지 않았습니다.
- 빌드: `_build.py`, 공통 `verify.py`, Playwright 1280px·390px 시각 검사를 실행한 결과를 아래에 기록합니다.

## 실행에서 확인한 값

- `execute.py`: 8개 노트북 모두 PASS, 총 코드 셀 50개, 최대 24줄입니다.
- 01절: `before_agent`와 `after_agent`는 각각 1회, 모델 관련 훅은 모델 호출 2회에 맞춰 2회씩, 도구 감싸기 훅은 1회 실행됐습니다. 실제 GPT-5.4 mini 호출의 예상비용은 0.000199달러였습니다.
- 02절: Ch16 원본 함수와 같은 네 정규식에서 email·phone·rrn·card가 각각 1건 검출되어 `<EMAIL_MASKED> <PHONE_MASKED> <RRN_MASKED> <CARD_MASKED>`가 됐습니다. 내장 email 미들웨어는 입력과 출력의 `learner@example.com`을 `learner@****.com`으로 바꿨습니다.
- 03절: 결정적 미들웨어 실행에서 주 모델 입력 메시지가 6개에서 3개로 줄고 출처 `E01 p.3`이 남았습니다. 실제 모델은 “대출은 5권이며 기간은 14일이고 예약이 없으면 7일 연장되며, 출처는 E01 p.3입니다.”라고 요약했고 예상비용은 0.000262달러였습니다.
- 04절: 첫 TimeoutError 뒤 두 번째 호출이 성공했고, 주 모델 실패 뒤 보조 모델 응답을 받았습니다. `run_limit=1`에서는 도구 실행 뒤 두 번째 모델 호출 전에 `Model call limits exceeded: run limit (1/1)` 메시지로 종료됐으며 모델 호출 수는 1이었습니다.
- 05절: 호출당 0.004달러, 상한 0.006달러 조건에서 첫 호출만 실행되고 두 번째 호출은 `BudgetExceeded`로 차단됐습니다.
- 06절: `agent_start → tool_start → tool_success → agent_end` 네 이벤트가 남고 이메일 원문과 도구 결과 원문은 직렬화된 이벤트에 없었습니다.
- 07절: A·B·C의 before는 순방향, wrap 진입은 순방향·반환은 역방향, after는 역방향인 18개 trace가 예상 목록과 같았습니다.
- 08절: 상태의 loan 3개·hr 2개 메시지 가운데 모델 요청에는 loan 3개만 전달됐습니다. 원래 상태 5개는 유지했습니다.
- `verify.py --chapter`: `PASS 8 sections / 50 code cells (max 24 lines)`입니다.
- `visual.cjs`: 9페이지를 1280px·390px로 측정한 18건이 모두 PASS입니다. 작은 글자·대비·잘림·본문 밖 텍스트·SVG 경계·가로 넘침·깨진 이미지·복사·다운로드 오류가 0건입니다.
- 공개 파일 목록 28개와 Ch16 선행 파일 목록 2개가 모두 존재합니다.

## 확인 필요 항목

- 한국어 감사 3단은 집필자와 다른 검토 세션에서 수행할 예정입니다.
- 01절과 03절의 실제 모델 문장·토큰 수·예상비용은 실행 시점에 달라질 수 있습니다.

## 품질 개선 시범 검증 (2026-09-15)

규격 `textbook/QUALITY-UPGRADE.md`로 8절을 다시 썼습니다. 가짜 모델을 없애고 gpt-5.4-mini(폴백 실험은 gpt-5.4-nano)를 temperature 0으로 호출합니다. 위 기록은 개선 전 판본의 결과입니다.

- `execute.py`: 8개 노트북을 새 커널에서 실행해 모두 PASS입니다.
- `verify.py --chapter`: `PASS 8 sections / 116 code cells (max 12 lines)`입니다.
- `upgrade_gates.py --label after --strict`: G1~G7 모두 0건, 8/8절 통과입니다. 수정 전은 G1 55·G2 51·G3 50·G4 10·G5 51·G6 145·G7 24건이었습니다.
- `visual.cjs`: 9페이지 × 1280px·390px, 18건 모두 PASS입니다.
- Ch21 빌드를 다시 실행해 공유 빌더 수정의 회귀가 없음을 확인했습니다.
- 별도 세션 검토 2회: 1차는 8절 모두 accept-with-fixes(상 5건 포함), 2차는 accept 6절·accept-with-fixes 2절이었습니다. 2차 지적까지 모두 반영했습니다.
- 주요 출력: 01 기록 12줄(모델 2·도구 1) / 02 `learner@****.com`, `****5678` / 03 입력 6 → 3, 글자 130 → 381 / 04 시도 3번, 폴백 nano, 호출 1번에서 멈춤 / 05 합계 104, 차단 뒤 사용량 45 / 06 사건 4개, 원문 없음 / 07 8줄 규칙 일치 / 08 입력 5 → 3, 기록 6개.

### 확인 필요 항목 (시범)

- 삽화 8장: 2026-09-15 nano_banana_pro 16:9 2k로 생성했습니다. 「그림만 보고 관계가 읽히는가」 검수에서 05(화면 색이 열림/닫힘을 흐림)와 07(바깥 봉투 안에 안쪽 봉투가 안 보임)을 탈락시키고 프롬프트를 고쳐 다시 만들었습니다. 본문 HTML에만 넣었고 게이트 8/8·verify·visual 18건을 다시 통과했습니다.
- 모델 문장과 토큰 수는 재실행마다 달라집니다. 재실행하면 본문 숫자를 다시 대조합니다.
- 실습 묶음 `textbook/downloads/llm-practice.zip`은 규격 확정 뒤 다시 만듭니다.

## 챕터 끝 실습 절 09 추가 (2026-09-16)

- 강사 요청으로 챕터 끝에 `09-Middleware-실습`(제목 「Middleware 실습: 도서관 상담 에이전트」)을 추가했습니다. 처음에는 「강사 시연」으로 만들었다가, 학생과 함께 실행하는 예제라서 이름을 바꿨습니다. 02절 이메일 가리기, 04절 호출 한도, 06절 감사 기록, 01·02절 모델 입력 기록을 한 에이전트에 붙였습니다.
- `execute.py` PASS(코드 셀 19개), `verify.py --chapter` `PASS 9 sections / 135 code cells (max 14 lines)`, 게이트 9/9절 0건, `visual.cjs` 09절·08절·목차 6건 PASS(이름 변경 뒤 다시 실행).
- 실행 1(한도 4): 모델 호출 2번, 모델 입력 `learner@****.com`, 감사 사건 agent_start·tool_call(renew_loan)·agent_end, 기록 속 원문 없음 False.
- 실행 2(한도 1): 모델 호출 1번, `Model call limits exceeded: run limit (1/1)`, tool 메시지와 감사 끝 사건은 남음.
- 별도 세션 검토 1회(accept-with-fixes): 호출 한도 자리 설명, 도구 실행 근거(tool 메시지 출력 추가), 결론 범위, 삽화 순서 등 지적을 모두 반영했습니다.
- 삽화 09-4 생성(job d242bcab-c627-43cd-abfa-1eb84266fc86, 2크레딧) 후 검수 통과.
- Part 6 목차(`textbook/part6/index.html`)와 실습 묶음은 아직 다시 만들지 않았습니다(규격 확정 뒤 일괄).
