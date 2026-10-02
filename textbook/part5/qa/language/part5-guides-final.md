# Part 5 안내 문서 한국어 감사

## 감사 결과

- 상태: `accept`
- 범위: `textbook/part5/_src/index.html`, `textbook/part5/practice-start.md`, `labs/part5/continuity-guide.md`
- 장르: 산문
- 최소 심각도: S1
- 일반 슬롭 감사: 세 파일 모두 결정적 S1 패턴이 없었습니다. 조사 호응, 수량 표현, 모호한 지시 관계, API 측정 절차 설명을 국소 수정했습니다.
- 정밀 윤문: 세 파일 모두 의미 보존 15항과 자연성 양방향 대조를 통과했습니다. 격식 상향, 상투구 주입, 문학화, 새로운 주장 주입은 없습니다.
- 코드·경로 보호: 감사 입력과 최종본의 백틱 및 `<code>` 문자열 집합이 같습니다. 구조 게이트의 수치·인용·격식 불변식도 세 파일 모두 통과했습니다.

## 원본 스냅숏과 해시

아래 원본은 윤문과 Ch 19 기술 정정 전에 저장했습니다. 원본 파일과 스냅숏의 SHA-256이 일치합니다.

| 원본 파일 | 스냅숏 | SHA-256 |
|---|---|---|
| `textbook/part5/_src/index.html` | `textbook/part5/qa/language/part5-guides-original/textbook-part5-src-index.html` | `ea20941183ba672f5baa825b187a034257c169e16c920d3d1b12685aba4b3323` |
| `textbook/part5/practice-start.md` | `textbook/part5/qa/language/part5-guides-original/textbook-part5-practice-start.md` | `802f939d6ce378197e34c29c9cbce6d053d720518a61882d18d4320b9fdbed27` |
| `labs/part5/continuity-guide.md` | `textbook/part5/qa/language/part5-guides-original/labs-part5-continuity-guide.md` | `88ab79efaeaaea6fb0ebb034b3a21b16a325055e78b2969f875f46ca518dc364` |

## 최종본 해시

| 최종 파일 | SHA-256 |
|---|---|
| `textbook/part5/_src/index.html` | `160d152361fffe749fb8954644a5ce4d843e7cfdf978cfa5777b3c8c74eb794a` |
| `textbook/part5/practice-start.md` | `5ca16b81221be4881ac4afe31d8584919b5321ccca210f4489bfdf566f6c96c3` |
| `labs/part5/continuity-guide.md` | `e0ddb44f1bd6747c9089a2381d96fbace204ba84804bcbb553c5414e9588da6a` |

## 주요 변경 사항

### `textbook/part5/_src/index.html`

- `한두 질문`을 `한두 개의 질문`으로 고쳐 수량 표현을 완결했습니다.
- `자료 종류`에 조사를 보완하고, 제공 폴더 구조를 유지해야 하는 목적을 분명히 했습니다.
- `묶음`이 가리키는 대상을 `압축 파일`로 밝혔습니다.

### `textbook/part5/practice-start.md`

- `코드 실행은 … 합니다`를 `코드는 … 실행합니다`로 고쳐 주어와 서술어의 관계를 분명히 했습니다.
- Ch 19 노트북이 실제로 읽는 파일을 `labs/part5/ch19-model-tools/data/orders.csv`로 명시했습니다. `labs/part1/ch04-data-tools`는 원본 비교용으로 함께 제공된다고 구분했습니다.
- `OPENAI_API_KEY=` 뒤의 입력 위치, 셀별 실행 확인, API를 호출해 측정한다는 절차를 분명히 했습니다.

### `labs/part5/continuity-guide.md`

- 에이전트를 도입할 필요가 없다는 결론도 허용하는 원문의 가능성을 유지하면서 조사 호응을 고쳤습니다.
- Ch 19의 실제 데이터 경로, Ch 4 파일과의 바이트 일치, 첫 번째 노트북의 함수 본문·SHA-256 출처 표기를 구분해 적었습니다.
- 모델의 도구 호출 요청과 실제 함수 실행의 차이, 고정 예시와 직접 API 측정 결과의 차이는 그대로 보존했습니다.

## Ch 19 기술 정정 확인

