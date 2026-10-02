# Ch24 실행 검증

- 실행일: 2026-09-11
- 환경: Python 3.12.13, LangGraph 1.2.11
- 노트북: 3개를 각각 새 커널에서 실행했습니다. 공통 검증기는 13개 코드 셀과 셀당 최대 24줄을 확인했습니다.
- 외부 동작: 실습 폴더의 로컬 텍스트 파일만 사용했습니다. 모델 API, 데이터베이스, 외부 업무 시스템은 호출하지 않았습니다.

## 실제 결과

- 01절: 부작용 뒤에 interrupt를 둔 실행은 거절해도 `transfer-local`이 2회 기록됐습니다. interrupt를 먼저 둔 실행은 `status='rejected'`를 반환하고 파일을 만들지 않았습니다.
- 02절: 첫 interrupt payload를 확인했고 `maybe`를 전달하자 오류가 포함된 두 번째 payload가 반환됐습니다. `approve`로 재개한 결과 `decision='approve'`, `next=()`였습니다.
- 03절: 원본 할인율 0.1의 최종 가격은 9000이었습니다. `discount` 직전 체크포인트의 할인율을 0.2로 바꾼 분기는 8000이었고 원본 결과는 9000으로 보존됐습니다.

## 검증 명령 결과

- `execute.py notebooks/*.ipynb --cwd <project-root>` → 3개 PASS
- `_build.py` → index와 절 3개 생성
- `verify.py --chapter textbook/part6/ch24-human-in-the-loop` → `PASS 3 sections / 13 code cells (max 24 lines)`
- `visual.cjs textbook/part6/ch24-human-in-the-loop` → 1280px·390px에서 3개 절과 index 모두 PASS
- 01절을 `--cwd labs/part6/ch24-human-in-the-loop/notebooks`로 다시 실행해 노트북 폴더 기준 상대경로 실행을 확인했습니다.
- Part 6 노트북 준비 검사에서 Ch24 3개는 설치 셀, 구체적 목적 주석, 함수 타입 힌트, assert, 셀당 25줄 이하를 모두 충족했습니다.

## 확인 필요 항목

- 한국어 감사 3단은 집필자와 다른 검토 세션에서 수행할 예정입니다.
