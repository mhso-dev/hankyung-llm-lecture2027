# Ch34 비용·Rate Limit 엔지니어링 한국어 감사 기록

## 범위와 기준

- 대상: 교재 절 5개, 노트북 마크다운 5개, `labs/part7/ch34-cost-rate-limits/README.md`, 도식 SVG 5개
- 장르: 산문 · 최소 심각도: S1
- 초기 기준본: `qa/language/baseline/ch34-src/`, `qa/language/baseline/ch34-notebook-markdown/`
- 초기 SHA-256: `qa/language/baseline/ch34-source-sha256-before.txt`
- 최종 SHA-256: `qa/language/ch34-final-sha256.txt`, `qa/language/ch34-post-tech-final-source-sha256.txt`

## 진단 요약

비용·캐시·배치·모델 선택·재시도·예산이라는 다섯 주제를 실제 실행 범위와 함께 설명합니다. 전문을 독자, 편집자, 낭독 관점으로 세 번 읽었고, 문단별 역할과 수치·날짜·고유명사·기술적 양태를 대조했습니다. 교재 문어체 금지 표현, 번역투, 이중 피동, 기계적 결산 표현, 수사적 대조를 다시 검색했으나 최종본에는 수정 근거가 되는 잔존 구간이 없습니다.

외부 맞춤법 검사는 상업적 대량 처리 금지 정책 때문에 전체 원문을 전송하지 않았습니다. 코드 블록·명령어·경로를 제외하고 전문을 로컬에서 읽어 띄어쓰기, 조사와 어미 호응, 수량 표현, 표준 문어체를 점검했습니다.

## 정독 소견

- 독자: 비용과 처리량을 실제 서비스 운영 지표로 연결하려는 수강생
- 목적: 작은 실행 결과의 범위를 보존하면서 비용 절감 조건과 한계를 설명합니다.
- 전체 인상: 절마다 개념, 실행, 해석, 한계가 일관된 순서로 이어집니다. 긴 문장은 조건과 해석을 담는 자리에 사용하고, 노트북 제목과 본문은 실행 흐름을 따라갑니다.

### 고친 자리

| 위치 | 수정 | 근거 |
| --- | --- | --- |
| 02절 실행·실패 설명 | 수량 수식어를 `고객 문의 세 건`, `세 개의 JSON 객체`로 정리 | 교재 문어체 수량 표기 |
| 03절 학습 목표 | 작은 표본을 일반화할 수 없는 이유를 설명하는 목표로 구체화 | 학습 행동을 분명히 하는 문장 |
| 04절 캡션·실행 확인 | `여섯 개의 작업`, `작업 여섯 개`로 수량과 대상을 명시 | 교재 문어체 수량 표기 |
| 05절 본문·복습 | 호출·대화·표본의 수량 표현과 문장 결속을 정리 | 교재 문어체 수량 표기, 표준 문장 구조 |

### 손대지 않은 자리

- 실제 실행 수치, 날짜, 모델명, API 경로, 코드·출력, 기술적 한정어는 보존했습니다.
- `A가 아니라 B` 구조는 기술적 구분을 설명하는 자리에서만 쓰였고 수사적 대비가 아니므로 보존했습니다.

## 수정 텍스트 경로

- `textbook/part7/ch34-cost-rate-limits/_src/02-Batch-API.html`
- `textbook/part7/ch34-cost-rate-limits/_src/03-모델-라우팅.html`
- `textbook/part7/ch34-cost-rate-limits/_src/04-백오프-큐-동시성.html`
- `textbook/part7/ch34-cost-rate-limits/_src/05-예산-가드와-p95.html`

노트북 마크다운과 README는 언어 감사에서 수정하지 않았습니다. 노트북 마크다운의 초기·최종 SHA-256은 `qa/language/ch34-notebook-markdown-sha256-before.txt`, `qa/language/ch34-notebook-markdown-sha256-after.txt`에서 일치합니다.

## 도식과 실행 자료 확인

다섯 SVG는 모두 짧고 완결된 `aria-label`을 제공하며, 도식의 상자 색·화살표·표시 값과 최신 캡션의 설명이 맞습니다. 기술 수정으로 노트북 01~03의 실습 경로와 실행 수치가 갱신됐습니다. 이는 언어 감사 전에 완료된 변경이며, 01절 본문의 `11,805`, `11,804`, `11,520`, `284`는 노트북 출력과 `runs/cache-measurement.json`의 기록과 일치합니다.

언어 감사 뒤 코드·출력 해시는 변하지 않았습니다. 비교 기록은 `qa/language/ch34-notebook-code-output-sha256-post-tech-only.txt`와 `qa/language/ch34-notebook-code-output-sha256-final2.txt`입니다.

## 기계 점검과 최종 검수

- `_build.py`: 5절과 챕터 색인 생성
- `verify.py`: `PASS 5 sections / 26 code cells (max 19 lines)`
- `verify_gates.py`: 절별 기록은 `qa/language/ch34-*-verify-gates-final2.txt`에 보관했습니다. P1·P2는 통과했습니다. 02~05절의 P3도 통과했고, 01절 P3 WARN은 재실행으로 `11,807/11,806/286`이 `11,805/11,804/284`로 바뀐 기술 동기화에서 생긴 이전 기준본 대비 수치 차이입니다. P0 WARN은 1.3~2.1%의 국소 수정률을 알리는 보고입니다.
- 시각 검사: 이 환경에서는 Playwright 모듈을 찾지 못해 다시 실행하지 못했습니다. 이전 기술 검토의 화면 검사 기록은 `textbook/part7/ch34-cost-rate-limits/qa/verification.md`에 있습니다.

Phase 6에서는 원문과 최종본을 문단 단위로 대조해 사실·주장·수치·날짜·고유명사·인용·예시·한정어·제목 독립성·문단 순서를 확인했습니다. 새 수사, 과도한 격식화, 문학화가 없고 수정한 수량 표기도 같은 실행 범위를 유지합니다.

최종 검수: `corrected`

- 의미 보존 15항: 통과
- 자연성 잔존: 수량 표현과 학습 목표의 모호함을 국소 보정
- 과윤문: 없음
- 게이트 재확인: exit 1 (P0 저윤문 WARN만 해당)

## 확인 필요 항목

없음.