- `labs/part5/ch19-model-tools/data/orders.csv`와 `labs/part1/ch04-data-tools/data/orders.csv`의 SHA-256은 모두 `f2d1e3ee1e4f6d22fd1cf84b0c77242a66a344ae7925be74c5d471569366ef64`입니다.
- Ch 19의 노트북 6개 모두 `data/orders.csv` 경로를 설정합니다.
- 첫 번째 노트북은 Ch 4 원본 함수 SHA-256 `64beca22…a81`과 함수 본문 일치를 명시합니다. 실제 `labs/part1/ch04-data-tools/data_tools.py`의 SHA-256은 `64beca22ff1546244224e975bf7945334adb85ccf0a916f3a17226be577a3a81`입니다.

## 한국어 감사 3단

1. `moai-coworker:ai-slop-reviewer`: 일반 AI 패턴을 전문 정독으로 확인하고 국소 수정했습니다.
2. `moai-writer:korean-spell-check`: 외부 검사기에 전송하지 않았습니다. `/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md`의 29행은 “대량 배치, SaaS 백엔드 연동, 상업 서비스 내 무단 재판매·재노출에는 사용하지 않습니다”라고 규정하고, 35행은 “상업적 대량 처리”를 사용 금지 대상으로 둡니다. 이 교재는 상업 교육과정의 Part 전체를 일괄 집필하는 작업이므로 외부 전송 단계를 생략했습니다.
3. `moai-writer:korean-humanize`: 장르 산문, 최소 심각도 S1로 전문을 세 번 읽고 국소 윤문했습니다. Phase 6에서 원문과 최종본을 문단 단위로 대조했습니다.

## 구조 게이트와 최종 판정

| run_id | 대상 | 변경률 | P1 | P2 | P3 | P5 리듬 | 판정 | 등급 |
|---|---|---:|---|---|---|---|---|---|
| `2026-09-10-001` | Part 5 인덱스 도입부 | 1.1% | PASS | PASS | PASS | 기준선 안 | accept | B |
| `2026-09-10-004` | 실습 시작 안내 | 1.1% | PASS | PASS | PASS | 기준선 안 | accept | B |
| `2026-09-10-005` | 학습 연결 안내 | 1.8% | PASS | PASS | PASS | 기준선 안 | accept | B |

세 run 모두 P0에서 5% 미만 저윤문 경고가 발생했습니다. 원문에 S1 패턴이 없고 지목한 문장만 고쳤기 때문에 변경률을 높이기 위한 추가 수정은 하지 않았습니다. 수치·인용·격식 불변식과 리듬 검사는 통과했습니다. B 등급은 A 등급의 최소 변경률 10%에 미치지 않아 부여됐으며, 잔존 S1이나 의미 훼손에 따른 등급이 아닙니다.

최종 검수: `accept`

- 의미 보존 15항: 통과
- 자연성 잔존: 조사 생략과 모호한 지시 관계를 완화했고 S1 패턴은 없습니다.
- 과윤문: 없음
- 게이트 재확인: exit 1. 저윤문 경고만 발생했습니다.
- codex 적대적 감사: 사용할 수 있는 `mcp__moai__codex_*` 도구가 없어 실행하지 않았습니다.

## 명령과 문서 구조 검증

- `uv sync --locked`: Ch 18 폴더에서 정상 완료했습니다.
- `uv run python --version`: `Python 3.12.13`을 확인했습니다.
- `uv run --with jupyterlab==4.4.9 jupyter lab`: JupyterLab 4.4.9가 실행되어 Ch 18 폴더를 제공하는 것을 확인한 뒤 정상 종료했습니다.
- `_src/index.html`: HTML5의 불리언 `download` 속성을 XML 표현으로 바꾼 검사 입력에서 구조 파싱을 통과했습니다. 원본의 HTML5 표기는 바꾸지 않았습니다.
- 감사용 `final.md` 세 파일과 실제 최종 파일의 바이트가 일치합니다.

## 확인 필요 항목

- `textbook/downloads/part5-practice.zip`은 감사 시점에 아직 생성되지 않았습니다. `_build_index.py`가 전체 챕터 검증 뒤 이 파일과 `env.example`, `manifest.json`을 생성하므로 Part 5 통합 빌드에서 링크와 압축 파일 내용을 확인해야 합니다.
