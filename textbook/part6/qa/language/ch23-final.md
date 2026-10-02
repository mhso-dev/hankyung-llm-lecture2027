# Ch23 한국어 감사 최종 기록

- 장르: 산문형 학습자료 · 대상: 개발 입문 수강생
- 범위: 본문 6개, `chapter.json` 산문 필드, SVG 캡션 6개, README 1개, 노트북 Markdown 6개

## 1차 슬롭 검토

학습 목표·도입·정리가 절별 실험 대신 같은 저장·재개 일반론을 반복했습니다. `멱등성가`처럼 조사가 잘못 붙은 표현도 있었습니다.

## 수정

각 절의 목표·도입·정리를 실행값으로 바꿨습니다. `UndefinedTable`과 표 생성, 새 SQLite 연결의 대화 복원, durability의 종료 시점, `good, flaky, flaky`, `order-2306`의 2회·1회 기록을 각 절에 연결했습니다. async 관찰의 조건부 성격과 외부 부작용의 별도 멱등성 필요성도 분명히 했습니다.

도식은 PostgreSQL·SQLite와 checkpoint 표를 초록, 그래프 제어를 파랑, 장애를 빨강으로 역할에 맞춰 국소 수정했습니다.

## 2차 맞춤법

외부 맞춤법 서비스는 사용하지 않았습니다. [korean-spell-check SKILL.md](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md)의 “상업적 대량 처리” 사용 금지에 따라 일괄 전송 대신 로컬 전문 정독을 했습니다.

## Phase 6 최종 판정

`accept`. 원문과 수정본을 절 단위로 대조했습니다. 코드·출력·수치·날짜·고유명사·참고 URL은 보존됐고, 수정은 반복 산문과 조사 오류 및 관찰 범위의 국소 보정에 한정했습니다.
